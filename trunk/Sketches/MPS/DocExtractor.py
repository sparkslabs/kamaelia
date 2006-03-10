#!/usr/bin/python
#
#

import textwrap
import inspect
import pprint
from docutils import core
import Kamaelia.Data.Repository

C = Kamaelia.Data.Repository.GetAllKamaeliaComponents()
CN = Kamaelia.Data.Repository.GetAllKamaeliaComponentsNested()
COMPONENTS = {}
for key in C.keys():
    COMPONENTS[".".join(key)] = C[key]

docdir = "tmp"

class plainRender(object):
    def itemRateControlledReusableFileReaderList(self, items):
        result = []
        for item in items:
            result.append("   "+ str(item[0])+ " : "+ str(item[1]))
        return "\n".join(result)+"\n"

    def heading(self, label, level=4):
        if level == 2: 
            u = "".join(["*" for x in label])
            return "\n"+label + "\n"+ u + "\n"
        if level == 3: return label + "\n"
        if level == 4: return label + ":" + "\n"
        if level == 5: return label + ":"

    def preformat(self, somestring):
        lines = somestring.split("\n")
        L = []
        for l in lines:
            L.append("    "+l+"\n")
        return "".join(L)
    def divider(self):
        return "\n"
    def start(self): return ""
    def stop(self): return ""

class htmlRender(object):
    def itemList(self, items):
        result = []
        for item in items:
            result.append("   "+ str(item[0])+ " : "+ str(item[1]))
        return "<ul><li>"+ "\n<li>".join(result)+"\n</ul>"

    def heading(self, label, level=4):
        if level == 2: return "<h2>" + label + "</h2>\n"
        if level == 3: return "<h3>" + label + "</h3>\n"
        if level == 4: return "<h4>" + label + "</h4>\n"
        if level == 5: return "<h5>" + label + "</h5>\n"

#    def preformat(self, somestring):
#        lines = somestring.split("\n")
#        L = []
#        for l in lines:
#            L.append("    "+l+"\n")
#        return "<pre>\n"+"".join(L)+"\n</pre>\n"

    def preformat(self, somestring):
        lines = somestring.split("\n")
        if debug:
            for i in range(len(lines)):
                print i,":", repr(lines[i])
        somestring = somestring.replace("(*","(\*")
        doc = core.publish_parts(somestring,writer_name="html")["whole"]
        if debug:
            print "Wibble?"
        doclines=doc.split("\n")
        while """<div class="document">""" not in doclines[0]:
            doclines = doclines[1:]
        doclines = doclines[1:]
        while """</div>""" not in doclines[-1]:
            doclines = doclines[:-1]
        try:
            while """</div>""" in doclines[-1]:
                doclines = doclines[:-1]
        except IndexError:
            pass
        doc = "\n".join(doclines)
        return doc

    def divider(self):
        return "\n"
    def start(self): return "<html><body>\n"
    def stop(self): 
        return """\
<HR>
<h2> Feedback </h2>
<P>Got a problem with the documentation? Something unclear, could
be clearer? Want to help with improving? Constructive criticism,
preferably in the form of suggested rewording is very welcome.

<P>Please leave the feedback 
<a href="http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685"> 
here, in reply to the documentation thread in the Kamaelia blog</a>. 
</body></html>
"""

class docFormatter(object):
    def __init__(self, renderer=plainRender):
        self.renderer = renderer()

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

        return self.renderer.heading(label) + self.renderer.itemList(items) + self.renderer.divider()

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
        return self.renderer.divider()+ textwrap.fill(para)+ self.renderer.divider()

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")
#        print argspec
#        return "(" + ", ".join(argspec[0]) + ")"

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

formatter = docFormatter(htmlRender)

debug = False
if debug:
  COMPONENTS = {
    "Kamaelia.ReadFileAdaptor" : ("ReadFileAdaptor",)
}
def generateDocumentationFiles():
    for MODULE in COMPONENTS:
        module = __import__(MODULE, [], [], COMPONENTS[MODULE])
        for COMPONENT in COMPONENTS[MODULE]:
            print
            print "Processing: "+MODULE+"."+COMPONENT+" ..."
            print "*" * len("Processing: "+MODULE+"."+COMPONENT+" ...")
            F = open(docdir+"/"+MODULE+"."+COMPONENT+".html","w")
            X = getattr(module, COMPONENT)
            F.write(formatter.preamble())
            F.write("<h1>"+ MODULE+"."+COMPONENT+"</h1>\n")
            F.write(formatter.formatComponent(X))
            F.write(formatter.postamble())
            F.close()

KamaeliaDocs = CN["Kamaelia"]

def formatFile(File,KamaeliaDocs):
    if len(KamaeliaDocs[File]) != 1 or File == "Experimental":
        return File + "("+ ",".join(KamaeliaDocs[File]) + ")"
    else:
        return KamaeliaDocs[File][0]

def showSection(KamaeliaDocs,indent=""):
    sections = []
    thissection = []
    for K in KamaeliaDocs.keys():
        try:
            KamaeliaDocs[K].keys()
            sections.append(K)
        except AttributeError:
            thissection.append(K)

    sections.sort()
    for section in sections:
        print indent+"SECTION", section
        showSection(KamaeliaDocs[section],indent+"   ")
        print indent + "ENDSECTION"

    if thissection != []:
        if sections != []:
           print indent+"Other components :"

        print indent+"   ",
        for File in thissection:
            print formatFile(File,KamaeliaDocs),
        print

showSection(KamaeliaDocs)
