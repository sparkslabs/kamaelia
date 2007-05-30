#!/usr/bin/python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
==================================
Documentation extractor and writer
==================================

A command line tool for generating Axon and Kamaelia documentation

Features:

* outputs HTML (with some simple additional directives for the wiki engine
  behind the Kamaelia website)

* python DocStrings are parsed as
  `ReStructuredText<http://docutils.sourceforge.net/rst.html>`_ - permitting
  rich formatting.

* can document modules, classes, functions, components and prefabs

* some customisation control over the output format

* generates hierarchical indices of modules

* fully qualified module, component, prefab, class and function names are
  automagically converted to hyperlinks

* can incorporate test suite output into documentation

*This is not an Axon/Kamaelia system* - it is not built from components. However
it is probably sufficiently useful to be classified as a 'tool'!



Usage
-----

For help on command line options, use the ``--help`` option::

    $> ./DocExtractor.py --help

The command lines currently being used to generate Kamaelia and Axon
documentation are as follows:

For Kamaelia component docs for the website::

    $> ./DocExtractor.py --urlprefix /Components/pydoc/                \
                         --root Kamaelia                               \
                         --footerinclude Components/pydoc-footer.html  \
                         --outdir <outputDirName>                      \
                         <repositoryDir> 

For Axon docs for the website::

    $> ./DocExtractor.py --urlprefix /Docs/Axon/                       \
                         --promotetitles                               \
                         --notjustcomponents                           \
                         --indexdepth 0                                \
                         --root Axon                                   \
                         --footerinclude Docs/Axon-footer.html         \
                         --outdir <outputDirName>                      \
                         <repositoryDir> 

Why differences?

* The ``--notjustcomponents`` flag which ensures that the classes and functions
  making up Axon are documented.

* The remaining differences change the formatting and style:
    
  * ``promotetitles`` pushes module level doc string titles to the top of the
    HTML pages generated - making them more prominent.

  * ``indexDepth`` of 0 supresses the generation of indexes of modules in a
    given subdir. Axon's ``__init__.py`` contains a comprehensive table of
    contents of its own, so the index is not needed.



Not quite plain HTML
--------------------

Although the output is primarily HTML, it does include Kamaelia website specific
directives (of the form ``[[foo][attribute=value] blah blah ]``

Since these directives use square brackets, any square brackets in the body text
are replaced with escaped codes.



Implementation Details
----------------------

Kamaelia.Support.Data.Repository is used to scan the specified code base and
extract info and documentation about modules, classes, functions, components and
prefabs.

All python doc strings are fed through the
`docutils <http://docutils.sourceforge.net/>`_ ReStructuredText parser to
generate formatted HTML output.

Internally individual documentation pages are built up entirely using docutils
node structures (a convenient intermediate tree representation of the doucment)

A separate renderer object is used to perform the final conversion to HTML, as
well as resolve the automatic linking of fully qualified names. It also
determines the appropriate filenames and URLs to use for individual pages and
hyperlinks between them.

A few bespoke extensions are added to the repertoire of docutils nodes to
represent specific directives that need to appear in the final output. These
are converted by the renderer object to final ``[[foo][bar=bibble] ...]``
format.

This is done this way to keep an unambiguous separation between directives and
documentation text. If directives were dropped in as plain text earlier in the
process then they might be confused with occurrences of square brackets in the
actual documentation text.

Code overview

* The *DocGenConfig* class encapsulates configuration choices and also carries
  the extracted repository info.

* *__main__* invokes *generateDocumentationFiles()* and *generateIndices()* to
  kick off the construction of all documentation files and index page files.

* The actual formatting and generation of pages is performed by the *docFormatter*
  class.

  * *formatXXXPage()* methods return document node trees representing the final
    pages to be converted to HTML and written to disk.

  * Other *formatXXX()* methods construct fragments of the document tree.


"""


import textwrap
import inspect
import pprint
import time
import os
import StringIO
from docutils import core
from docutils import nodes
#from Kamaelia.Support.Data import Repository
import Repository


from renderHTML import RenderHTML

from Nodes import boxright

class DocGenConfig(object):
    """Configuration object for documentation generation."""
    def __init__(self):
        super(DocGenConfig,self).__init__()
        # NOTE: These settings are overridden in __main__ - modify them there,
        #       not here
        self.repository = None
        self.filterPattern=""
        self.docdir="pydoc"
        self.docroot="Kamaelia"
        self.treeDepth=99
        self.tocDepth=99
        self.includeMethods=False
        self.includeModuleDocString=False
        self.includeNonKamaeliaStuff=False
        self.showComponentsOnIndices=False
        self.promoteModuleTitles=False
        self.deemphasiseTrails=False
        self.pageFooter=""
        self.testOutputDir=None
        self.testExtensions=[]

        
class docFormatter(object):
    """\
    docFormatter(renderer,config) -> new docFormatter object

    Object that formats documentation - methods of this class return document
    trees (docutils node format) documenting whatever was requested.

    Requires the renderer object so it can determine URIs for hyperlinks.
    """
    def __init__(self, renderer, config):
        super(docFormatter,self).__init__()
        self.renderer = renderer
        self.config = config
        self.errorCount=0

    uid = 0

    def genUniqueRef(self):
        uid = str(self.uid)
        self.uid+=1
        return uid

    def boxes(self,componentName, label, boxes):
        """\
        Format documentation for inboxes/outboxes. Returns a docutils document
        tree fragment.

        Keyword arguments:

        - componentName  -- name of the component the boxes belong to
        - label          -- typically "Inboxes" or "Outboxes"
        - boxes          -- dict containing (boxname, boxDescription) pairs
        """
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
                ids   = ["symbol-"+componentName+"."+label],
                names = ["symbol-"+componentName+"."+label],
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
        """
        Parses a doc string in ReStructuredText format and returns a docutils
        document tree fragment.

        Removes any innate indentation from the raw doc strings before parsing.
        Also captures any warnings generated by parsing and writes them to
        stdout, incrementing the self.errorCount flag.
        """
        if docstring is None:
            docstring = " "
        lines = docstring.split("\n")
        if len(lines)>1:
            line1 = textwrap.dedent(lines[0])
            rest = textwrap.dedent("\n".join(lines[1:]))
            docstring = line1+"\n"+rest
        else:
            docstring=textwrap.dedent(docstring)

        while len(docstring)>0 and docstring[0] == "\n":
            docstring = docstring[1:]
        while len(docstring)>0 and docstring[-1] == "\n":
            docstring = docstring[:-1]
            
        warningStream=StringIO.StringIO()
        overrides={"warning_stream":warningStream,"halt_level":99}
        docTree=core.publish_doctree(docstring,settings_overrides=overrides)
        warnings=warningStream.getvalue()
        if warnings:
            print "!!! Warnings detected:"
            print warnings
            self.errorCount+=1
        warningStream.close()
        
        return nodes.section('', *docTree.children)

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        docTree = nodes.section('') #self.emptyTree()
        
        methods = X.methods
        methods.sort()
        
        
        for method in methods:
            methodHead = method.name + "(" + method.argString + ")"
            
            docTree.append( nodes.section('',
                                ids   = ["symbol-"+X.name+"."+method.name],
                                names = ["symbol-"+X.name+"."+method.name],
                                * [ nodes.title('', methodHead) ]
                                  + self.docString(method.docString)
                            )
                          )

        return docTree

    def formatInheritedMethods(self,CLASS):
        docTree = nodes.section('')
        
        overrides = [method.name for method in CLASS.methods] # copy of list of existing method names

        for base in CLASS.allBasesInMethodResolutionOrder:
            baseName = base.fullPathName
            basePathFragments = baseName.split(".")
            baseModuleName = tuple(basePathFragments[:-1])
            if baseModuleName == tuple():
                baseModuleName = tuple(CLASS.module.split("."))
                baseName = ".".join(baseModuleName)+"."+baseName
            baseClassName = basePathFragments[-1]

            if base is not None:
                # work out which methods haven't been already overriden
                methodList = []
                for method in base.methods:
                    if method.name not in overrides:
                        overrides.append(method.name)
                        uri = self.renderer.makeURI(baseName,"symbol-"+baseClassName+"."+method.name)
                        methodList.append(nodes.list_item('',
                            nodes.paragraph('','',
                                nodes.reference('', nodes.Text(method.name), refuri=uri),
                                nodes.Text("(" + method.argString + ")"),
                                ),
                            )
                        )

                if len(methodList)>0:
                    docTree.append( nodes.section('',
                        nodes.title('', "Methods inherited from "+baseName+" :"),
                        nodes.bullet_list('', *methodList),
                        )
                    )

                        
        return docTree
                            

    def formatClassStatement(self, name, bases):
        return "class "+ name+"("+", ".join(bases)+")"
    
    def formatPrefabStatement(self, name):
        return "prefab: "+name
    
    def formatComponent(self, X):
        # no class bases available from repository scanner 
        CLASSNAME = self.formatClassStatement(X.name, X.bases) #X.__bases__)
        CLASSDOC = self.docString(X.docString)
        INBOXES = self.boxes(X.name,"Inboxes", X.inboxes)
        OUTBOXES = self.boxes(X.name,"Outboxes", X.outboxes)
        
        if self.config.includeMethods and len(X.methods):
            METHODS = [ nodes.section('',
                          nodes.title('', 'Methods defined here'),
                          boxright('',
                              nodes.paragraph('', '',
                                  nodes.strong('', nodes.Text("Warning!"))
                              ),
                              nodes.paragraph('', '',
                                  nodes.Text("You should be using the inbox/outbox interface, not these methods (except construction). This documentation is designed as a roadmap as to their functionalilty for maintainers and new component developers.")
                              ),
                          ),
                          * self.formatMethodDocStrings(X)
                        )
                      ]
        else:
            METHODS = []
            
        return \
                nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["symbol-"+X.name]) ]
                  + CLASSDOC
                  + [ INBOXES, OUTBOXES ]
                  + METHODS
                  + [ self.formatInheritedMethods(X) ]
                )
        
    def formatPrefab(self, X):
        CLASSNAME = self.formatPrefabStatement(X.name)
        CLASSDOC = self.docString(X.docString)
        
        return nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["symbol-"+X.name]) ]
                  + CLASSDOC
            )
        
    def formatFunction(self, X):
        functionHead = X.name + "(" + X.argString + ")"
        return nodes.section('',
                    ids   = ["symbol-"+X.name],
                    names = ["symbol-"+X.name],
                    * [ nodes.title('', functionHead) ]
                        + self.docString(X.docString)
                    )
                            

    def formatClass(self, X):
        # no class bases available from repository scanner 
        CLASSNAME = self.formatClassStatement(X.name, X.bases)

        if len(X.methods)>0:
            METHODS = [ nodes.section('',
                            nodes.title('', 'Methods defined here'),
                            * self.formatMethodDocStrings(X)
                        )
                      ]
        else:
            METHODS = []
        return \
                nodes.section('',
                    nodes.title('', CLASSNAME, ids=["class-"+X.name]),
                    self.docString(X.docString),
                    * METHODS + [self.formatInheritedMethods(X)]
                )
        
    def formatTests(self, moduleName):
        if not self.config.testOutputDir:
            return nodes.container('')
        else:
            docTree = nodes.container('')
            for (ext,heading) in self.config.testExtensions:
                filename = os.path.join(self.config.testOutputDir, moduleName+ext)
                try:
                    file=open(filename,"r")
                    itemlist = nodes.bullet_list()
                    foundSomething=False
                    for line in file.readlines():
                        line=line[:-1]   # strip of trailing newline
                        itemlist.append(nodes.list_item('',nodes.paragraph('',line)))
                        foundSomething=True
                    if foundSomething:
                        docTree.append(nodes.paragraph('', heading))
                        docTree.append(itemlist)
                    file.close()
                except IOError:
                    pass
            if len(docTree.children)>0:
                docTree.insert(0,nodes.title('', "Test documentation"))
            return docTree
    
    def formatTrail(self, moduleName):
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
                line.append(nodes.Text("."))
            URI = self.renderer.makeURI(accum)
            line.append( nodes.reference('', element, refuri=URI) )
            
            firstPass=False
        
        return trail

    def formatTrailAsTitle(self, moduleName):
        trailTree = self.formatTrail(moduleName)
        title = nodes.title('', '', *trailTree.children)
        if self.config.deemphasiseTrails:
            title = nodes.section('', title)

        return title
        
    def declarationsList(self, components, prefabs, classes, functions):
        uris = {}
        prefixes = {}
        postfixes = {}
        
        for component in components:
            fullname = component.module + "." + component.name
            uris[component.name] = self.renderer.makeURI(fullname)
            prefixes[component.name] = "component "
            postfixes[component.name] = ""
            
        for prefab in prefabs:
            fullname = prefab.module + "." + prefab.name
            uris[prefab.name] = self.renderer.makeURI(fullname)
            prefixes[prefab.name] = "prefab "
            postfixes[prefab.name] = ""
            
        for cls in classes:
            fullname = cls.module + "." + cls.name
            uris[cls.name] = self.renderer.makeURI(fullname)
            prefixes[cls.name] = "class "
            postfixes[cls.name] = ""
            
        for function in functions:
            fullname = function.module + "." + function.name
            uris[function.name] = self.renderer.makeURI(fullname)
            prefixes[function.name] = ""
            postfixes[function.name] = "("+function.argString+")"

        declNames = uris.keys()
        declNames.sort()
        
        return nodes.container('',
            nodes.bullet_list('',
                *[ nodes.list_item('',
                       nodes.paragraph('', '',
                         nodes.strong('', '',
                           nodes.Text(prefixes[NAME]),
                           nodes.reference('', NAME, refuri=uris[NAME])),
                           nodes.Text(postfixes[NAME]),
                         )
                       )
                   for NAME in declNames
                 ]
                )
            )

    def formatComponentPage(self,moduleName, component):
        return self.formatDeclarationPage(moduleName, self.formatComponent, component)
        
    def formatPrefabPage(self,moduleName, prefab):
        return self.formatDeclarationPage(moduleName, self.formatPrefab, prefab)
        
    def formatClassPage(self,moduleName, cls):
        return self.formatDeclarationPage(moduleName, self.formatClass, cls)
        
    def formatFunctionPage(self,moduleName, function):
        return self.formatDeclarationPage(moduleName, self.formatFunction, function)
        
    def formatDeclarationPage(self, name, method, arg):
        parentURI = self.renderer.makeURI(".".join(name.split(".")[:-1]))
        trailTitle = self.formatTrailAsTitle(name)
        
        declarationTree = method(arg)
        
        return nodes.section('',
            trailTitle,
            nodes.paragraph('', '',
                nodes.Text("For examples and more explanations, see the "),
                nodes.reference('', 'module level docs.', refuri=parentURI)
                ),
            nodes.transition(),
            nodes.section('', *declarationTree),
            )
           
    def formatModulePage(self, moduleName, module, components, prefabs, classes, functions):
        
        trailTitle = self.formatTrailAsTitle(moduleName)
        moduleTree = self.docString(module.docString, main=True)
        testsTree = self.formatTests(moduleName)
        while len(testsTree.children)>0:
            node=testsTree.children[0]
            testsTree.remove(node)
            moduleTree.append(node)
            
        
        if self.config.promoteModuleTitles and \
           len(moduleTree.children)>=1 and \
           isinstance(moduleTree.children[0], nodes.title):
            theTitle = moduleTree.children[0]
            moduleTree.remove(theTitle)
            promotedTitle = [ theTitle ]
        else:
            promotedTitle = []

        toc = self.buildTOC(moduleTree, depth=self.config.tocDepth)
        
        allDeclarations = []
        
        declarationTrees = {}
        for component in components:
            cTrail = self.formatTrail(moduleName+"."+component.name)
            declarationTrees[component.name] = nodes.container('',
                nodes.title('','', *cTrail.children),
                    self.formatComponent(component)
            )
            
        for prefab in prefabs:
            assert(prefab.name not in declarationTrees)
            pTrail = self.formatTrail(moduleName+"."+prefab.name)
            declarationTrees[prefab.name] = nodes.container('',
                nodes.title('','', *pTrail.children),
                    self.formatPrefab(prefab)
            )

        for cls in classes:
            assert(cls.name not in declarationTrees)
            cTrail = self.formatTrail(moduleName+"."+cls.name)
            declarationTrees[cls.name] = nodes.container('',
                nodes.title('','', *cTrail.children),
                    self.formatClass(cls)
            )

        for function in functions:
            assert(function.name not in declarationTrees)
            fTrail = self.formatTrail(moduleName+"."+function.name)
            declarationTrees[function.name] = nodes.container('',
                nodes.title('','', *fTrail.children),
                    self.formatFunction(function)
            )

        declNames = declarationTrees.keys()
        declNames.sort()
        for name in declNames:
            allDeclarations.extend(declarationTrees[name])
        
        componentListTree = self.declarationsList( components, prefabs, classes, functions )

        return nodes.container('',
            nodes.section('',
                trailTitle,
                ),
            nodes.section('',
                * promotedTitle + \
                  [ componentListTree,
                    toc,
                  ]
            ),
            nodes.transition(),
            moduleTree,
            nodes.transition(),
            nodes.section('', *allDeclarations),
            )
            
    def buildTOC(self, srcTree, parent=None, depth=None):
        """Recurse through a source document tree, building a table of contents"""
        if parent is None:
            parent = nodes.bullet_list()

        if depth==None:
            depth=self.config.tocDepth
            
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

        # go through parent promoting any doubly nested bullet_lists
        for item in parent.children:
            if isinstance(item.children[0], nodes.bullet_list):
                sublist = item.children[0]
                for subitem in sublist.children[:]:   # copy it so it isn't corrupted by what we're about to do
                    sublist.remove(subitem)
                    item.parent.insert(item.parent.index(item), subitem)
                parent.remove(item)
                
            
        return parent
        

    def formatIndexPage(self, path, subTree): #indexName, subTree, componentsAndPrefabs):
        depth=self.config.treeDepth

        indexName = ".".join(path)

        trailTitle = self.formatTrailAsTitle(indexName)
        
        moduleTree = nodes.container('')
        if self.config.includeModuleDocString:
            if subTree.has_key("__init__"):
                docs = subTree["__init__"].docString
                if docs and ("This is a doc string" not in docs):
                    moduleTree =self.docString(docs)

        if self.config.promoteModuleTitles and \
           len(moduleTree.children)>=1 and \
           isinstance(moduleTree.children[0], nodes.title):
            theTitle = moduleTree.children[0]
            moduleTree.remove(theTitle)
            promotedTitle = [ theTitle ]
        else:
            promotedTitle = []

        return nodes.section('',
            * [ trailTitle ]
            + promotedTitle
            + [ self.generateIndex(path, subTree, depth=depth) ]
            + [ moduleTree ]
            )

    def generateIndex(self, path, srcTree, parent=None, depth=99):
        if parent is None:
            parent = nodes.bullet_list()

        if depth<=0:
            return parent

        items=nodes.section()

        childNames = srcTree.keys()
        childNames.sort()
        for name in [c for c in childNames if c != "__init__"]:
            moduleContents = []
            
            modPath = tuple(list(path)+[name])
            modName = ".".join(modPath)

            if self.config.repository.flatModules.has_key(modPath):
                thisMod = self.config.repository.flatModules[modPath]
                
                # build "(a,b,c)" style list of links to actual components/prefabs in the module
                # (if they exist)
                if self.config.showComponentsOnIndices:
                    declNames = [_.name for _ in thisMod.components + thisMod.prefabs]
                    if len(declNames)>0:
                        moduleContents.append(nodes.Text(" ( "))
                        first=True
                        for declName in declNames:
                            if not first:
                                moduleContents.append(nodes.Text(", "))
                            first=False
                            uri = self.renderer.makeURI(modName+"."+declName)
                            linkToDecl = nodes.reference('', nodes.Text(declName), refuri=uri)
                            moduleContents.append(linkToDecl)
                        moduleContents.append(nodes.Text(" )"))

            # now make the list item for this module
            uri = self.renderer.makeURI(modName)
            text = name
            newItem = nodes.list_item('',
                nodes.paragraph('','',
                    nodes.strong('', '',nodes.reference('', text, refuri=uri)),
                    *moduleContents
                    )
                )
                
            if isinstance(srcTree[name],dict):  # if not empty, recurse
                newItem.append(nodes.bullet_list())
                self.generateIndex(modPath, srcTree[name], newItem[-1], depth-1)
            parent.append(newItem)

        return parent



            
def generateDocumentationFiles(formatter, CONFIG):
    
    MODULES = [ K for K in CONFIG.repository.flatModules.keys() \
                if CONFIG.filterPattern in ".".join(K) ]
    for MODULE in MODULES:
        moduleName = ".".join(MODULE)
        print "Processing: "+moduleName

        module     = CONFIG.repository.flatModules[MODULE]
        components = module.components
        prefabs    = module.prefabs
        if CONFIG.includeNonKamaeliaStuff:
            classes    = module.classes
            functions  = module.functions
        else:
            classes = []
            functions = []
        
        doctree  = formatter.formatModulePage(moduleName, module, components, prefabs, classes, functions)
        filename = formatter.renderer.makeFilename(moduleName)
        output   = formatter.renderer.render(moduleName, doctree)
        
        F = open(CONFIG.docdir+"/"+filename, "w")
        F.write(output)
        F.close()
        
        for component in components:
            NAME = moduleName+"."+component.name
            print "    Component: "+NAME
            filename = formatter.renderer.makeFilename(NAME)
            doctree = formatter.formatComponentPage(NAME, component)
            output   = formatter.renderer.render(NAME, doctree)
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()

        for prefab in prefabs:
            NAME = moduleName+"."+prefab.name
            print "    Prefab: "+NAME
            filename = formatter.renderer.makeFilename(NAME)
            doctree = formatter.formatPrefabPage(NAME, prefab)
            output   = formatter.renderer.render(NAME, doctree)
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()
            
        for cls in classes:
            NAME = moduleName+"."+cls.name
            filename = formatter.renderer.makeFilename(NAME)
            doctree = formatter.formatClassPage(NAME, cls)
            output = formatter.renderer.render(NAME, doctree)
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()

        for function in functions:
            NAME = moduleName+"."+function.name
            filename = formatter.renderer.makeFilename(NAME)
            doctree = formatter.formatFunctionPage(NAME, function)
            output = formatter.renderer.render(NAME, doctree)
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()

def generateIndices(formatter, CONFIG):

    def generate(formatter, CONFIG, subtree, path):
        if path != []:
            indexName = ".".join(path)
            print "Creating index: "+indexName
            
            doctree  = formatter.formatIndexPage(path,subtree)
            filename = formatter.renderer.makeFilename(indexName)
            output   = formatter.renderer.render(indexName, doctree)
            
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()
        
        for (name,leaf) in subtree.items():
            if isinstance(leaf, dict):
                generate(formatter, CONFIG, leaf, path+[name])
            else:
                # must be module documentation object
                pass

    generate(formatter, CONFIG, CONFIG.repository.nestedModules, [])
    

    
    
if __name__ == "__main__":
    import sys
    
    config = DocGenConfig()
    config.docdir     = "pydoc"
    config.treeDepth=99
    config.tocDepth=3
    config.includeMethods=True
    config.includeModuleDocString=True
    config.showComponentsOnIndices=True
        

    urlPrefix=""

    cmdLineArgs = []

    for arg in sys.argv[1:]:
        if arg[:2] == "--" and len(arg)>2:
            cmdLineArgs.append(arg.lower())
        else:
            cmdLineArgs.append(arg)
    
    if not cmdLineArgs or "--help" in cmdLineArgs or "-h" in cmdLineArgs:
        sys.stderr.write("\n".join([
            "Usage:",
            "",
            "    "+sys.argv[0]+" <arguments - see below>",
            "",
            "Only <repository dir> is mandatory, all other arguments are optional.",
            "",
            "    --help               Display this help message",
            "",
            "    --filter <substr>    Only build docs for components/prefabs for components",
            "                         or modules who's full path contains <substr>",
            "",
            "    --urlprefix <prefix> Prefix for URLs - eg. a base dir: '/Components/pydoc/",
            "                         (remember the trailing slash if you want one)",
            "",
            "    --outdir <dir>       Directory to put output into (default is 'pydoc')",
            "                         directory must already exist (and be emptied)",
            "",
            "    --root <moduleRoot>  The module path leading up to the repositoryDir specified",
            "                         eg. Kamaelia.File, if repositoryDir='.../Kamaelia/File/'",
            "                         default='Kamaelia'",
            "",
            "    --notjustcomponents  Will generate documentation for classes and functions too",
            "",
            "    --footerinclude <file> A directive will be included to specify '<file>'",
            "                           as an include at the bottom of all pages.",
            "",
            "    --promotetitles      Promote module level doc string titles to top of pages",
            "                         generated. Also causes breadcrumb trails at the top of",
            "                         pages to be reduced in emphasis slightly, so the title",
            "                         properly stands out",
            "",
            "    --indexdepth         Depth (nesting levels) of indexes on non-module pages.",
            "                         Use 0 to suppress index all together",
            "",
            "    --includeTestOutput <dir> Incorporate test suite output",
            "                        as found in the specified directory.",
            "",
            "    <repositoryDir>      Use Kamaelia modules here instead of the installed ones",
            "",
            "",
        ]))
        sys.exit(0)

    try:
        if "--filter" in cmdLineArgs:
            index = cmdLineArgs.index("--filter")
            config.filterPattern = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]

        if "--urlprefix" in cmdLineArgs:
            index = cmdLineArgs.index("--urlprefix")
            urlPrefix = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        if "--outdir" in cmdLineArgs:
            index = cmdLineArgs.index("--outdir")
            config.docdir = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        if "--root" in cmdLineArgs:
            index = cmdLineArgs.index("--root")
            config.docroot = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        if "--notjustcomponents" in cmdLineArgs:
            index = cmdLineArgs.index("--notjustcomponents")
            config.includeNonKamaeliaStuff=True
            del cmdLineArgs[index]

        if "--promotetitles" in cmdLineArgs:
            index = cmdLineArgs.index("--promotetitles")
            config.promoteModuleTitles=True
            config.deemphasiseTrails=True
            del cmdLineArgs[index]

        if "--footerinclude" in cmdLineArgs:
            index = cmdLineArgs.index("--footerinclude")
            location=cmdLineArgs[index+1]
            config.pageFooter = "\n[[include][file="+location+"]]\n"
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]

        if "--indexdepth" in cmdLineArgs:
            index = cmdLineArgs.index("--indexdepth")
            config.treeDepth = int(cmdLineArgs[index+1])
            assert(config.treeDepth >= 0)
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        if "--includetestoutput" in cmdLineArgs:
            index = cmdLineArgs.index("--includetestoutput")
            config.testOutputDir = cmdLineArgs[index+1]
            config.testExtensions = [("...ok","Tests passed:"),("...fail","Tests failed:")]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]

        if len(cmdLineArgs)==1:
            REPOSITORYDIR = cmdLineArgs[0]
        elif len(cmdLineArgs)==0:
            REPOSITORYDIR = None
        else:
            raise
    except:
        sys.stderr.write("\n".join([
            "Error in command line arguments.",
            "Run with '--help' for info on command line arguments.",
            "",
            "",
        ]))
        sys.exit(1)
    
    sys.argv=sys.argv[0:0]
        
    debug = False
    REPOSITORY = Repository.SourceTreeDocs(baseDir=REPOSITORYDIR,rootName=config.docroot)
    config.repository=REPOSITORY
    
    import time
    theTime=time.strftime("%d %b %Y at %H:%M:%S UTC/GMT", time.gmtime())
    config.pageFooter += "\n<p><i>-- Automatic documentation generator, "+theTime+"</i>\n"

    renderer = RenderHTML(titlePrefix="Kamaelia docs : ",
                          urlPrefix=urlPrefix,
                          debug=False,
                          rawFooter=config.pageFooter)
    
    if 1:
        # automatically generate crosslinks when component names are seen
        crossLinks = {}
        for (path,m) in REPOSITORY.flatModules.items():
            items = m.components + m.prefabs
            if config.includeNonKamaeliaStuff:
                items += m.classes + m.functions
            for item in items:
                name=".".join(path)
                crossLinks[name] = name
                name=".".join(list(path)+[item.name])
                crossLinks[name] = name
        renderer.setAutoCrossLinks( crossLinks )
    
    formatter = docFormatter(renderer, config=config)

    generateDocumentationFiles(formatter,config)
    generateIndices(formatter,config)

    if formatter.errorCount>0:
        print "Errors occurred during docstring parsing/page generation."
        sys.exit(2)
    else:
        sys.exit(0)
        