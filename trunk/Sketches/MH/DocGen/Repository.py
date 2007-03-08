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


class KamaeliaModuleDocs(object):
    def __init__(self, source):
        super(KamaeliaModuleDocs,self).__init__()
        self.AST = compiler.parse(source)

        self.extractModuleDocString()
        self.findEntities()
        
        self.prefabs = []
        for prefabName in self.prefabNames:
            doc = self.documentFunction(prefabName)
            self.prefabs.append(doc)
        
#        self.components = []
#        for componentNAme in self.componentNames:
#            doc = self.documentComponent(componentName)
#            self.components.append(doc)
        

    def extractModuleDocString(self):
        assert(isinstance(self.AST, ast.Module))
        self.docString = self.AST.doc

    def findEntities(self):
        # find the __kamaelia_compoents__ declaration
        stmt = self.AST.getChildren()[1]
        assert(isinstance(stmt, ast.Stmt))
        components = self.findAssignment( "__kamaelia_components__",
                                          stmt,
                                          [ast.Class, ast.Function, ast.Module]
                                        )
        prefabs    = self.findAssignment( "__kamaelia_prefabs__",
                                          stmt,
                                          [ast.Class, ast.Function, ast.Module]
                                        )

        # flatten the results
        components = _stringsInList(components)
        prefabs    = _stringsInList(prefabs)

        # and remove any repeats (unlikely)
        self.componentNames = dict([(x,x) for x in components]).keys()
        self.prefabNames = dict([(x,x) for x in prefabs]).keys()
        

    def findAssignment(self, target, node, ignores):
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
                        found += rhs
                        
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self.findAssignment(target, child, ignores)
                
        return found

    def findFunction(self, target, node, ignores):
        # recurse to find a function statement for the given target
        # but ignoring any branches matching the node classes listed
        for child in node.getChildren():
            if isinstance(child, ast.Function):
                if child.name == target:
                    return child
            
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                rval = self.findFunction(target, child, ignores)
                if rval != None:
                    return rval
        return None
    
    def documentFunction(self, prefabName):
        fnode = self.findFunction( prefabName,
                                   self.AST.getChildren()[1],
                                   [ast.Class, ast.Function, ast.Module]
                                 )
        name = fnode.name
        doc = fnode.doc
        # don't bother with argument default values since we'd need to reconstruct
        # potentially complex values
        argNames = [(argName,argName) for argName in fnode.argnames]
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
        return (name, argNames, doc)
        


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
            found.extend(stringsInList(item))
    return found


def parseModule(source):
    return KamaeliaModuleDocs(source)

if __name__ == "__main__":
    f=open("/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/File/Reading.py","r")
    source = f.read()
    f.close()

    modDocs = KamaeliaModuleDocs(source)

    #print modDocs.docString
    for (name,args,doc) in modDocs.prefabs:
        print name,args
    