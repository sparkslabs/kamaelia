#!/usr/bin/env python

import textwrap
import inspect
import pprint
import time
from docutils import core
from docutils import nodes
import docutils


class RenderHTML(object):
    
    def __init__(self, debug=False):
        super(RenderHTML,self).__init__()
        self.debug=debug
        
    def makeFilename(self, docName):
        return docName + ".html"
    
    def makeURI(self, docName):
        return self.makeFilename(docName)
        
    def render(self, docName, docTree):
        if not isinstance(docTree, nodes.document):
            root = core.publish_doctree('')
            root.children = docTree
            docTree = root

        reader = docutils.readers.doctree.Reader(parser_name='null')
        pub = core.Publisher(reader, None, None, source=docutils.io.DocTreeInput(docTree),
                             destination_class=docutils.io.StringOutput)
        pub.set_writer("html")
        output = pub.publish(enable_exit_status=None)

        parts = pub.writer.parts
        
        doc = parts["html_title"] \
            + parts["html_subtitle"] \
            + parts["docinfo"] \
            + parts["fragment"]
            
        wholedoc = self.headers(doc) + doc + self.footers(doc)
        return doc
    
    def headers(self,doc):
        return "<html><body>\n"
    
    def footers(self,doc):
        return "</body></html>n"
    
#    def itemPairList(self, items):
#        return self.simpleList([ "<b>"+str(item[0])+"</b> : "+str(item[1]) for item in items ])
#
#    def simpleList(self, items):
#        return "<ul><li>"+ ("\n<li>".join(items))+"\n</ul>"
#
#    def heading(self, label, level=4):
#        if level == 2: return "<h2>" + label + "</h2>\n"
#        if level == 3: return "<h3>" + label + "</h3>\n"
#        if level == 4: return "<h4>" + label + "</h4>\n"
#        if level == 5: return "<h5>" + label + "</h5>\n"
#
#    def preformat(self, somestring):
#        lines = somestring.split("\n")
#        if self.debug:
#            for i in range(len(lines)):
#                print i,":", repr(lines[i])
#        somestring = somestring.replace("(*","(\*")
#        parts = core.publish_parts(somestring,writer_name="html")
#        doc = parts["html_title"] \
#            + parts["html_subtitle"] \
#            + parts["docinfo"] \
#            + parts["fragment"]
#        
#        return doc
#
#    def divider(self):
#        return "\n"
#    
#    def hardDivider(self):
#        return "\n<hr />\n"
#    
#    def setAnchor(self,name):
#        return '\n<a name="'+name+'" />'
#    
#    def linkToAnchor(self,name,text):
#        return '<a href="#' + name +'">' + text + '</a>'
#    
#    def linkTo(self,name,text):
#        return '<a href="' + name + '.html">' + text + '</a>'
#    
#    def start(self): return "<html><body>\n"
#    def stop(self): 
#        return """\
#<HR>
#<h2> Feedback </h2>
#<P>Got a problem with the documentation? Something unclear, could
#be clearer? Want to help with improving? Constructive criticism,
#preferably in the form of suggested rewording is very welcome.
#
#<P>Please leave the feedback 
#<a href="http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685"> 
#here, in reply to the documentation thread in the Kamaelia blog</a>. 
#</body></html>
#"""
#