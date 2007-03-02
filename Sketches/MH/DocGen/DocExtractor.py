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

    uid = 0

    def genUniqueRef(self):
        uid = str(self.uid)
        self.uid+=1
        return uid

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
                ids   = ["component-"+componentName+"-"+label],
                names = ["component-"+componentName+"-"+label],
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
            
        return nodes.section('', *core.publish_doctree(docstring).children)
#        pre = ""
#        if main:
#            pre = "\n"
#
#        return pre + self.renderer.preformat(docstring)+ "\n"

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        docTree = nodes.section('') #self.emptyTree()
        
        for method in sorted([x for x in inspect.classify_class_attrs(X) if x[2] == X and x[1] == "method"]):
            if method[0][-7:] == "__super":
                continue
            methodHead = method[0]+self.formatArgSpec(inspect.getargspec(method[3]))
            
            docTree.append( nodes.section('',
                                ids   = ["component-"+X.__name__+"-method-"+method[0]],
                                names = ["component-"+X.__name__+"-method-"+method[0]],
                                * [ nodes.title('', methodHead) ]
                                  + self.docString(method[3].__doc__)
                            )
                          )

        return docTree

    def formatClassStatement(self, name, bases):
        return "class "+ name+"("+",".join([str(base)[8:-2] for base in bases])+")"
    
    def formatPrefabStatement(self, name):
        return "prefab: "+name

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

        return nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["component-"+X.__name__]) ]
                  + CLASSDOC
                  + [ INBOXES, OUTBOXES ]
                  + METHODS
            )
        
    def formatPrefab(self, X):
        CLASSNAME = self.formatPrefabStatement(X.__name__)
        CLASSDOC = self.docString(X.__doc__)
        
        return nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["component-"+X.__name__]) ]
                  + CLASSDOC
            )
        
#    def componentAnchor(self, C):
#        return self.renderer.setAnchor(C)
#    
    def formatModuleTrail(self, moduleName):
        path = moduleName.split(".")
        
        trail = nodes.paragraph('')
        line = trail
        
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
        return nodes.section('',
#            nodes.paragraph('', '', nodes.Text('Components and Prefabs')),
            nodes.bullet_list('',
                *[ nodes.list_item('',
                       nodes.paragraph('', '',
                         nodes.strong('', '',
                           nodes.reference('', COMPONENT, refid='component-'+COMPONENT))
                         )
                       )
                   for COMPONENT in componentList
                 ]
                )
            )

    def formatModule(self, moduleName, module, components, prefabs):
        
        trailTree = self.formatModuleTrail(moduleName)
        moduleTree = self.docString(module.__doc__, main=True)
        toc = self.buildTOC(moduleTree, depth=3)
        
        allDeclarations = []
        
        declarationTrees = {}
        for component in components:
            declarationTrees[component.__name__] = self.formatComponent(component, includeMethods=True)
            
        for prefab in prefabs:
            assert(prefab.__name__ not in declarationTrees)
            declarationTrees[prefab.__name__] = self.formatPrefab(prefab)
            
        for name in sorted(declarationTrees.keys()):
            allDeclarations.extend(declarationTrees[name])
        
        componentListTree = self.componentList( sorted(declarationTrees.keys()) )

        return nodes.section('',
            trailTree,
#            nodes.paragraph('', nodes.Text("Component/Prefab details")),
            componentListTree,
            nodes.paragraph('', nodes.Text("Explanations")),
            toc,
            nodes.transition(),
            moduleTree,
            nodes.transition(),
            nodes.section('',
                id = [ 'component-declarations' ],
                name = [ 'component-declarations' ],
                * [ nodes.title('', "Component/Prefab details"),
                    nodes.section('',
                        *allDeclarations
                    )
                  ]
                )
            )
            
    def buildTOC(self, srcTree, parent=None, depth=3):
        """Recurse through a source document tree, building a table of contents"""
        if parent is None:
            parent = nodes.bullet_list()

        if depth<=0:
            return parent

        items=nodes.section()
        
        for n in srcTree.children:
            if isinstance(n, nodes.title):
                refid = self.genUniqueRef()
                n.attributes['ids'].append(refid)
                newItem = nodes.list_item()
                newItem.append(nodes.paragraph('','', nodes.reference('', refid=refid, *n.children)))
                newItem.append(nodes.bullet_list())
                parent.append(newItem)
            elif isinstance(n, nodes.section):
                if len(parent)==0:
                    newItem = nodes.list_item()
                    newItem.append(nodes.bullet_list())
                    parent.append(newItem)
                self.buildTOC( n, parent[-1][-1], depth-1)

        for item in items:
            if len(item[1]) == 0:
                item.remove(item[1])   # remove any empty bullet_list stubs
            parent.append(item)

        return parent
        
        toc = nodes.bullet_list('')


        
        tocEntry = nodes.list_item('')
        
        for n in srcTree.children:
            if isinstance(n, nodes.title):
                if len(tocEntry)>=1:
                    toc.append(tocEntry)
                tocEntry = nodes.list_item('')
                tocEntry.append(nodes.paragraph('', '', *n.children))
            elif isinstance(n, nodes.section):
                subToc = self.buildTOC(n, depth-1)
                if len(subToc)>=1:
                    tocEntry.extend(subToc)
        
        if len(tocEntry)>=1:
            toc.append(tocEntry)
            
        return toc


def generateDocumentationFiles(filterString):
    MODULES = dict(COMPONENTS.items())
    MODULES.update(dict(PREFABS.items()))
    MODULES = [M for M in MODULES.keys() if filterString in M]
    for MODULE in MODULES:
        print "Processing: "+MODULE
        
        cNames = COMPONENTS.get(MODULE,[])
        pNames = PREFABS.get(MODULE,[])
        
        module = __import__(MODULE, [], [], cNames+pNames)
        components = [ getattr(module, c) for c in cNames ]
        prefabs = [ getattr(module, p) for p in pNames ]
        
        doctree  = formatter.formatModule(MODULE, module, components, prefabs)
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
        P = Kamaelia.Support.Data.Repository.GetAllKamaeliaPrefabs()
        COMPONENTS = {}
        for key in C.keys():
            COMPONENTS[".".join(key)] = C[key]
        PREFABS = {}
        for key in P.keys():
            PREFABS[".".join(key)] = P[key]

    import sys
    filterPattern = ""
    if len(sys.argv)>1:
        filterPattern = sys.argv[1]

    generateDocumentationFiles(filterPattern)
    generateIndexFile()
