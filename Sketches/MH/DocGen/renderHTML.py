#!/usr/bin/env python

import textwrap
import inspect
import pprint
import time
from docutils import core
from docutils import nodes
import docutils


class RenderHTML(object):
    
    def __init__(self, debug=False, titlePrefix=""):
        super(RenderHTML,self).__init__()
        self.titlePrefix=titlePrefix
        self.debug=debug
        
    def makeFilename(self, docName):
        if docName=="Kamaelia":
            docName="index"
        return docName + ".html"
    
    def makeURI(self, docName):
        return self.makeFilename(docName)
        
    def render(self, docName, docTree):
        if not isinstance(docTree, nodes.document):
            root = core.publish_doctree('')
            root.append(docTree)
            docTree = root

        docTree.attributes['title']=docName
        docTree.transformer.add_transform(boxright_transform)
        docTree.transformer.apply_transforms()
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
            
        wholedoc = self.headers(docTree) + doc + self.footers(docTree)
        return wholedoc
    
    def headers(self,doc):
        title = self.titlePrefix + doc.attributes['title']
        return "<html><head><title>"+title+"</title></head><body>\n"
    
    def footers(self,doc):
        return "</body></html>\n"
    


from Nodes import boxright


class boxright_transform(docutils.transforms.Transform):
    default_priority=100

    def apply(self):
        boxes=[]
        for target in self.document.traverse(boxright):
            target.insert(0, nodes.Text("[[boxright] "))
            target.append(nodes.Text("]"))
            boxes.append(target)
        for box in boxes:
            box.replace_self( nodes.container('', *box.children) )
        