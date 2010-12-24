#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
========================
Doctree to HTML Renderer
========================

Renderer for converting docutils document trees to HTML output with Kamaelia
website specific directives, and automatic links for certain text patterns.


"""

import textwrap
import inspect
import pprint
import time
from docutils import core
from docutils import nodes
import docutils
import re

class RenderHTML(object):
    """\
    RenderHTML([debug][,titlePrefix][,urlPrefix][,rawFooter]) -> new RenderHTML object

    Renders docutils document trees to html with Kamaelia website specific
    directives.

    Also contains helper functions for determining filenames and URIs for
    documents.

    Keyword arguments::

    - debug        -- Optional. True for debugging mode - currently does nothing (default=False)
    - titlePrefix  -- Optional. Prefix for the HTML <head><title> (default="")
    - urlPrefix    -- Optional. Prefix for all URLs. Should include a trailing slash if needed (default="")
    - rawFooter    -- Optional. Footer text that will be appended just before the </body></html> tags (default="")
    """
    
    def __init__(self, debug=False, titlePrefix="", urlPrefix="",rawFooter=""):
        super(RenderHTML,self).__init__()
        self.titlePrefix=titlePrefix
        self.debug=debug
        self.urlPrefix=urlPrefix
        self.rawFooter=rawFooter
        self.mappings={}
        
    def makeFilename(self, docName):
        """\
        Returns the file name for a given document name.

        Eg. "Kamaelia.Chassis" will be mapped to something like "Kamaelia.Chassis.html"
        """
        return docName + ".html"
    
    def makeURI(self, docName,internalRef=None):
        """\
        Returns the URI for a given document name. Takes into account the url prefix.

        Eg. "Kamaelia.Chassis" will be mapped to something like "/mydocs/Kamaelia.Chassis.html"
        """
        if internalRef is not None:
            suffix="#"+internalRef
        else:
            suffix=""
        return self.urlPrefix+self.makeFilename(docName)+suffix
        
    def setAutoCrossLinks(self, mappings):
        """\
        Set mapping for the automagic generation of hyperlinks between content.

        Supply a dict of mappings mapping patterns (strings) to the fully qualified
        entity name to be linked to.
        """
        self.mappings = {}
        for (key,ref) in mappings.items():
            # compile as an RE - detects the pattern providing nothign preceeds it,
            # and it is not part of a larger pattern, eg A.B is part of A.B.C
            pattern=re.compile("(?<![a-zA-Z0-9._])"+re.escape(key)+"(?!\.?[a-zA-Z0-9_])")
            # convert the destination to a URI
            uri = self.makeURI(ref)
            self.mappings[pattern] = uri
            
    def addAutoLinksToURI(self, mappings):
        for (key,uri) in mappings.items():
            pattern=re.compile("(?<![a-zA-Z0-9._])"+re.escape(key)+"(?!\.?[a-zA-Z0-9_])")
            self.mappings[pattern] = uri
        
        
    def render(self, docName, docTree):
        """\
        Render the named document tree as HTML with Kamaelia website specific directives.

        Returns string containing the entire HTML document.
        """
        if not isinstance(docTree, nodes.document):
            root = core.publish_doctree('')
            root.append(docTree)
            docTree = root

        docTree.attributes['title']=docName

        # do this first, before we turn the boxright nodes into "[ [boxright] ... ]"
        docTree.transformer.add_transform(squareBracketReplace_transform)
        docTree.transformer.apply_transforms()
        
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
        return self.rawFooter+"</body></html>\n"
    


from Nodes import boxright


class boxright_transform(docutils.transforms.Transform):
    """\
    Transform that replaces boxright nodes with the corresponding Kamaelia
    website [[boxright] <child node content> ] directive
    """
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
    """\
    Transform that searches text in the document for any of the patterns in the
    supplied set of mappings. If a pattern is found it is converted to a
    hyperlink
    """
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

class squareBracketReplace_transform(docutils.transforms.Transform):
    """\
    Transform that replaces square brackets in text with escape codes, so that
    the Kamaelia website doesn't interpret them as directives
    """
    default_priority=100

    def apply(self):
        for target in self.document.traverse(nodes.Text):
            newText = target.replace("[","%91%")
            newText = newText.replace("]","%93%")
            target.parent.replace(target, newText)
