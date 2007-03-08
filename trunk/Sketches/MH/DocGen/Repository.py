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
        

    def extractModuleDocString(self):
        assert(isinstance(self.AST, ast.Module))
        self.docString = self.AST.doc

    def findEntities(self):
        # find the __kamaelia_compoents__ declaration
        stmt = self.AST.getChildren()[1]
        assert(isinstance(stmt, ast.Stmt))
        components = self.findAssignment( "__kamaelia_components__",
                                          stmt,
                                          [ast.Class, ast.Function]
                                        )
        prefabs    = self.findAssignment( "__kamaelia_prefabs__",
                                          stmt,
                                          [ast.Class, ast.Function]
                                        )

        # flatten the results
        components = self.stringsInList(components)
        prefabs    = self.stringsInList(prefabs)

        # and remove any repeats (unlikely)
        components = dict([(x,x) for x in components]).keys()
        prefabs = dict([(x,x) for x in prefabs]).keys()
        
        print components
        print prefabs
        

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

    def stringsInList(self, theList):
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