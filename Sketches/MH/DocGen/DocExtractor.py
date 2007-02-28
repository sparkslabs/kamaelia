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
import Kamaelia.Support.Data.Repository

from renderHTML      import RenderHTML
from renderPlaintext import RenderPlaintext




class docFormatter(object):
    def __init__(self, renderer=RenderPlaintext,debug=False):
        super(docFormatter,self).__init__()
        self.renderer = renderer(debug)
        self.debug = debug

    def boxes(self,label, boxes):
        items = []
        for box in boxes:
            try:
                description = boxes[box]
            except KeyError:
                description = ""
            except TypeError:
                description = "Code uses old style inbox/outbox description - no metadata available"
            items.append((box, description))

        return self.renderer.heading(label) + self.renderer.itemPairList(items) + self.renderer.divider()

    def name(self,name):
        return self.renderer.heading(name)

    def methodName(self,name):
        return self.renderer.heading(name,3)

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
            
        pre = ""
        if main:
            pre = self.renderer.divider()

        return pre + self.renderer.preformat(docstring)+ self.renderer.divider()

    def SectionHeader(self, header):
        return self.renderer.heading(header, 2)

    def paragraph(self, para):
        return self.renderer.divider()+ "<p>"+textwrap.fill(para)+ self.renderer.divider()

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        r = ""
        for method in sorted([x for x in inspect.classify_class_attrs(X) if x[2] == X and x[1] == "method"]):
            if method[0][-7:] == "__super":
                continue
            methodHead = method[0]+self.formatArgSpec(inspect.getargspec(method[3]))
            r += self.methodName(methodHead)+ self.docString(method[3].__doc__)

        return r

    def formatClassStatement(self, name, bases):
        return "class "+ name+"("+",".join([str(base)[8:-2] for base in bases])+")"

    def formatComponent(self, X):
        return self.SectionHeader(self.formatClassStatement(X.__name__, X.__bases__)) + \
               self.docString(X.__doc__, main=True) + \
               self.boxes("Inboxes", X.Inboxes) + \
               self.boxes("Outboxes", X.Outboxes) + \
               self.SectionHeader("Methods defined here")+ \
               self.paragraph("[[boxright][[include][file=Components/MethodNote.html][croptop=1][cropbottom=1] ] ]") +\
               self.formatMethodDocStrings(X)

    def preamble(self): return self.renderer.start()
    def postamble(self): return self.renderer.stop()
    
    def formatModule(self, M):
        return self.docString(M.__doc__, main=True)
    
    def hardDivider(self):
        return self.renderer.hardDivider()

    def componentAnchor(self, C):
        return self.renderer.setAnchor(C)
    
    def moduleTrail(self, moduleName):
        path = moduleName.split(".")
        
        trail = ""
        accum = ""
        firstPass=True
        for element in path:
            if not firstPass:
                accum += "."
            accum += element
            
            if not firstPass:
                trail += " . "
            trail += self.renderer.linkTo(accum, element)
            
            firstPass=False
            
        return self.paragraph(trail)
    
    def componentList(self, C):
        links = []
        for COMPONENT in C:
            links.append( self.renderer.linkToAnchor(COMPONENT,COMPONENT) )
            
        return self.paragraph("Components:"+self.renderer.simpleList(links))


def generateDocumentationFiles():
    for MODULE in COMPONENTS:
        module = __import__(MODULE, [], [], COMPONENTS[MODULE])
        F = open(docdir+"/"+MODULE+formatter.renderer.extension, "w")
        F.write(formatter.preamble())
        
        F.write(formatter.moduleTrail(MODULE))
        F.write(formatter.componentList(COMPONENTS[MODULE]))
        
        F.write(formatter.formatModule(module))
        F.write(formatter.hardDivider())
        
        for COMPONENT in COMPONENTS[MODULE]:
            F.write(formatter.componentAnchor(COMPONENT))
            X = getattr(module, COMPONENT)
            F.write(formatter.formatComponent(X))
            
        F.write(formatter.postamble())
        F.close()
        
        
#        for COMPONENT in COMPONENTS[MODULE]:
#            print
#            print "Processing: "+MODULE+"."+COMPONENT+" ..."
#            print "*" * len("Processing: "+MODULE+"."+COMPONENT+" ...")
#            F = open(docdir+"/"+MODULE+"."+COMPONENT+".html","w")
#            X = getattr(module, COMPONENT)
#            F.write(formatter.preamble())
#            F.write("<h1>"+ MODULE+"."+COMPONENT+"</h1>\n")
#            F.write(formatter.formatComponent(X))
#            F.write(formatter.postamble())
#            F.close()


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

    generateDocumentationFiles()
    generateIndexFile()
