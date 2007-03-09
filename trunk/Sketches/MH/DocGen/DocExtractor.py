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
        self.components = {}
        self.prefabs = {}
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

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        docTree = nodes.section('') #self.emptyTree()
        
        methods = [x for x in inspect.classify_class_attrs(X) if x[2] == X and x[1] == "method"]
        methods.sort()
        
        for method in methods:
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

    def formatComponent(self, X):
        CLASSNAME = self.formatClassStatement(X.__name__, X.__bases__)
        CLASSDOC = self.docString(X.__doc__)
        INBOXES = self.boxes(X.__name__,"Inboxes", X.Inboxes)
        OUTBOXES = self.boxes(X.__name__,"Outboxes", X.Outboxes)
        
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
            
        trailTree = self.formatTrail(X.__module__+"."+X.__name__)

        return \
                nodes.section('',
                * [ nodes.title('', CLASSNAME, ids=["component-"+X.__name__]) ]
                  + CLASSDOC
                  + [ INBOXES, OUTBOXES ]
                  + METHODS
                )
        
    def formatPrefab(self, X):
        CLASSNAME = self.formatPrefabStatement(X.__name__)
        CLASSDOC = self.docString(X.__doc__)
        
        return nodes.container('',
                * [ nodes.title('', CLASSNAME, ids=["component-"+X.__name__]) ]
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
            fullname = component.__module__ + "." + component.__name__
            uris[component.__name__] = self.renderer.makeURI(fullname)

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
        moduleTree = self.docString(module.__doc__, main=True)
        toc = self.buildTOC(moduleTree, depth=self.config.tocDepth)
        
        allDeclarations = []
        
        declarationTrees = {}
        for component in components:
            cTrail = self.formatTrail(moduleName+"."+component.__name__)
            declarationTrees[component.__name__] = nodes.container('',
                nodes.title('','', *cTrail.children),
                    self.formatComponent(component)
            )
            
        for prefab in prefabs:
            assert(prefab.__name__ not in declarationTrees)
            declarationTrees[prefab.__name__] = self.formatPrefab(prefab)

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
        

    def formatIndex(self, indexName, subTree, componentsAndPrefabs):
        depth=self.config.treeDepth
        
        moduleTree = []
        if self.config.includeModuleDocString:
            docs = __import__(indexName+".__init__", [], [],["__doc__"]).__doc__
            if docs and "This is a doc string" not in docs:
                moduleTree = [ nodes.transition(),
                            self.docString(docs) ]
        
        return nodes.section('',
            * [ nodes.title('', '', *self.formatTrail(indexName).children),
                self.generateIndex(subTree, componentsAndPrefabs, depth=depth),
              ]
            + moduleTree
            + [ nodes.transition(),
                self.postscript(),
              ]
            )

    def generateIndex(self, srcTree, componentsAndPrefabs, parent=None, depth=99):
        if parent is None:
            parent = nodes.bullet_list()

        if depth<=0:
            return parent

        items=nodes.section()

        childNames = srcTree.keys()
        childNames.sort()
        for name in childNames:
            
            # build "(a,b,c)" style list of links to actual components/prefabs in the module
            # (if they exist)
            moduleContents = []
            if self.config.showComponentsOnIndices:
                if len(componentsAndPrefabs.get(name,[])) > 0:
                    moduleContents.append(nodes.Text(" ( "))
                    first=True
                    declarationNames = componentsAndPrefabs[name]
                    declarationNames.sort()
                    for declaration in declarationNames:
                        if not first:
                            moduleContents.append(nodes.Text(", "))
                        first=False
                        uri = self.renderer.makeURI(name+"."+declaration)
                        linkToDecl = nodes.reference('', nodes.Text(declaration), refuri=uri)
                        moduleContents.append(linkToDecl)
                    moduleContents.append(nodes.Text(" )"))

            # now make the list item for this module
            uri = self.renderer.makeURI(name)
            text = name.split(".")[-1]
            newItem = nodes.list_item('',
                nodes.paragraph('','',
                    nodes.strong('', '',nodes.reference('', text, refuri=uri)),
                    *moduleContents
                    )
                )
                
            if srcTree[name]:  # if not empty, recurse
                newItem.append(nodes.bullet_list())
                self.generateIndex(srcTree[name], componentsAndPrefabs, newItem[-1], depth-1)
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
    MODULES = dict(CONFIG.components.items())
    MODULES.update(dict(CONFIG.prefabs.items()))
    MODULES = [M for M in MODULES.keys() if CONFIG.filterPattern in M]
    for MODULE in MODULES:
        print "Processing: "+MODULE
        
        cNames = CONFIG.components.get(MODULE,[])
        pNames = CONFIG.prefabs.get(MODULE,[])
        
        module = __import__(MODULE, [], [], cNames+pNames)
        components = [ getattr(module, c) for c in cNames ]
        prefabs = [ getattr(module, p) for p in pNames ]
        
        doctree  = formatter.formatModule(MODULE, module, components, prefabs)
        filename = formatter.renderer.makeFilename(MODULE)
        output   = formatter.renderer.render(MODULE, doctree)
        
        F = open(CONFIG.docdir+"/"+filename, "w")
        F.write(output)
        F.close()
        
        for component in components:
            NAME = MODULE+"."+component.__name__
            print "    Component: "+NAME
            filename = formatter.renderer.makeFilename(NAME)
            doctree = formatter.formatComponentPage(NAME, component)
            output   = formatter.renderer.render(NAME, doctree)
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()

        for prefab in prefabs:
            NAME = MODULE+"."+prefab.__name__
            print "    Prefab: "+NAME
            filename = formatter.renderer.makeFilename(NAME)
            doctree = formatter.formatPrefabPage(NAME, prefab)
            output   = formatter.renderer.render(NAME, doctree)
            F = open(CONFIG.docdir+"/"+filename, "w")
            F.write(output)
            F.close()



def generateIndices(formatter, CONFIG):

    # list of all leaf modules
    ALLITEMS = dict(CONFIG.components.items())
    for (mod,prefabs) in CONFIG.prefabs.items():
        ALLITEMS[mod] = ALLITEMS.get(mod,[])
        ALLITEMS[mod].extend(prefabs)
    MODULES = ALLITEMS.keys()
    
    # now build a list of all module sub paths, eg A, A.B, A.B.C
    MODULETREE = {}
    INDEX = {}
    for fullPath in MODULES:
        parts = fullPath.split(".")
        path = ""
        currentNode = MODULETREE
        for part in parts:
            if path!="":
                path+="."
            path+=part
            currentNode[path] = currentNode.get(path,{})
            currentNode = currentNode.get(path,{})
            if path not in INDEX and path not in MODULES:
                INDEX[path] = currentNode
                
    # MODULETREE now contains a tree structure; at each node is the full path
    # leading up to that point. This tree includes all leaves from MODULES
    
    # INDEX contains maps all partial paths, excluding modules, to subsets of
    # the module tree structure
    
    for indexName in INDEX.keys():
        print "Creating index: "+indexName
        
        doctree  = formatter.formatIndex(indexName, INDEX[indexName],ALLITEMS)
        filename = formatter.renderer.makeFilename(indexName)
        output   = formatter.renderer.render(indexName, doctree)
        
        F = open(CONFIG.docdir+"/"+filename, "w")
        F.write(output)
        F.close()
    
    
if __name__ == "__main__":

    import sys
    
    
    config = DocGenConfig()

    debug = False
    if debug:
        COMPONENTS = {
            "Kamaelia.ReadFileAdaptor" : ("ReadFileAdaptor",)
        }
        PREFABS = {}
    else:
#        C = Kamaelia.Support.Data.Repository.GetAllKamaeliaComponents()
#        P = Kamaelia.Support.Data.Repository.GetAllKamaeliaPrefabs()
        C = Repository.GetAllKamaeliaComponents()
        P = Repository.GetAllKamaeliaPrefabs()
        COMPONENTS = {}
        for key in C.keys():
            COMPONENTS[".".join(key)] = C[key]
        PREFABS = {}
        for key in P.keys():
            PREFABS[".".join(key)] = P[key]
    
    config.components = COMPONENTS
    config.prefabs    = PREFABS
    config.docdir     = "pydoc"

    if len(sys.argv)>1:
        config.filterPattern = sys.argv[1]

    config.treeDepth=99
    config.tocDepth=3
    config.includeMethods=True
    config.includeModuleDocString=False
    config.showComponentsOnIndices=True
        
    renderer = RenderHTML(titlePrefix="Kamaelia docs : ",debug=False)
    
    if 0:
        # automatically generate crosslinks when component names are seen
        crossLinks = {}
        for (m,cs) in COMPONENTS.items() + PREFABS.items():
            for c in cs:
                crossLinks[m+"."+c] = m+"."+c
        for fullpath in crossLinks.keys():
            shortened = fullpath.split(".")[-1]
            crossLinks[shortened] = crossLinks[fullpath]
        renderer.setAutoCrossLinks( crossLinks )
    
    formatter = docFormatter(renderer, config=config)

    generateDocumentationFiles(formatter,config)
    generateIndices(formatter,config)
