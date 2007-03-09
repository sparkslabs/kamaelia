#!/usr/bin/env python

import textwrap
import inspect
import pprint
import time
from docutils import core
from docutils import nodes
import docutils
import re

class RenderHTML(object):
    
    def __init__(self, debug=False, titlePrefix="", urlPrefix=""):
        super(RenderHTML,self).__init__()
        self.titlePrefix=titlePrefix
        self.debug=debug
        self.urlPrefix=urlPrefix
        self.mappings={}
        
    def makeFilename(self, docName):
        if docName=="Kamaelia":
            docName="index"
        return docName + ".html"
    
    def makeURI(self, docName):
        return self.urlPrefix+self.makeFilename(docName)
        
    def setAutoCrossLinks(self, mappings):
        self.mappings = {}
        for (key,ref) in mappings.items():
            pattern = re.compile("(?<![a-zA-Z0-9._])"+re.escape(key)+"(?![a-zA-Z0-9._])")
            uri = self.makeURI(ref)
            self.mappings[pattern] = uri
        
    def render(self, docName, docTree):
        if not isinstance(docTree, nodes.document):
            root = core.publish_doctree('')
            root.append(docTree)
            docTree = root

        docTree.attributes['title']=docName
        
        docTree.transformer.add_transform(boxright_transform)
        docTree.transformer.add_transform(crosslink_transform, priority=None, mappings=self.mappings)
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
        return """\
<html>
<head>
<title>"""+title+"""</title>
<style type="test/css">
pre.literal-block, pre.doctest-block {
  margin-left: 2em ;
  margin-right: 2em ;
  background-color: #eeeeee }
</style>
</head>
<body>
"""
    
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
        
class crosslink_transform(docutils.transforms.Transform):
    default_priority=100
    
    def apply(self, mappings):
        self.mappings = mappings
        self.recurse(self.document)
        
    def recurse(self, parent):
        i=0
        while i<len(parent.children):
            thisNode = parent[i]
            if isinstance(thisNode, nodes.Text):
                changeMade = self.crosslink(parent, i)
                if not changeMade:
                    i=i+1
            else:
                if isinstance(thisNode, (nodes.reference,)): # nodes.literal_block)):
                    pass
                elif thisNode.children:
                    self.recurse(thisNode)
                i=i+1
            
    def crosslink(self, parent, i):
        text = parent[i].astext()
        for pattern in self.mappings.keys():
            match = pattern.search(text)
            if match:
                head = text[:match.start()]
                tail = text[match.end():]
                middle = text[match.start():match.end()]
                URI = self.mappings[pattern]
                
                parent.remove(parent[i])
                if tail:
                    parent.insert(i, nodes.Text(tail))
                if middle:
                    parent.insert(i, nodes.reference('', nodes.Text(middle), refuri=URI))
                if head:
                    parent.insert(i, nodes.Text(head))
                return True
        return False
        