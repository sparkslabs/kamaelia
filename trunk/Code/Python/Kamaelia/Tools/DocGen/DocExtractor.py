#!/usr/bin/python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

* can dump symbols (with mappings to URLs) to a file and/or read them in. This
  makes it possible to cross-link, for example, from the Kamaelia documentation
  back to the Axon documentation.

*This is not an Axon/Kamaelia system* - it is not built from components. However
it is probably sufficiently useful to be classified as a 'tool'!



Usage
-----

For help on command line options, use the ``--help`` option::

    $> ./DocExtractor.py --help

The command lines currently being used to generate Kamaelia and Axon
documentation are as follows:

For Axon docs for the website::

    $> ./DocExtractor.py --urlprefix /Docs/Axon/                       \
                         --promotetitles                               \
                         --notjustcomponents                           \
                         --indexdepth 0                                \
                         --root Axon                                   \
                         --footerinclude Docs/Axon-footer.html         \
                         --outdir <outputDirName>                      \
                         --dumpSymbolsTo <symbolFile>                  \
                         <repositoryDir> 

For Kamaelia component docs for the website::

    $> ./DocExtractor.py --urlprefix /Components/pydoc/                \
                         --root Kamaelia                               \
                         --footerinclude Components/pydoc-footer.html  \
                         --outdir <outputDirName>                      \
                         --linkToSymbols <symbolFile>                  \
                         <repositoryDir> 

Why differences?

* The ``--notjustcomponents`` flag which ensures that the classes and functions
  making up Axon are documented.
  
* the ``--dumpSymbolsTo`` option creates a dump of all symbols documented.
  ``--linkToSymbols`` reads them in for generating crosslinks.

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
import ConfigParser
from docutils import core
from docutils import nodes
from Kamaelia.Support.Data import Repository

ClassScope    = Repository.ClassScope
FunctionScope = Repository.FunctionScope
ModuleScope   = Repository.ModuleScope
ImportScope   = Repository.ImportScope

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
        self.dumpSymbolsTo=None
        self.loadSymbolsFrom=[]

        
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
            print "Offending docstring:"
            print '"""'
            print docstring
            print '"""'
        warningStream.close()
        
        return nodes.section('', *docTree.children)

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,className,X):
        docTree = nodes.section('')
        
        methods = X.listAllFunctions()
        methods.sort()
        
        
        for (methodname,method) in methods:
            methodHead = methodname + "(" + method.argString + ")"
            
            docTree.append( nodes.section('',
                                ids   = ["symbol-"+className+"."+methodname],
                                names = ["symbol-"+className+"."+methodname],
                                * [ nodes.title('', methodHead) ]
                                  + self.docString(method.doc)
                            )
                          )

        return docTree

    def formatInheritedMethods(self,className,CLASS):
        docTree = nodes.section('')
        
        overrides = [name for (name,method) in CLASS.listAllFunctions()] # copy of list of existing method names
        for base in CLASS.allBasesInMethodResolutionOrder:
            if isinstance(base,ClassScope):
                moduleName=base.module
                findName=moduleName[len(self.config.docroot+"."):]
                module=self.config.repository.find(findName)
                try:
                    className=module.locate(base)
                except ValueError:
                    continue
                
                # work out which methods haven't been already overriden
                methodList = []
                for (name,method) in base.listAllFunctions():
                    if name not in overrides:
                        overrides.append(name)
                        uri = self.renderer.makeURI(moduleName,"symbol-"+className+"."+name)
                        methodList.append(nodes.list_item('',
                            nodes.paragraph('','',
                                nodes.reference('', nodes.Text(name), refuri=uri),
                                nodes.Text("(" + method.argString + ")"),
                                ),
                            )
                        )

                if len(methodList)>0:
                    docTree.append( nodes.section('',
                        nodes.title('', "Methods inherited from "+moduleName+"."+className+" :"),
                        nodes.bullet_list('', *methodList),
                        )
                    )

                        
        return docTree
                            

    def formatClassStatement(self, name, bases):
        baseNames=[]
        for baseName,base in bases:
            baseNames.append(baseName)
        return "class "+ name+"("+", ".join(baseNames)+")"
    
    def formatPrefabStatement(self, name):
        return "prefab: "+name
    
    def formatComponent(self, moduleName, name, X):
        # no class bases available from repository scanner 
        CLASSNAME = self.formatClassStatement(name, X.bases)
        CLASSDOC = self.docString(X.doc)
        INBOXES = self.boxes(name,"Inboxes", X.inboxes)
        OUTBOXES = self.boxes(name,"Outboxes", X.outboxes)
        
        if self.config.includeMethods and len(X.listAllFunctions()):
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
                          * self.formatMethodDocStrings(name,X)
                        )
                      ]
        else:
            METHODS = []

        return \
                nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["symbol-"+name]) ]
                  + CLASSDOC
                  + [ INBOXES, OUTBOXES ]
                  + METHODS
                  + [ self.formatInheritedMethods(name,X) ]
                )
        
    def formatPrefab(self, moduleName, name, X):
        CLASSNAME = self.formatPrefabStatement(name)
        CLASSDOC = self.docString(X.doc)
        
        return nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["symbol-"+name]) ]
                  + CLASSDOC
            )
        
    def formatFunction(self, moduleName, name, X):
        functionHead = name + "(" + X.argString + ")"
        return nodes.section('',
                    ids   = ["symbol-"+name],
                    names = ["symbol-"+name],
                    * [ nodes.title('', functionHead) ]
                        + self.docString(X.doc)
                    )
                            

    def formatClass(self, moduleName, name, X):
        CLASSNAME = self.formatClassStatement(name, X.bases)

        if len(X.listAllFunctions()):
            METHODS = [ nodes.section('',
                            nodes.title('', 'Methods defined here'),
                            * self.formatMethodDocStrings(name,X)
                        )
                      ]
        else:
            METHODS = []
        return \
                nodes.section('',
                    nodes.title('', CLASSNAME, ids=["symbol-"+name]),
                    self.docString(X.doc),
                    * METHODS + [self.formatInheritedMethods(name,X)]
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
    
    def formatTrail(self, fullPathName):
        path = fullPathName.split(".")
        
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

    def formatTrailAsTitle(self, fullPathName):
        trailTree = self.formatTrail(fullPathName)
        title = nodes.title('', '', *trailTree.children)
        if self.config.deemphasiseTrails:
            title = nodes.section('', title)

        return title
        
    def declarationsList(self, moduleName, components, prefabs, classes, functions):
        uris = {}
        prefixes = {}
        postfixes = {}
        
        for (name,component) in components:
            uris[name] = self.renderer.makeURI(moduleName+"."+name)
            prefixes[name] = "component "
            postfixes[name] = ""
            
        for (name,prefab) in prefabs:
            uris[name] = self.renderer.makeURI(moduleName+"."+name)
            prefixes[name] = "prefab "
            postfixes[name] = ""
            
        for (name,cls) in classes:
            uris[name] = self.renderer.makeURI(moduleName+"."+name)
            prefixes[name] = "class "
            postfixes[name] = ""
            
        for (name,function) in functions:
            uris[name] = self.renderer.makeURI(moduleName+"."+name)
            prefixes[name] = ""
            postfixes[name] = "("+function.argString+")"

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

    def formatComponentPage(self, moduleName, name, component):
        return self.formatDeclarationPage(moduleName, name, self.formatComponent, component)
        
    def formatPrefabPage(self, moduleName, name, prefab):
        return self.formatDeclarationPage(moduleName, name, self.formatPrefab, prefab)
        
    def formatClassPage(self, moduleName, name, cls):
        return self.formatDeclarationPage(moduleName, name, self.formatClass, cls)
        
    def formatFunctionPage(self, moduleName, name, function):
        return self.formatDeclarationPage(moduleName, name, self.formatFunction, function)
        
    def formatDeclarationPage(self, moduleName, name, method, item):
        parentURI = self.renderer.makeURI(item.module)
        trailTitle = self.formatTrailAsTitle(moduleName+"."+name)
        
        itemDocTree = method(moduleName, name, item)
        
        return nodes.section('',
            trailTitle,
            nodes.paragraph('', '',
                nodes.Text("For examples and more explanations, see the "),
                nodes.reference('', 'module level docs.', refuri=parentURI)
                ),
            nodes.transition(),
            nodes.section('', *itemDocTree),
            )
           
    def formatModulePage(self, moduleName, module, components, prefabs, classes, functions):
        
        trailTitle = self.formatTrailAsTitle(moduleName)
        moduleDocTree = self.docString(module.doc, main=True)
        testsTree = self.formatTests(moduleName)
        while len(testsTree.children)>0:
            node=testsTree.children[0]
            testsTree.remove(node)
            moduleDocTree.append(node)
            
        
        if self.config.promoteModuleTitles and \
           len(moduleDocTree.children)>=1 and \
           isinstance(moduleDocTree.children[0], nodes.title):
            theTitle = moduleDocTree.children[0]
            moduleDocTree.remove(theTitle)
            promotedTitle = [ theTitle ]
        else:
            promotedTitle = []

        toc = self.buildTOC(moduleDocTree, depth=self.config.tocDepth)
        
        allDeclarations = []
        
        declarationTrees = []
        for (name,component) in components:
            cTrail = self.formatTrail(moduleName+"."+name)
            declarationTrees.append((
                name,
                nodes.container('',
                    nodes.title('','', *cTrail.children),
                    self.formatComponent(moduleName,name,component)
                    )
                 ))
            
        for (name,prefab) in prefabs:
            pTrail = self.formatTrail(moduleName+"."+name)
            declarationTrees.append((
                name,
                nodes.container('',
                    nodes.title('','', *pTrail.children),
                    self.formatPrefab(moduleName,name,prefab)
                    )
                ))

        for (name,cls) in classes:
            cTrail = self.formatTrail(moduleName+"."+name)
            declarationTrees.append((
                name,
                nodes.container('',
                nodes.title('','', *cTrail.children),
                    self.formatClass(moduleName,name,cls)
                    )
                ))

        for (name,function) in functions:
            fTrail = self.formatTrail(moduleName+"."+name)
            declarationTrees.append((
                name,
                nodes.container('',
                    nodes.title('','', *fTrail.children),
                    self.formatFunction(moduleName,name,function)
                    )
                ))

        declarationTrees.sort()   # sort by name
        concatenatedDeclarations=[]
        for (name,tree) in declarationTrees:
            concatenatedDeclarations.extend(tree)
        
        componentListTree = self.declarationsList( moduleName, components, prefabs, classes, functions )
        
        if len(module.listAllModules()) > 0:
            subModuleIndex = self.generateIndex(moduleName,module,self.config.treeDepth)
        else:
            subModuleIndex = []
        return nodes.container('',
            nodes.section('',
                trailTitle,
                ),
             nodes.section('',
                 * promotedTitle + \
                   [ componentListTree] + \
                   subModuleIndex + \
                   [ toc ]
             ),
             moduleDocTree,
             nodes.transition(),
             nodes.section('', *concatenatedDeclarations),
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
        

    def generateIndex(self, pathToHere, module, depth=99):
        if depth<=0:
            return []
        
        tree=[]
        children = module.listAllModules()
        children.sort()
        
        if pathToHere!="":
            pathToHere=pathToHere+"."
        
        for subModuleName,submodule in children:
            moduleContents=[]
            
            if self.config.showComponentsOnIndices:
                moduleContains=[name for (name,item) in submodule.listAllComponentsAndPrefabs()]
                if len(moduleContains)>0:
                    moduleContains.sort()
                    moduleContents.append(nodes.Text(" ( "))
                    first=True
                    for name in moduleContains:
                        if not first:
                            moduleContents.append(nodes.Text(", "))
                        first=False
                        uri = self.renderer.makeURI(pathToHere+subModuleName+"."+name)
                        linkToDecl = nodes.reference('', nodes.Text(name), refuri=uri)
                        moduleContents.append(linkToDecl)
                    moduleContents.append(nodes.Text(" )"))
            
            uri=self.renderer.makeURI(pathToHere+subModuleName)
            tree.append( nodes.list_item('',
                nodes.paragraph('','',
                    nodes.strong('', '',nodes.reference('', subModuleName, refuri=uri)),
                    *moduleContents
                ),
                *self.generateIndex(pathToHere+subModuleName, submodule,depth-1)
            ) )

        if len(tree):
            return [ nodes.bullet_list('', *tree) ]
        else:
            return []




            
def generateDocumentationFiles(formatter, CONFIG):
    for (moduleName,module) in CONFIG.repository.listAllModulesIncSubModules():
        
        print "Processing: "+moduleName
        
        components=module.listAllComponents()
        prefabs=module.listAllPrefabs()

        if CONFIG.includeNonKamaeliaStuff:
            classes    = [X for X in module.listAllClasses() if X not in components]
            functions  = [X for X in module.listAllFunctions() if X not in prefabs]
        else:
            classes = []
            functions = []
        
        if CONFIG.filterPattern in moduleName:
            doctree  = formatter.formatModulePage(moduleName, module, components, prefabs, classes, functions)
            filename = formatter.renderer.makeFilename(moduleName)
            output   = formatter.renderer.render(moduleName, doctree)
            
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()
        
        for (name,component) in components:
            NAME=moduleName+"."+name
            if CONFIG.filterPattern in NAME:
                print "    Component: "+NAME
                filename = formatter.renderer.makeFilename(NAME)
                doctree = formatter.formatComponentPage(moduleName, name, component)
                output   = formatter.renderer.render(NAME, doctree)
                F = open(CONFIG.docdir+"/"+filename, "w")
                F.write(output)
                F.close()

        for (name,prefab) in prefabs:
            NAME=moduleName+"."+name
            if CONFIG.filterPattern in NAME:
                print "    Prefab: "+NAME
                filename = formatter.renderer.makeFilename(NAME)
                doctree = formatter.formatPrefabPage(moduleName, name, prefab)
                output   = formatter.renderer.render(NAME, doctree)
                F = open(CONFIG.docdir+"/"+filename, "w")
                F.write(output)
                F.close()
            
        for (name,cls) in classes:
            NAME=moduleName+"."+name
            if CONFIG.filterPattern in NAME:
                print "    Class: "+NAME
                filename = formatter.renderer.makeFilename(NAME)
                doctree = formatter.formatClassPage(moduleName, name, cls)
                output = formatter.renderer.render(NAME, doctree)
                F = open(CONFIG.docdir+"/"+filename, "w")
                F.write(output)
                F.close()

        for (name,function) in functions:
            NAME=moduleName+"."+name
            if CONFIG.filterPattern in NAME:
                print "    Function: "+NAME
                filename = formatter.renderer.makeFilename(NAME)
                doctree = formatter.formatFunctionPage(moduleName, name, function)
                output = formatter.renderer.render(NAME, doctree)
                F = open(CONFIG.docdir+"/"+filename, "w")
                F.write(output)
                F.close()


def dumpSymbols(makeURI, CONFIG, filename, theTime="", cmdLineArgs=[]):
    """\
    Dumps symbols from the repository to a text file - classes, functions, prefabs,
    components and modules. Includes, for each, the URL for the corresponding
    piece of generated documentation.
    
    This data can therefore be read in by another documentation build to allow
    cross links to be generated.
    
    Arguments:
    
    - makeURI      -- function for transforming symbols to the corresponding URI they should map to
    - CONFIG       -- configuration object
    - filename     -- filename to dump to
    - theTime      -- Optional. String describing the time of this documentation build.
    - cmdLineArgs  -- Optional. The command line args used to invoke this build.
    """
    print "Dumping symbols to file '"+filename+"' ..."
    F=open(filename,"wb")
    F.write(";\n")
    F.write("; Kamaelia documentation extractor symbol dump\n")
    if theTime:
        F.write("; (generated on "+theTime+" )\n")
    if cmdLineArgs:
        F.write(";\n")
        F.write("; Command line args for build were:\n")
        F.write(";      "+" ".join(cmdLineArgs)+"\n")
    F.write(";\n")
    F.write("\n")
    cfg=ConfigParser.ConfigParser()
    cfg.optionxform = str  # make case sensitive
    
    cfg.add_section("COMPONENTS")
    cfg.add_section("PREFABS")
    cfg.add_section("CLASSES")
    cfg.add_section("FUNCTIONS")
    cfg.add_section("MODULES")
    
    for (moduleName,module) in CONFIG.repository.listAllModulesIncSubModules():
        uri=makeURI(moduleName)
        cfg.set("MODULES", option=moduleName, value=uri)
        
        components=module.listAllComponents()
        prefabs=module.listAllPrefabs()

        if CONFIG.includeNonKamaeliaStuff:
            classes    = [X for X in module.listAllClasses() if X not in components]
            functions  = [X for X in module.listAllFunctions() if X not in prefabs]
        else:
            classes = []
            functions = []
            
        for (name,item) in classes:
            NAME=moduleName+"."+name
            URI=makeURI(NAME)
            cfg.set("CLASSES", option=NAME, value=URI)
            
        for (name,item) in prefabs:
            NAME=moduleName+"."+name
            URI=makeURI(NAME)
            cfg.set("PREFABS", option=NAME, value=URI)
            
        for (name,item) in components:
            NAME=moduleName+"."+name
            URI=makeURI(NAME)
            cfg.set("COMPONENTS", option=NAME, value=URI)
            
        for (name,item) in functions:
            NAME=moduleName+"."+name
            URI=makeURI(NAME)
            cfg.set("FUNCTIONS", option=NAME, value=URI)
            
    cfg.write(F)
    F.close()
    
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
            "    --dumpSymbolsTo <file> Dumps catalogue of major symbols (classes, components, ",
            "                           prefabs, functions) to the specified file, along with",
            "                           the URLs they map to.",
            "",
            "    --linkToSymbols <file> Read symbols from the specified file and automatically",
            "                           link any references to those symbols to the respective",
            "                           URLs defined in the symbol file.",
            "                           Repeat this option for every symbol file to be read in.",
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
            
        if "--dumpsymbolsto" in cmdLineArgs:
            index = cmdLineArgs.index("--dumpsymbolsto")
            config.dumpSymbolsTo = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        while "--linktosymbols" in cmdLineArgs:
            index = cmdLineArgs.index("--linktosymbols")
            config.loadSymbolsFrom.append(cmdLineArgs[index+1])
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
    
    args=sys.argv
    sys.argv=sys.argv[0:0]
        
    debug = False
    REPOSITORY=Repository.ModuleDoc( moduleName=config.docroot,
                                     filePath=REPOSITORYDIR,
                                     localModules={},
                                   )
    REPOSITORY.resolve(roots={config.docroot:REPOSITORY})
    config.repository=REPOSITORY
    
    import time
    theTime=time.strftime("%d %b %Y at %H:%M:%S UTC/GMT", time.gmtime())
    config.pageFooter += "\n<p><i>-- Automatic documentation generator, "+theTime+"</i>\n"

    renderer = RenderHTML(titlePrefix="Kamaelia docs : ",
                          urlPrefix=urlPrefix,
                          debug=False,
                          rawFooter=config.pageFooter)
    
    # automatically generate crosslinks when component names are seen
    crossLinks = {}
    wantedTypes=(ClassScope,FunctionScope,ModuleScope,)
    for (fullPathName,item) in REPOSITORY.listAllMatching(recurseDepth=99,noRecurseTypes=ImportScope,types=wantedTypes):
        if config.includeNonKamaeliaStuff \
        or isinstance(item,ModuleScope) \
        or getattr(item,"isComponent",False) \
        or getattr(item,"isPrefab",False):
            fullPathName = REPOSITORY.module+"."+fullPathName
            crossLinks[fullPathName] = fullPathName
            
    renderer.setAutoCrossLinks( crossLinks )
    
    # also add crosslinks for any referenced external files of symbols
    for filename in config.loadSymbolsFrom:
        print "Reading symbol links from '%s' ..." % filename
        cfg=ConfigParser.ConfigParser()
        cfg.optionxform = str  # make case sensitive
        if not os.path.isfile(filename):
            raise RuntimeError("Could not find symbol file: "+filename)
        cfg.read(filename)                                     # not checking retval for python 2.3 compatibility
        renderer.addAutoLinksToURI(dict(cfg.items("CLASSES")))
        renderer.addAutoLinksToURI(dict(cfg.items("FUNCTIONS")))
        renderer.addAutoLinksToURI(dict(cfg.items("COMPONENTS")))
        renderer.addAutoLinksToURI(dict(cfg.items("PREFABS")))
        renderer.addAutoLinksToURI(dict(cfg.items("MODULES")))
    
    formatter = docFormatter(renderer, config=config)

    generateDocumentationFiles(formatter,config)

    if config.dumpSymbolsTo is not None:
        dumpSymbols(formatter.renderer.makeURI, config, config.dumpSymbolsTo, theTime, args)

    if formatter.errorCount>0:
        print "Errors occurred during docstring parsing/page generation."
        sys.exit(2)
    else:
        sys.exit(0)
        