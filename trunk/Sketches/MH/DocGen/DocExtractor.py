#!/usr/bin/python
#
# This program generates Kamaelia's documentation directly from the
# source. I am currently running this as follows:
#
# ./DocExtractor.py
# cp index.html ../../Website/Components/.
# cd tmp
# cp * ../../../Website/Components/pydoc/.
#
# This is then checked into the repository as follows:
#
# cd ../../../Website/Components/pydoc
# cvs add *html # produces warnings about double adds
# cd ..
# cvs ci
#

import textwrap
import inspect
import pprint
import time
from docutils import core
from docutils import nodes
import Kamaelia.Support.Data.Repository

from renderHTML      import RenderHTML
from renderPlaintext import RenderPlaintext




class docFormatter(object):
    def __init__(self, renderer=RenderPlaintext,debug=False):
        super(docFormatter,self).__init__()
        self.renderer = renderer(debug)
        self.debug = debug

    def emptyTree(self):
        return core.publish_doctree("")
    
    def boxes(self,componentName, label, boxes):
        items = []
        for box in boxes:
            try:
                description = boxes[box]
            except KeyError:
                description = ""
            except TypeError:
                description = "Code uses old style inbox/outbox description - no metadata available"
            items.append((str(box), str(description)))

        docTree= nodes.section('',
                ids   = ["section-"+componentName+"-"+label],
                names = ["section-"+componentName+"-"+label],
                *[ nodes.title('', label),
                   nodes.bullet_list('',
                      *[ nodes.list_item('', nodes.paragraph('', '',
                                                 nodes.strong('', boxname),
                                                 nodes.Text(" : "+boxdesc))
                                             )
                         for (boxname,boxdesc) in items
                       ]
                   ),
                ]
            )
        return docTree
    
    def docString(self,docstring, main=False):
        if docstring is None:
            docstring = " "
        lines = "\n".split(docstring)
        if len(lines)>1:
            line1 = textwrap.dedent(lines[0])
            rest = textwrap.dedent("\n".join(lines[1:]))
            docstring = line1+"\n"+rest
        else:
            docstring=textwrap.dedent(docstring)

        while docstring[0] == "\n":
            docstring = docstring[1:]
        while docstring[-1] == "\n":
            docstring = docstring[:-1]
            
        return core.publish_doctree(docstring).children
#        pre = ""
#        if main:
#            pre = "\n"
#
#        return pre + self.renderer.preformat(docstring)+ "\n"

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        docTree = self.emptyTree()
        
        for method in sorted([x for x in inspect.classify_class_attrs(X) if x[2] == X and x[1] == "method"]):
            if method[0][-7:] == "__super":
                continue
            methodHead = method[0]+self.formatArgSpec(inspect.getargspec(method[3]))
            
            docTree.append( nodes.section('',
                                ids   = ["section-"+X.__name__+"-method-"+method[0]],
                                names = ["section-"+X.__name__+"-method-"+method[0]],
                                * [ nodes.title('', methodHead) ]
                                  + self.docString(method[3].__doc__)
                            )
                          )

        return docTree.children

    def formatClassStatement(self, name, bases):
        return "class "+ name+"("+",".join([str(base)[8:-2] for base in bases])+")"

    def formatComponent(self, X, includeMethods=False):
        CLASSNAME = self.formatClassStatement(X.__name__, X.__bases__)
        CLASSDOC = self.docString(X.__doc__)
        INBOXES = self.boxes(X.__name__,"Inboxes", X.Inboxes)
        OUTBOXES = self.boxes(X.__name__,"Outboxes", X.Outboxes)
        
        if includeMethods:
            METHODS = [ nodes.section('',
                          nodes.title('', 'Methods defined here'),
                          * self.formatMethodDocStrings(X)
                        )
                      ]
        else:
            METHODS = []
        
        docTree = self.emptyTree()
        docTree.children.extend( [
            nodes.section('',
                ids   = ["section-"+X.__name__],
                names = ["section-"+X.__name__],
                * [ nodes.title('', CLASSNAME) ]
                  + CLASSDOC
                  + [ INBOXES,
                      OUTBOXES,
                    ]
                  + METHODS
            ),
        ] )
        return docTree
        
#    def componentAnchor(self, C):
#        return self.renderer.setAnchor(C)
#    
    def formatModuleTrail(self, moduleName):
        path = moduleName.split(".")
        
        trail = self.emptyTree()
        trail.append( nodes.paragraph('') )
        line = trail.children[0]
        
        accum = ""
        firstPass=True
        for element in path:
            if not firstPass:
                accum += "."
            accum += element
            
            if not firstPass:
                line.append(nodes.Text(" . "))
            URI = self.renderer.makeURI(accum)
            line.append( nodes.reference('', element, refuri=URI) )
            
            firstPass=False
        
        return trail
    
    def componentList(self, componentList):
        docTree = self.emptyTree()
        docTree.append( nodes.paragraph('', '', nodes.Text('Components')) )
        docTree.append( nodes.bullet_list('',
                          *[ nodes.list_item('',
                                nodes.paragraph('', '', nodes.reference('', COMPONENT, refid='section-'+COMPONENT))
                             )
                             for COMPONENT in componentList ]
                        )
                      )
                     
        return docTree

    def formatModule(self, moduleName, module, components):
        
        trailTree = self.formatModuleTrail(moduleName)
        moduleTree = self.docString(module.__doc__, main=True)
        moduleTree = self.promoteFirstTitle(moduleTree)
        
        allComponents = []
        
        componentTrees = {}
        for component in components:
            componentTrees[component.__name__] = self.formatComponent(component, includeMethods=False)
            
        for cname in sorted(componentTrees.keys()):
            allComponents.extend(componentTrees[cname])
        
        componentListTree = self.componentList( sorted(componentTrees.keys()) )
        
        rootTree = self.emptyTree()
        rootTree.extend(trailTree)
        rootTree.extend(componentListTree)
        rootTree.extend(moduleTree)
        rootTree.extend( nodes.section('',
                             id = [ 'section-ALL-COMPONENTS' ],
                             name = [ 'section-ALL-COMPONENTS' ],
                             * [ nodes.section('',
                                   * [ nodes.title('', "The Components") ]
                                   + allComponents
                                 )
                               ]
                         )
                       )

#        print rootTree
        return rootTree.children
            
    def promoteFirstTitle(self, docs):
        """If first element in these docelements is a title, then put everything
        below it into a section, to make sure they get nested to lower heading levels"""
        if len(docs)>=1 and isinstance(docs[0],nodes.title):
            docs = [ docs[0], nodes.section('', *docs[1:]) ]
        return docs



def generateDocumentationFiles(filterString):
    for MODULE in [M for M in COMPONENTS if filterString in M]:
        print "Processing: "+MODULE
        
        module = __import__(MODULE, [], [], COMPONENTS[MODULE])
        components = [ getattr(module, c) for c in COMPONENTS[MODULE] ]
        
        doctree  = formatter.formatModule(MODULE, module, components)
        filename = formatter.renderer.makeFilename(MODULE)
        output   = formatter.renderer.render(MODULE, doctree)
        
        F = open(docdir+"/"+filename, "w")
        F.write(output)
        F.close()
        
#        F.write(formatter.preamble())
#        
#        F.write(formatter.moduleTrail(MODULE))
#        F.write(formatter.componentList(COMPONENTS[MODULE]))
#        
#        F.write(formatter.formatModule(module))
#        F.write(formatter.hardDivider())
#        
#        for COMPONENT in COMPONENTS[MODULE]:
#            F.write(formatter.componentAnchor(COMPONENT))
#            X = getattr(module, COMPONENT)
#            F.write(formatter.formatComponent(X))
#            
#        F.write(formatter.postamble())
#        F.close()


def formatFile(SectionStack,File,KamaeliaDocs):
    filepath = "/Components/pydoc/"+".".join(SectionStack+[File])
    if len(KamaeliaDocs[File]) != 1 or File == "Experimental":
        components = [ x for x in KamaeliaDocs[File] ]
        components.sort()
        components = [ "<a href='" +filepath+"." +x+".html'>"+x+"</a>" for x in components ]
        return File + "("+ ", ".join(components) + ")"
    else:
        return "<a href='" +filepath+"." +KamaeliaDocs[File][0]+".html'>"+KamaeliaDocs[File][0]+"</a>"


def sectionStart(Filehandle, indent, section):
    if indent == "":
        Filehandle.write("""\
<div class="topsection">
  <div class="sectionheader"> %s </div>
  <div class="sectioncontent">
""" % (section,) )
    else:
        Filehandle.write( """\
<div class="subsection">
  <div class="sectionheader"> %s </div>
  <div class="sectioncontent">
""" % (section,))


def sectionEnd(Filehandle, indent):
    Filehandle.write(indent+"</div></div>\n")

def showSection(Filehandle, SectionStack, KamaeliaDocs,indent=""):
    global count
    sections = []
    thissection = []
#    if indent == "":
#        Filehandle.write('<table border="0">\n<tr><td>\n')
    for K in KamaeliaDocs.keys():
        try:
            KamaeliaDocs[K].keys()
            sections.append(K)
        except AttributeError:
            thissection.append(K)


    if indent != "":
        if thissection != []:
            if indent == "":
                Filehandle.write('<div class="none">&nbsp;</div>\n<p>Other Components:\n<ul>\n')
    
            Filehandle.write( indent+"   ")
            thissection.sort()
            for File in thissection:
                Filehandle.write( formatFile(SectionStack,File,KamaeliaDocs)+" ")
            Filehandle.write("\n")
            if indent == "":
                Filehandle.write( '</ul>\n')

    sections.sort()
    for section in sections:
        sectionStart(Filehandle, indent, section)
        showSection(Filehandle, SectionStack+[section],KamaeliaDocs[section],indent+"   ")
        sectionEnd(Filehandle, indent)

    if indent == "":
        if thissection != []:
            if indent == "":
                Filehandle.write( '<div class="none">&nbsp;</div>\n<p>Other Components:\n<ul>\n')
    
            Filehandle.write( indent+"   ")
            thissection.sort()
            for File in thissection:
                Filehandle.write( formatFile(SectionStack,File,KamaeliaDocs)+" ")
            Filehandle.write("\n")
            if indent == "":
                Filehandle.write( '</ul>\n')


def generateIndexFile():
    F = open("index.html","w")
    KamaeliaDocs = CN["Kamaelia"]
    F.write("""\
<html>
<style>
.topsection {
              width: 50%;
              float: left;
              padding-top: 0.3em;
            }
.subsection { }
.sectionheader {
                 font-weight: bold;
               }
.sectioncontent { font-size: 0.9em;
                  margin-left: 2em;
                }
.verticaldivider { float: bottom;
                   width: 100%;
                 }
.none { width: 100%;
        clear: both;
</style>

<body>
"""+ """<P>Last Generated: %s
""" % (time.asctime(),))

    showSection(F,["Kamaelia"],KamaeliaDocs)

    F.write("""\
</body>
</html>
""")


if __name__ == "__main__":

    docdir = "pydoc"
    
    formatter = docFormatter(RenderHTML)
#    formatter = docFormatter(RenderPlaintext)

    debug = False
    if debug:
        COMPONENTS = {
            "Kamaelia.ReadFileAdaptor" : ("ReadFileAdaptor",)
        }
    else:
        C = Kamaelia.Support.Data.Repository.GetAllKamaeliaComponents()
        CN = Kamaelia.Support.Data.Repository.GetAllKamaeliaComponentsNested()
        COMPONENTS = {}
        for key in C.keys():
            COMPONENTS[".".join(key)] = C[key]

    import sys
    filterPattern = ""
    if len(sys.argv)>1:
        filterPattern = sys.argv[1]

    generateDocumentationFiles(filterPattern)
    generateIndexFile()
