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
from docutils import nodes
import Kamaelia.Support.Data.Repository

from renderHTML      import RenderHTML
from renderPlaintext import RenderPlaintext

from Nodes import boxright

class docFormatter(object):
    def __init__(self, renderer=RenderPlaintext,debug=False):
        super(docFormatter,self).__init__()
        self.renderer = renderer
        self.debug = debug

    uid = 0

    def genUniqueRef(self):
        uid = str(self.uid)
        self.uid+=1
        return uid

    def emptyTree(self):
        return core.publish_doctree("")
    
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
#        pre = ""
#        if main:
#            pre = "\n"
#
#        return pre + self.renderer.preformat(docstring)+ "\n"

    def formatArgSpec(self, argspec):
        return pprint.pformat(argspec[0]).replace("[","(").replace("]",")").replace("'","")

    def formatMethodDocStrings(self,X):
        docTree = nodes.section('') #self.emptyTree()
        
        for method in sorted([x for x in inspect.classify_class_attrs(X) if x[2] == X and x[1] == "method"]):
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

    def formatComponent(self, X, includeMethods=False):
        CLASSNAME = self.formatClassStatement(X.__name__, X.__bases__)
        CLASSDOC = self.docString(X.__doc__)
        INBOXES = self.boxes(X.__name__,"Inboxes", X.Inboxes)
        OUTBOXES = self.boxes(X.__name__,"Outboxes", X.Outboxes)
        
        if includeMethods:
            METHODS = [ nodes.section('',
                          nodes.title('', 'Methods defined here'),
                          boxright('',
                              nodes.paragraph('', '',
                                nodes.Text("hello!!!!!")
                                ),
                          ),
                          * self.formatMethodDocStrings(X)
                        )
                      ]
        else:
            METHODS = []

        return nodes.container('',
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
        
    def formatModuleTrail(self, moduleName):
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
                line.append(nodes.Text(" . "))
            URI = self.renderer.makeURI(accum)
            line.append( nodes.reference('', element, refuri=URI) )
            
            firstPass=False
        
        return trail
    
    def componentList(self, componentList):
        return nodes.container('',
#            nodes.paragraph('', '', nodes.Text('Components and Prefabs')),
            nodes.bullet_list('',
                *[ nodes.list_item('',
                       nodes.paragraph('', '',
                         nodes.strong('', '',
                           nodes.reference('', COMPONENT, refid='component-'+COMPONENT))
                         )
                       )
                   for COMPONENT in componentList
                 ]
                )
            )

    def formatModule(self, moduleName, module, components, prefabs):
        
        trailTree = self.formatModuleTrail(moduleName)
        moduleTree = self.docString(module.__doc__, main=True)
        toc = self.buildTOC(moduleTree, depth=3)
        
        allDeclarations = []
        
        declarationTrees = {}
        for component in components:
            declarationTrees[component.__name__] = self.formatComponent(component, includeMethods=True)
            
        for prefab in prefabs:
            assert(prefab.__name__ not in declarationTrees)
            declarationTrees[prefab.__name__] = self.formatPrefab(prefab)
            
        for name in sorted(declarationTrees.keys()):
            allDeclarations.extend(declarationTrees[name])
        
        componentListTree = self.componentList( sorted(declarationTrees.keys()) )

        return nodes.section('',
            trailTree,
#            nodes.paragraph('', nodes.Text("Component/Prefab details")),
            componentListTree,
            nodes.paragraph('', nodes.Text("Explanations")),
            toc,
            nodes.transition(),
            moduleTree,
            nodes.transition(),
            nodes.section('',
                id = [ 'component-declarations' ],
                name = [ 'component-declarations' ],
                * [ nodes.title('', "Component/Prefab details"),
                    nodes.section('',
                        *allDeclarations
                    )
                  ]
                ),
            nodes.transition(),
            self.postscript(),
            )
            
    def buildTOC(self, srcTree, parent=None, depth=3):
        """Recurse through a source document tree, building a table of contents"""
        if parent is None:
            parent = nodes.bullet_list()

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
        

    def formatIndex(self, indexName, subTree, depth):
        return nodes.section('',
#            nodes.title('', indexName),
            self.formatModuleTrail(indexName),
            self.generateIndex(subTree, depth=depth),
            nodes.transition(),
            self.postscript(),
            )

    def generateIndex(self, srcTree, parent=None, depth=99):
        if parent is None:
            parent = nodes.bullet_list()

        if depth<=0:
            return parent

        items=nodes.section()

        for name in sorted(srcTree.keys()):
            uri = self.renderer.makeURI(name)
            text = name.split(".")[-1]
            newItem = nodes.list_item('',
                nodes.paragraph('','', nodes.reference('', text, refuri=uri))
                )
            if srcTree[name]:  # if not empty, recurse
                newItem.append(nodes.bullet_list())
                self.generateIndex(srcTree[name], newItem[-1], depth-1)
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
            
            
def generateDocumentationFiles(filterString):
    MODULES = dict(COMPONENTS.items())
    MODULES.update(dict(PREFABS.items()))
    MODULES = [M for M in MODULES.keys() if filterString in M]
    for MODULE in MODULES:
        print "Processing: "+MODULE
        
        cNames = COMPONENTS.get(MODULE,[])
        pNames = PREFABS.get(MODULE,[])
        
        module = __import__(MODULE, [], [], cNames+pNames)
        components = [ getattr(module, c) for c in cNames ]
        prefabs = [ getattr(module, p) for p in pNames ]
        
        doctree  = formatter.formatModule(MODULE, module, components, prefabs)
        filename = formatter.renderer.makeFilename(MODULE)
        output   = formatter.renderer.render(MODULE, doctree)
        
        F = open(docdir+"/"+filename, "w")
        F.write(output)
        F.close()
        



def generateIndices(depth=99):

    # list of all leaf modules
    MODULES = dict(COMPONENTS.items())
    MODULES.update(dict(PREFABS.items()))
    MODULES = MODULES.keys()
    
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
        
        doctree  = formatter.formatIndex(indexName, INDEX[indexName], depth)
        filename = formatter.renderer.makeFilename(indexName)
        output   = formatter.renderer.render(indexName, doctree)
        
        F = open(docdir+"/"+filename, "w")
        F.write(output)
        F.close()
    
    


if __name__ == "__main__":

    docdir = "pydoc"
    
    formatter = docFormatter(RenderHTML(titlePrefix="Kamaelia docs : ",debug=False))
#    formatter = docFormatter(RenderPlaintext)

    debug = False
    if debug:
        COMPONENTS = {
            "Kamaelia.ReadFileAdaptor" : ("ReadFileAdaptor",)
        }
    else:
        C = Kamaelia.Support.Data.Repository.GetAllKamaeliaComponents()
        P = Kamaelia.Support.Data.Repository.GetAllKamaeliaPrefabs()
        COMPONENTS = {}
        for key in C.keys():
            COMPONENTS[".".join(key)] = C[key]
        PREFABS = {}
        for key in P.keys():
            PREFABS[".".join(key)] = P[key]

    import sys
    filterPattern = ""
    if len(sys.argv)>1:
        filterPattern = sys.argv[1]

    generateDocumentationFiles(filterPattern)
    generateIndices(depth=2)
