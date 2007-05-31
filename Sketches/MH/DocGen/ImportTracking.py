#!/usr/bin/env python

# ------------------------------------------------------------------------------
# Test Content

from Axon.Component import component
import Axon.ThreadedComponent

class Test(object):
    pass

class Test2(component):
    pass

class Test3(Axon.ThreadedComponent.threadedcomponent):
    pass

import Axon.ThreadedComponent as bibble

flurble = bibble.threadedcomponent

class Test4(flurble): # derives from Axon.ThreadedComponent.threadedcomponent
    pass

from Kamaelia.Chassis.Pipeline import Pipeline as foo

class Test5(foo): # derives from Kamaelia.Chassis.Pipeline.Pipeline
    pass

(alpha,beta) = (flurble, foo)
[gamma,delta] = (alpha,beta)
(epsilon, theta) = gamma,(object,object)

import Kamaelia.Chassis.Graphline as Graphline, Kamaelia.Chassis.Carousel as Carousel

class Test5a(epsilon):
    pass


Test6 = Test5

class Test7(Test6):
    pass

def Test8():
    pass

Test9 = Test8

Test10 = Test8
Test10a=Test10
Test10 = "hello"

from Nodes import boxright

class Test11(boxright):
    pass

epsilon = boxright

class Test12(epsilon):
    pass

import Nodes

class Test13(Nodes.boxright):
    pass

from Axon.Component import component as Axon

class Test14(object):
    import Axon
    class Test15(Test13):
        def foo(self): pass
        
    class Test16(Axon.AxonExceptions.noSpaceInBox):
        pass
    
    def plig(self):
        pass
    
    Test17=Test15

class Test18(Axon):
    pass

Test19 = Test14
Test14 = None
    
# ------------------------------------------------------------------------------

import compiler
from compiler import ast

import __builtin__ as BUILTINS


def UNPARSED(ast=None):
    return { "type" : "UNPARSED",
             "ast"  : ast,
           }


class Scope(object):

    def __init__(self, type="Module", ASTChildren=None, imports=None, localModules={}, rootScope=None):
        super(Scope,self).__init__()

        self.symbols={}
        self.type=type
        if imports is not None:
            self.imports=imports
        else:
            self.imports=ImportScope("")
        self.localModules=localModules
        if rootScope is not None:
            self.rootScope=rootScope
        else:
            self.rootScope=self

        if ASTChildren is None or ASTChildren==[]:
            return
        
        # parse the AST
        for node in ASTChildren:
            if isinstance(node, ast.From): 
                self._parse_From(node)            # parse "from ... import"s to recognise what symbols are mapped to what imported things
            elif isinstance(node, ast.Import):
                self._parse_Import(node)          # parse resolvesTo to recognise what symbols are mapped to what imported things
            elif isinstance(node, ast.Class):
                self._parse_Class(node)           # classes need to be parsed so we can work out base classes
            elif isinstance(node, ast.Function):
                self._parse_Function(node)
            elif isinstance(node, ast.Assign):
                self._parse_Assign(node)          # parse assignments that map stuff thats been imported to new names
            elif isinstance(node, ast.AugAssign):
                pass                              # definitely ignore these
            else:
                pass                              # ignore everything else for the moment
        return

    def _parse_From(self,node):
        sourceModule = node.modname
        for (name, destName) in node.names:
            # check if this is actually a local module
            if sourceModule in self.localModules:
                sourceModule=self.localModules[sourceModule]
            mapsTo = ".".join([sourceModule,name])
            if destName == None:
                destName = name

            theImport=self.imports.find(mapsTo)
            self.assign(destName, theImport)

    def _parse_Import(self, node):
        for (name,destName) in node.names:
            if name in self.localModules:
                fullname = self.localModules[name]
            else:
                fullname = name
            if destName == None:
                self.imports.find(fullname) # force creation of the full item - looking it up in an import asserts its existence
                head=fullname.split(".")[0]
                theImport=self.imports.find(head)
                self.assign(head,theImport)
            else:
                theImport=self.imports.find(fullname)
                self.assign(destName, theImport)
        
    def _parse_Class(self, node):
        self.assign(node.name, ClassScope(node,self.imports,self.localModules,self.rootScope,self))
        
    def _parse_Function(self, node):
        self.assign(node.name, FunctionScope(node,self.imports,self.localModules,self.rootScope))
        
    def _parse_Assign(self, node):
        for target in node.nodes:
            # for each assignment target, go clamber through mapping against the assignment expression
            # we'll only properly parse things with a direct 1:1 mapping
            # if, for example, the assignment relies on understanding the value being assigned, eg. (a,b) = c
            # then we'll silently fail
            assignments = self._mapAssign(target,node.expr)
            resolvedAssignments = []
            for (target,expr) in assignments:
                if isinstance(expr,str):
                    try:
                        resolved = self.find(expr)
                    except ValueError:
                        resolved = UnparsedScope(expr,self.imports,self.localModules,self.rootScope)
                else:
                    resolved = UnparsedScope(expr,self.imports,self.localModules,self.rootScope)
                resolvedAssignments.append((target,resolved))
                
            for (target,expr) in resolvedAssignments:
                self.assign(target,expr)

    def _mapAssign(self, target, expr):
        """\
        Correlate each term on the lhs to the respective term on the rhs of the assignment.

        Return a list of pairs (lhs, rhs) not yet resolved - just the names
        """
        assignments = []
        if isinstance(target, ast.AssName):
            targetname = self._parse_Name(target)
            if isinstance(expr, (ast.Name, ast.Getattr)):
                assignments.append( (targetname, self._parse_Name(expr)) )
            else:
                assignments.append( (targetname, UNPARSED(expr)) )
        elif isinstance(target, (ast.AssTuple, ast.AssList)):
            if isinstance(expr, (ast.Tuple, ast.List)):
                targets = target.nodes
                exprs = expr.nodes
                if len(targets)==len(exprs):
                    for i in range(0,len(targets)):
                        assignments.extend(self._mapAssign(targets[i],exprs[i]))
                else:
                    for i in range(0,len(targets)):
                        assignments.append( (targetname, UNPARSED()) )
            else:
                pass # dont know what to do with this term on the lhs of the assignment
        else:
            pass # dont know what to do with this term on the lhs of the assignment
        return assignments

    def _parse_Name(self,node):
        if isinstance(node, (ast.Name, ast.AssName)):
            return node.name
        elif isinstance(node, (ast.Getattr, ast.AssAttr)):
            return ".".join([self._parse_Name(node.expr), node.attrname])
        else:
            return ""
        
    def resolveName(self,provisionalName):
        return provisionalName

    def find(self, name, checkRoot=True):
        segmented=name.split(".")
        head=segmented[0]
        tail=".".join(segmented[1:])

        if head in self.symbols:
            found=self.symbols[head]
            if tail=="":
                return found
            else:
                return found.find(tail,checkRoot=False)
        else:
            if checkRoot and self.rootScope != self:
                return self.rootScope.find(name,checkRoot=False)
        raise ValueError("Cannot find it!")

    def assign(self, name, value, checkRoot=True):
        segmented=name.split(".")
        head=segmented[0]
        tail=".".join(segmented[1:])

        if tail=="":
            self.symbols[head]=value
        else:
            if head in self.symbols:
                self.symbols[head].assign(tail,value,checkRoot=False)
            else:
                if checkRoot and self.rootScope != self:
                    return self.rootScope.assign(name,value,checkRoot=False)
            raise ValueError("Cannot assign to this!")

    def listAllClasses(self,recurseDepth=0):
        return self.listAllMatching(ClassScope,recurseDepth)
            
    def listAllFunctions(self,recurseDepth=0):
        return self.listAllMatching(FunctionScope,recurseDepth)
            
    def listAllMatching(self,types,recurseDepth=0):
        found=[]
        for symbol in self.symbols:
            item=self.symbols[symbol]
            if isinstance(item,types):
                found.append((symbol,item))
            if recurseDepth>0:
                subfound=item.listAllMatching(types,recurseDepth-1)
                for (name,thing) in subfound:
                    found.append((symbol+"."+name,thing))
        return found
            
class ModuleScope(Scope):
    def __init__(self, AST, imports, localModules={}, rootScope=None):
        super(ModuleScope,self).__init__("Module",AST.node.nodes,imports,localModules,None)
        self.doc = AST.doc


class ClassScope(Scope):
    def __init__(self, AST, imports, localModules, rootScope, parentScope):
        super(ClassScope,self).__init__("Class",AST.code,imports,localModules,rootScope)

        self.doc = AST.doc
        # parse bases
        self.bases = []
        for baseName in AST.bases:
            parsedBaseName=self._parse_Name(baseName)
            try:
                base=parentScope.find(parsedBaseName)
                resolvedBaseName = base.resolveName(parsedBaseName)
            except ValueError:
                base=None
                resolvedBaseName = parsedBaseName
            self.bases.append((resolvedBaseName,base))
        

class FunctionScope(Scope):
    def __init__(self, AST, imports, localModules, rootScope):
        super(FunctionScope,self).__init__("Class",None,imports,localModules,rootScope) # don't bother parsing function innards

        self.doc = AST.doc
        # parse arguments
        argNames = [(str(argName),str(argName)) for argName in AST.argnames]
        i=-1
        numVar = AST.varargs or 0
        numKW  = AST.kwargs or 0
        for j in range(numKW):
            argNames[i] = ( argNames[i][0], "**"+argNames[i][1] )
            i-=1
        for j in range(numVar):
            argNames[i] = ( argNames[i][0], "*"+argNames[i][1] )
            i-=1
        for j in range(len(AST.defaults)-numVar-numKW):
            argNames[i] = ( argNames[i][0], "["+argNames[i][1]+"]" )
            i-=1
        
        argStr = ", ".join([arg for (_, arg) in argNames])
        argStr = argStr.replace(", [", "[, ")
        
        self.args = argNames
        self.argString = argStr

class ImportScope(Scope):
    def __init__(self,importPathName="",imports=None):
        if importPathName=="" and imports==None:
            imports=self
        super(ImportScope,self).__init__("Module",None,imports,[],None)  # its an opaque imported module, no local modules, etc to concern ourselves with
        
        self.doc = ""
        self.importPathName=importPathName
        
    def resolveName(self,provisionalName):
        return self.importPathName

    def find(self,name,checkRoot=False):
        # we assume the symbol exists(!), so if it is referenced, we create a placeholder for it (if one doesn't already exist)
        # shouldn't check in root scope of this parsing, since, as an import, this *is* the new root (its a new module)
        checkRoot=False
        segmented=name.split(".")
        head=segmented[0]
        tail=".".join(segmented[1:])

        if head not in self.symbols:
            if self.importPathName:
                fullname=self.importPathName+"."+head
            else:
                fullname=head
            self.assign(head, ImportScope(fullname,self.imports))
            
        found=self.symbols[head]
        if tail=="":
            return found
        else:
            return found.find(tail,checkRoot=False)

    def assign(self, name, value, checkRoot=False):
        # we assume the symbol exists(!), so if it is referenced, we create a placeholder for it (if one doesn't already exist)
        checkRoot=False
        segmented=name.split(".")
        head=segmented[0]
        tail=".".join(segmented[1:])

        if tail=="":
            self.symbols[head]=value
        else:
            if head not in self.symbols:
                if self.importPathName:
                    fullname=self.importPathName+"."+head
                else:
                    fullname=head
                self.assign(head, ImportScope(fullname,self.imports))
            self.symbols[head].assign(tail,value,checkRoot=False)
    
class UnparsedScope(Scope):
    def __init__(self, AST, imports, localModules, rootScope):
        super(UnparsedScope,self).__init__("Unparsed",AST,imports,localModules,rootScope)
        self.doc=""
        self.ast=AST
        



if __name__ == "__main__":

    

    import sys
    if len(sys.argv)==2:
        sourcefile = sys.argv[1]
        check=False
    else:
        sourcefile = sys.argv[0]
        check=True


    # now lets try to sequentially traverse the AST and track imports (and
    # name reassignments of them) so we can eventually determine what the base
    # classes of declared classes are

    AST = compiler.parseFile(sourcefile)
    root = AST           # root statement node is a module, get the children

    localModules = {
        "Nodes" : "Pretend.there.is.a.module.path.Nodes",
        }
    
    d = ModuleScope(root,None,localModules)
    
    import pprint
    print "-----MAPPINGS:"
    print
    for (name,data) in d.listAllMatching(object,recurseDepth=5):
        print name
    print
    print d.find("Graphline.Inboxes").ast
    print "-----CLASSES IDENTIFIED:"
    print
    for (classname,data) in d.listAllClasses(recurseDepth=2):
        bases = [name for (name,_) in data.bases]
        print "class ",classname,"..."
        print "   parsing says bases are:",bases
        if check:
            print "   bases actually are:    ",[base.__module__+"."+base.__name__ for base in eval(classname).__bases__]
    print
    print "-----FUNCTIONS:"
    print
    for (funcname,data) in d.listAllFunctions(recurseDepth=2):
        print "function ",funcname,"(",data.argString,")",
        if check:
            print "...",
            if eval(funcname).__class__.__name__ in ["function","instancemethod"]:
                print "YES"
            else:
                print "NO"
        else:
            print
    print
    print "-----"
#     print
#     for (name,data) in d.listAllMatching(object,recurseDepth=5):
#         print name
#         print " ...","(",data.__class__.__name__,")"
#         print " ...",data.resolveName(name)
#     print
#     print "-----"
#     for (name,data) in d.imports.listAllMatching(object,recurseDepth=5):
#         print name
#         print " ...","(",data.__class__.__name__,")"
#         print " ...",data.resolveName(name)
#     print
#     print "-----"
    
