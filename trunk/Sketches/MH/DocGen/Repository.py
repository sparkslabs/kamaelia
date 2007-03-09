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

class KamaeliaRepositoryDocs(object):
    def __init__(self, baseDir=None):
        super(KamaeliaRepositoryDocs,self).__init__()
        if baseDir:
            self.baseDir = baseDir
        else:
            import Kamaelia
            self.baseDir = os.path.dirname(Kamaelia.__file__)
            
        flat={}
        nested={"Kamaelia":{}}
        self.build(self.baseDir, flat, nested["Kamaelia"], base=["Kamaelia"])
        
        self.flatModules = flat
        self.nestedModules = nested
        
        
    def build(self,dirName,flatModules,nestedModules,base):
        dirEntries = os.listdir(dirName)
        containsPythonFiles = False
        
        for filename in dirEntries:
            filepath = os.path.join(dirName, filename)
            if filename == "Repository.py":
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
                moduleDocs = KamaeliaModuleDocs(filepath, flatModulePath)
                
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


class KamaeliaComponentDocs(object): pass
class KamaeliaPrefabDocs(object): pass
KamaeliaFunctionDocs = KamaeliaPrefabDocs
KamaeliaMethodDocs = KamaeliaPrefabDocs


class KamaeliaModuleDocs(object):
    def __init__(self, filepath, modulePath):
        super(KamaeliaModuleDocs,self).__init__()
        self.AST = compiler.parseFile(filepath)

        self.extractModuleDocString()
        self.findEntities()
        
        self.prefabs = []
        for prefabName in self.prefabNames:
            doc = self.documentNamedFunction(prefabName, modulePath)
            self.prefabs.append(doc)
        
        self.components = []
        for componentName in self.componentNames:
            doc = self.documentNamedComponent(componentName, modulePath)
            self.components.append(doc)
        

    def extractModuleDocString(self):
        assert(isinstance(self.AST, ast.Module))
        self.docString = self.AST.doc or ""

    def findEntities(self):
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
        components = _stringsInList(components)
        prefabs    = _stringsInList(prefabs)

        # and remove any repeats (unlikely)
        self.componentNames = dict([(x,x) for x in components]).keys()
        self.prefabNames = dict([(x,x) for x in prefabs]).keys()
        

    def findAssignments(self, target, node, ignores):
        # recurse to find an assignment statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Assign):
                assignStmt = child.getChildren()
                lhs = assignStmt[0]
                if isinstance(lhs, ast.AssName):
                    if lhs.getChildren()[0] == target:
                        rhs = assignStmt[1]
                        found.append(rhs)
                        
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
                if child.name == target or target == None:
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
        
        theFunc = KamaeliaFunctionDocs()
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
                if child.name == target:
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
        
        methodNodes = self.findFunctions(None, cnode.code, [ast.Class, ast.Function, ast.Module])
        methods = [self.documentFunction(node, modulePath) for node in methodNodes]
        
        theComp = KamaeliaComponentDocs()
        theComp.name = componentName
        theComp.docString = cDoc
        theComp.inboxes = inboxDoc
        theComp.outboxes = outboxDoc
        theComp.methods = methods
        theComp.module = ".".join(modulePath)
        return theComp

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
    rDocs = KamaeliaRepositoryDocs(baseDir)
    moduleTree = rDocs.nestedModules
    reduced = _reduceToNames(moduleTree, keepComponents=True, keepPrefabs=False)
    if reduced["Kamaelia"].has_key("Support"):
        del reduced["Kamaelia"]["Support"]
    return reduced

def GetAllKamaeliaComponents(baseDir=None):
    rDocs = KamaeliaRepositoryDocs(baseDir)
    modules = rDocs.flatModules
    return _reduceToNames(modules, keepComponents=True, keepPrefabs=False)

def GetAllKamaeliaPrefabsNested(baseDir=None):
    rDocs = KamaeliaRepositoryDocs(baseDir)
    moduleTree = rDocs.nestedModules
    reduced = _reduceToNames(moduleTree, keepComponents=False, keepPrefabs=True)
    if reduced["Kamaelia"].has_key("Support"):
        del reduced["Kamaelia"]["Support"]
    return reduced
    
def GetAllKamaeliaPrefabs(baseDir=None):
    rDocs = KamaeliaRepositoryDocs(baseDir)
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
    modDocs = KamaeliaModuleDocs(file,["Kamaelia","File","Reading"])

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
