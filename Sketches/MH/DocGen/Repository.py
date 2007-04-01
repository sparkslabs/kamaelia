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

import compiler
from compiler import ast
import os

class SourceTreeDocs(object):
    def __init__(self, baseDir=None, rootName="Kamaelia", excludeFilenames=["Repository.py"]):
        super(SourceTreeDocs,self).__init__()
        
        if baseDir:
            self.baseDir = baseDir
        else:
            import Kamaelia
            self.baseDir = os.path.dirname(Kamaelia.__file__)
            
        self.excludeFilenames = excludeFilenames
            
        root=rootName.split(".")
        self.flatModules={}
        self.nestedModules={}
        
        nested=self.nestedModules
        for node in root:
            nested[node] = {}
            nested=nested[node]
        self.build(self.baseDir, self.flatModules, nested, base=root)
        
        
    def build(self,dirName,flatModules,nestedModules,base):
        dirEntries = os.listdir(dirName)
        containsPythonFiles = False
        
        for filename in dirEntries:
            filepath = os.path.join(dirName, filename)
            if filename in self.excludeFilenames:
                continue
            
            elif os.path.isdir(filepath):
                subTree = {}
                subBase = base + [filename]
                foundPythonFiles = self.build(filepath, flatModules, subTree, subBase)
                # only include if there was actually something in there!
                if foundPythonFiles:
                    containsPythonFiles = True
                    nestedModules[filename] = subTree
                
            elif isPythonFile(dirName, filename):
                containsPythonFiles=True
                moduleName = filename[:-3]
                modulePath = ".".join(base+[moduleName])
                if filename == "__init__.py":
                    flatModulePath = base[:]
                else:
                    flatModulePath = base+[moduleName]
                    
                print "Parsing:",filepath
                moduleDocs = ModuleDocs(filepath, flatModulePath)
                
                flatModules[tuple(flatModulePath)] = moduleDocs
                nestedModules[moduleName] = moduleDocs

        return containsPythonFiles


def isPythonFile(Path, File):
    FullEntry = os.path.join(Path, File)
    if os.path.isfile(FullEntry):
        if len(File) > 3:
            if File[-3:] == ".py":
                return True
    return False


class ClassDocs(object): pass
class FunctionDocs(object): pass
MethodDocs         = FunctionDocs
KamaeliaPrefabDocs = FunctionDocs
class KamaeliaComponentDocs(ClassDocs): pass

ANY=object()

class ModuleDocs(object):
    def __init__(self, filepath, modulePath):
        super(ModuleDocs,self).__init__()
        self.AST = compiler.parseFile(filepath)

        self.extractModuleDocString()
        self.findKamaeliaEntities()
        self.findOtherEntities()
        
        self.prefabs = []
        for prefabName in self.prefabNames:
            doc = self.documentNamedFunction(prefabName, modulePath)
            self.prefabs.append(doc)
        
        self.components = []
        for componentName in self.componentNames:
            doc = self.documentNamedComponent(componentName, modulePath)
            self.components.append(doc)
        
        self.classes = []
        for className in self.otherClassNames:
            doc = self.documentNamedClass(className, modulePath)
            self.classes.append(doc)
            
        self.functions = []
        for funcName in self.otherFunctionNames:
            doc = self.documentNamedFunction(funcName, modulePath)
            self.functions.append(doc)
            

    def extractModuleDocString(self):
        assert(isinstance(self.AST, ast.Module))
        self.docString = self.AST.doc or ""

    def findKamaeliaEntities(self):
        # find the __kamaelia_compoents__ declaration
        stmt = self.AST.getChildren()[1]
        assert(isinstance(stmt, ast.Stmt))
        components = self.findAssignments( "__kamaelia_components__",
                                           stmt,
                                           [ast.Class, ast.Function, ast.Module]
                                         )
        prefabs    = self.findAssignments( "__kamaelia_prefabs__",
                                           stmt,
                                           [ast.Class, ast.Function, ast.Module]
                                         )

        # flatten the results
        components = _stringsInList([x for (_,x) in components])
        prefabs    = _stringsInList([x for (_,x) in prefabs])

        # and remove any repeats (unlikely)
        self.componentNames = dict([(x,x) for x in components]).keys()
        self.prefabNames = dict([(x,x) for x in prefabs]).keys()
        
    def findOtherEntities(self):
        stmt = self.AST.getChildren()[1]
        assert(isinstance(stmt, ast.Stmt))
        
        # find other class, method etc top level declarations in the source
        functions = self.findFunctions(ANY, stmt, [ast.Class, ast.Module, ast.Function, ast.If])
        classes   = self.findClasses(ANY, stmt, [ast.Class, ast.Module, ast.Function, ast.If])
        
        # convert from ast to name
        functions = [func.getChildren()[1] for func in functions]
        classes   = [clss.getChildren()[0] for clss in classes]
        
        # remove anything already matched up as being a prefab or component
        functions = [name for name in functions if name not in self.prefabNames]
        classes   = [name for name in classes   if name not in self.componentNames]

        self.otherFunctionNames = functions
        self.otherClassNames   = classes
        

    def findAssignments(self, target, node, ignores):
        # recurse to find an assignment statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Assign):
                assignStmt = child.getChildren()
                lhs = assignStmt[0]
                if isinstance(lhs, ast.AssName):
                    lhsname = lhs.getChildren()[0]
                    if lhsname == target or target==ANY:
                        rhs = assignStmt[1]
                        found.append((lhsname,rhs))
                        
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self.findAssignments(target, child, ignores)
                
        return found

    def findFunctions(self, target, node, ignores):
        # recurse to find a function statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Function):
                if child.name == target or target == ANY:
                    found.append(child)
            
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self.findFunctions(target, child, ignores)
                
        return found
    
    def documentNamedFunction(self, prefabName, modulePath):
        fnode = self.findFunctions( prefabName,
                                    self.AST.getChildren()[1],
                                    [ast.Class, ast.Function, ast.Module]
                                  )
        assert(len(fnode)==1)
        fnode=fnode[0]
        assert(prefabName == fnode.name)
        return self.documentFunction(fnode, modulePath)
        
    def documentFunction(self, fnode, modulePath):
        doc = fnode.doc or ""
        # don't bother with argument default values since we'd need to reconstruct
        # potentially complex values
        argNames = [(str(argName),str(argName)) for argName in fnode.argnames]
        i=-1
        numVar = fnode.varargs or 0
        numKW  = fnode.kwargs or 0
        for j in range(numKW):
            argNames[i] = ( argNames[i][0], "**"+argNames[i][1] )
            i-=1
        for j in range(numVar):
            argNames[i] = ( argNames[i][0], "*"+argNames[i][1] )
            i-=1
        for j in range(len(fnode.defaults)-numVar-numKW):
            argNames[i] = ( argNames[i][0], "["+argNames[i][1]+"]" )
            i-=1
        
        argStr = ", ".join([arg for (_, arg) in argNames])
        argStr = argStr.replace(", [", "[, ")
        
        theFunc = FunctionDocs()
        theFunc.name = fnode.name
        theFunc.args = argNames
        theFunc.argString = argStr
        theFunc.docString = doc
        theFunc.module = ".".join(modulePath)
        return theFunc
        
    
    def findClasses(self, target, node, ignores):
        # recurse to find a function statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Class):
                if child.name == target or target == ANY:
                    found.append(child)
            
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self.findClasses(target, child, ignores)
                
        return found
    
    def findBoxDecl(self, codeNode, boxTypeName):
        for child in codeNode.getChildren():
            if isinstance(child, ast.Assign):
                assignStmt = child.getChildren()
                lhs = assignStmt[0]
                if isinstance(lhs, ast.AssName):
                    if lhs.getChildren()[0] == boxTypeName:
                        rhs = assignStmt[1]
                        if isinstance(rhs, ast.Dict):
                            return self.parseDictBoxes(rhs)
                        elif isinstance(rhs, ast.List):
                            return self.parseListBoxes(rhs)
        return []
                
    def parseDictBoxes(self, dictNode):
        boxes = []
        for (lhs,rhs) in dictNode.items:
            if isinstance(lhs, ast.Const) and isinstance(rhs, ast.Const):
                name = lhs.value
                desc = rhs.value
                if isinstance(name, str) and isinstance(desc, str):
                    boxes.append((name,desc))
        return dict(boxes)
                
    def parseListBoxes(self, listNode):
        boxes = []
        for item in listNode.getChildren():
            if isinstance(item, ast.Const):
                name = item.value
                if isinstance(name, str):
                    boxes.append((name,''))
        return list(boxes)
    
    def documentNamedComponent(self, componentName, modulePath):
        cnode = self.findClasses( componentName,
                                  self.AST.getChildren()[1],
                                  [ast.Class, ast.Function, ast.Module]
                                )
        assert(len(cnode)>=1)
        cnode = cnode[0]
        assert(componentName == cnode.name)
        cDoc = cnode.doc or ""
        inboxDoc  = self.findBoxDecl(cnode.code, "Inboxes")
        outboxDoc = self.findBoxDecl(cnode.code, "Outboxes")
        
        methodNodes = self.findFunctions(ANY, cnode.code, [ast.Class, ast.Function, ast.Module])
        methods = [self.documentFunction(node, modulePath) for node in methodNodes]
        
        theComp = KamaeliaComponentDocs()
        theComp.name = componentName
        theComp.docString = cDoc
        theComp.inboxes = inboxDoc
        theComp.outboxes = outboxDoc
        theComp.methods = methods
        theComp.module = ".".join(modulePath)
        return theComp
    
    def documentNamedClass(self, className, modulePath):
        cnode = self.findClasses( className,
                                  self.AST.getChildren()[1],
                                  [ast.Class, ast.Function, ast.Module, ast.If]
                                )
        assert(len(cnode)>=1)
        cnode = cnode[0]
        assert(className == cnode.name)
        cDoc = cnode.doc or ""
        
        methodNodes = self.findFunctions(ANY, cnode.code, [ast.Class, ast.Function, ast.Module])
        methods = [self.documentFunction(node, modulePath) for node in methodNodes]
        
        theClass = ClassDocs()
        theClass.name = className
        theClass.docString = cDoc
        theClass.methods = methods
        theClass.module = ".".join(modulePath)
        return theClass


def _stringsInList(theList):
    # flatten a tree structured list containing strings, or possibly ast nodes
    
    if isinstance(theList,ast.Node):
        theList = theList.getChildren()
        
    found = []
    for item in theList:
        if isinstance(item,str):
            found.append(item)
        elif isinstance(item, ast.Name):
            found.append(item.name)
        elif isinstance(item,(list,tuple,ast.Node)):
            found.extend(_stringsInList(item))
    return found



# METHODS PROVIDING
# BACKWARD COMPATIBILITY WITH OLD Repository.py

def GetAllKamaeliaComponentsNested(baseDir=None):
    rDocs = SourceTreeDocs(baseDir)
    moduleTree = rDocs.nestedModules
    reduced = _reduceToNames(moduleTree, keepComponents=True, keepPrefabs=False)
    if reduced["Kamaelia"].has_key("Support"):
        del reduced["Kamaelia"]["Support"]
    return reduced

def GetAllKamaeliaComponents(baseDir=None):
    rDocs = SourceTreeDocs(baseDir)
    modules = rDocs.flatModules
    return _reduceToNames(modules, keepComponents=True, keepPrefabs=False)

def GetAllKamaeliaPrefabsNested(baseDir=None):
    rDocs = SourceTreeDocs(baseDir)
    moduleTree = rDocs.nestedModules
    reduced = _reduceToNames(moduleTree, keepComponents=False, keepPrefabs=True)
    if reduced["Kamaelia"].has_key("Support"):
        del reduced["Kamaelia"]["Support"]
    return reduced
    
def GetAllKamaeliaPrefabs(baseDir=None):
    rDocs = SourceTreeDocs(baseDir)
    modules = rDocs.flatModules
    return _reduceToNames(modules, keepComponents=False, keepPrefabs=True)


def _reduceToNames(tree, keepComponents=True, keepPrefabs=True):
    output={}
    for key in tree.keys():
        value=tree[key]
        if isinstance(value,dict):
            output[key] = _reduceToNames(value, keepComponents, keepPrefabs)
        elif isinstance(value, KamaeliaModuleDocs):
            if key == "__init__":
                continue
            else:
                items = []
                if keepComponents:
                    componentNames = [c.name for c in value.components]
                    items.extend(componentNames)
                if keepPrefabs:
                    prefabNames = [p.name for p in value.prefabs]
                    items.extend(prefabNames)
                if len(items)>0:
                    output[key] = items
    return output
    


        
if __name__ == "__main__":
    file="/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/File/Reading.py"
    #file="/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/Chassis/Pipeline.py"
    #file="/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/Protocol/RTP/NullPayloadRTP.py"
    modDocs = ModuleDocs(file,["Kamaelia","File","Reading"])

    print "MODULE:"
    print modDocs.docString
    
    print 
    print "PREFABS:"
    for m in modDocs.prefabs:
        print m.name, m.args
        
    print
    print "COMPONENTS:"
    for comp in modDocs.components:
        print comp.name
        print "Inboxes:  ",comp.inboxes
        print "Outboxes: ",comp.outboxes
        for meth in comp.methods:
            print meth.name + "(" + meth.argString + ")"
        print

    import pprint
    pprint.pprint(GetAllKamaeliaComponents(),None,4)
    print
    print "*******************************************************************"
    print
    pprint.pprint(GetAllKamaeliaComponentsNested(),None,4)
