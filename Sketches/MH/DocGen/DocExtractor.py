#!/usr/bin/python
#
# This program generates Kamaelia's documentation directly from the
# source. I am currently running this as follows:
#
# mkdir ./pydoc/
# ./DocExtractor.py
#
# documentation is placed into the "pydoc" subdirectory

import textwrap
import inspect
import pprint
import time
from docutils import core
from docutils import nodes
#import Kamaelia.Support.Data.Repository
import Repository


from renderHTML      import RenderHTML
from renderPlaintext import RenderPlaintext

from Nodes import boxright

class DocGenConfig(object):
    """Configuration object for documentation generation."""
    def __init__(self):
        super(DocGenConfig,self).__init__()
        # NOTE: These settings are overridden in __main__ - modify them there,
        #       not here
        self.repository = None
        self.debug=False
        self.filterPattern=""
        self.docdir="pydoc"
        self.treeDepth=99
        self.tocDepth=99
        self.includeMethods=False
        self.includeModuleDocString=False
        self.showComponentsOnIndices=False

class docFormatter(object):
    def __init__(self, renderer=RenderPlaintext, config=DocGenConfig(), debug=False):
        super(docFormatter,self).__init__()
        self.renderer = renderer
        self.debug = debug
        self.config = config

    uid = 0

    def genUniqueRef(self):
        uid = str(self.uid)
        self.uid+=1
        return uid

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
            
        return nodes.section('', *core.publish_doctree(docstring).children)

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        docTree = nodes.section('') #self.emptyTree()
        
        methods = X.methods
        methods.sort()
        
        
        for method in methods:
            methodHead = method.name + "(" + method.argString + ")"
            
            docTree.append( nodes.section('',
                                ids   = ["component-"+X.name+"-method-"+method.name],
                                names = ["component-"+X.name+"-method-"+method.name],
                                * [ nodes.title('', methodHead) ]
                                  + self.docString(method.docString)
                            )
                          )

        return docTree

    def formatClassStatement(self, name, bases):
        return "class "+ name+"("+",".join([str(base)[8:-2] for base in bases])+")"
    
    def formatPrefabStatement(self, name):
        return "prefab: "+name

    def formatComponent(self, X):
        # no class bases available from repository scanner 
        CLASSNAME = self.formatClassStatement(X.name, []) #X.__bases__)
        CLASSDOC = self.docString(X.docString)
        INBOXES = self.boxes(X.name,"Inboxes", X.inboxes)
        OUTBOXES = self.boxes(X.name,"Outboxes", X.outboxes)
        
        if self.config.includeMethods:
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
            
        trailTree = self.formatTrail(X.module+"."+X.name)

        return \
                nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["component-"+X.name]) ]
                  + CLASSDOC
                  + [ INBOXES, OUTBOXES ]
                  + METHODS
                )
        
    def formatPrefab(self, X):
        CLASSNAME = self.formatPrefabStatement(X.name)
        CLASSDOC = self.docString(X.docString)
        
        return nodes.container('',
                * [ nodes.title('', CLASSNAME, ids=["component-"+X.name]) ]
                  + CLASSDOC
            )
        
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
    
    def componentList(self, components):
        uris = {}
        for component in components:
            fullname = component.module + "." + component.name
            uris[component.name] = self.renderer.makeURI(fullname)

        componentNames = uris.keys()
        componentNames.sort()
        
        return nodes.container('',
            nodes.bullet_list('',
                *[ nodes.list_item('',
                       nodes.paragraph('', '',
                         nodes.strong('', '',
                           nodes.reference('', NAME, refuri=uris[NAME]))
                         )
                       )
                   for NAME in componentNames
                 ]
                )
            )

    def formatComponentPage(self,moduleName, component):
        return self.formatDeclarationPage(moduleName, self.formatComponent, component)
        
    def formatPrefabPage(self,moduleName, prefab):
        return self.formatDeclarationPage(moduleName, self.formatPrefab, prefab)
        
    def formatDeclarationPage(self, name, method, arg):
        parentURI = self.renderer.makeURI(".".join(name.split(".")[:-1]))
        trailTree = self.formatTrail(name)
        declarationTree = method(arg)
        
        return nodes.section('',
            nodes.title('', '', *trailTree.children),
            nodes.paragraph('', '',
                nodes.Text("For examples and more explanations, see the "),
                nodes.reference('', 'module level docs.', refuri=parentURI)
                ),
            nodes.transition(),
            nodes.section('', *declarationTree),
            nodes.transition(),
            self.postscript(),
            )
           
    def formatModule(self, moduleName, module, components, prefabs):
        
        trailTree = self.formatTrail(moduleName)
        moduleTree = self.docString(module.docString, main=True)
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
            declarationTrees[prefab.name] = self.formatPrefab(prefab)

        declNames = declarationTrees.keys()
        declNames.sort()
        for name in declNames:
            allDeclarations.extend(declarationTrees[name])
        
        componentListTree = self.componentList( components + prefabs )

        return nodes.container('',
            nodes.section('',
                nodes.title('','', *trailTree.children),
                componentListTree,
                nodes.paragraph('', nodes.Text("Explanations")),
                toc,
            ),
            nodes.transition(),
            moduleTree,
            nodes.transition(),
            nodes.section('', *allDeclarations),
            nodes.transition(),
            self.postscript() 
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

        return parent
        

    def formatIndex(self, path, subTree): #indexName, subTree, componentsAndPrefabs):
        depth=self.config.treeDepth

        indexName = ".".join(path)
        
        moduleTree = []
        if self.config.includeModuleDocString:
            if subTree.has_key("__init__"):
                docs = subTree["__init__"].docString
            if docs and "This is a doc string" not in docs:
                moduleTree = [ nodes.transition(),
                            self.docString(docs) ]
        
        return nodes.section('',
            * [ nodes.title('', '', *self.formatTrail(indexName).children),
                self.generateIndex(path, subTree, depth=depth),
              ]
            + moduleTree
            + [ nodes.transition(),
                self.postscript(),
              ]
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
            modPath = tuple(list(path)+[name])
            thisMod = self.config.repository.flatModules[modPath]
            modName = ".".join(modPath)
            
            # build "(a,b,c)" style list of links to actual components/prefabs in the module
            # (if they exist)
            moduleContents = []
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

    def postscript(self):
        return self.docString("""\
            Feedback
            --------
            Got a problem with the documentation? Something unclear that could be clearer?
            Want to help improve it? Constructive criticism is very welcome! (preferably in
            the form of suggested rewording)
            
            Please leave you feedback
            `here <http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701>`_
            in reply to the documentation thread in the Kamaelia blog.
            """)
            
            
def generateDocumentationFiles(formatter, CONFIG):
    
    MODULES = [ K for K in CONFIG.repository.flatModules.keys() \
                if CONFIG.filterPattern in ".".join(K) ]
    for MODULE in MODULES:
        moduleName = ".".join(MODULE)
        print "Processing: "+moduleName

        module     = CONFIG.repository.flatModules[MODULE]
        components = module.components
        prefabs    = module.prefabs
        
        doctree  = formatter.formatModule(moduleName, module, components, prefabs)
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



def generateIndices(formatter, CONFIG):

    def generate(formatter, CONFIG, subtree, path):
        if path != []:
            indexName = ".".join(path)
            print "Creating index: "+indexName
            
            doctree  = formatter.formatIndex(path,subtree)
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

    debug = False
    REPOSITORY = Repository.KamaeliaRepositoryDocs(None)
    config.repository=REPOSITORY
    config.docdir     = "pydoc"

    if len(sys.argv)>1:
        config.filterPattern = sys.argv[1]

    config.treeDepth=99
    config.tocDepth=3
    config.includeMethods=True
    config.includeModuleDocString=True
    config.showComponentsOnIndices=True
        
    renderer = RenderHTML(titlePrefix="Kamaelia docs : ",debug=False)
    
    if 0:
        # automatically generate crosslinks when component names are seen
        crossLinks = {}
        for (path,m) in REPOSITORY.flatModules():
            for item in m.components + m.prefabs:
                name=".".join(path+[item.name])
                crossLinks[name] = name
        for fullpath in crossLinks.keys():
            shortened = fullpath.split(".")[-1]
            crossLinks[shortened] = crossLinks[fullpath]
        renderer.setAutoCrossLinks( crossLinks )
    
    formatter = docFormatter(renderer, config=config)

    generateDocumentationFiles(formatter,config)
    generateIndices(formatter,config)
