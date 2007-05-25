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

class Test5(epsilon):
    pass


Test6 = Test5

class Test7(Test6):
    pass

def Test8():
    pass

Test9 = Test8

Test10 = Test8
Test10 = "hello"

from Nodes import boxright

class Test11(boxright):
    pass

epsilon = boxright

class Test12(epsilon):
    pass

# ------------------------------------------------------------------------------

import compiler
from compiler import ast

import __builtin__ as BUILTINS

def UNKNOWN(name):
    return { "name" : name,
             "type" : "UNKNOWN",
           }

def CLASS(name,bases):
    return { "name"  : name,
             "type"  : "CLASS",
             "bases" : bases,
           }

def FUNCTION(name):
    return { "name" : name,
             "type" : "FUNCTION",
           }

def UNPARSED(ast=None):
    return { "name" : "",
             "type" : "UNPARSED",
             "ast"  : ast,
           }
           
class DeclarationTracker(object):
    def __init__(self,localModules={}):
        """\
        Arguments:

        - localModules  -- a dict mapping modules in the local path of this one to their full module path

        eg. if the module being parsed is foo.bibble and other modules exist called "foo.bar", "foo.plig" and "foo.boing.yoyo"
        then we should provide a dictionary { "bar":"foo.bar", "plig":"foo.plig", "boing.yoyo":"foo.boing.yoyo" }
        so import statements can be checked against this.
        """
        super(DeclarationTracker,self).__init__()
        self.resolvesTo = {}
        self.localModules = localModules

    def parse_From(self, node):
        sourceModule = node.modname
        for (name, destName) in node.names:
            # check if this is actually a local module
            if sourceModule in self.localModules:
                sourceModule=self.localModules[sourceModule]
            mapsTo = ".".join([sourceModule,name])
            if destName == None:
                destName = name
            self.resolvesTo[destName] = UNKNOWN(mapsTo)

    def parse_Import(self, node):
        for (name,destName) in node.names:
            if name in self.localModules:
                name = self.localModules[name]
            if destName == None:
                destName = name
            self.resolvesTo[destName] = UNKNOWN(name)

    def parse_Class(self, node):
        name = node.name
        bases = node.bases
        resolvedBases = []
        for base in bases:
            expBase = self.parseName(base)
            resolvedBase = self.matchToSymbolName(expBase)
            resolvedBases.append(resolvedBase)
        self.resolvesTo[name] = CLASS(name,resolvedBases)  # XXX LOCAL NAME, DOES IT NEED SCOPING CONTEXT?

    def parse_Assign(self, node):
        for target in node.nodes:
            # for each assignment target, go clamber through mapping against the assignment expression
            # we'll only properly parse things with a direct 1:1 mapping
            # if, for example, the assignment relies on understanding the value being assigned, eg. (a,b) = c
            # then we'll silently fail
            assignments = self.mapAssign(target,node.expr)
            resolvedAssignments = []
            for (target,expr) in assignments:
                if isinstance(expr,str):
                    resolved = self.matchToSymbolName(expr)
                else:
                    resolved = expr
                resolvedAssignments.append((target,resolved))
                
            for (target,expr) in resolvedAssignments:
                self.resolvesTo[target] = expr


    def mapAssign(self, target, expr):
        """\
        Correlate each term on the lhs to the respective term on the rhs of the assignment.

        Return a list of pairs (lhs, rhs) not yet resolved - just the names
        """
        assignments = []
        if isinstance(target, ast.AssName):
            targetname = self.parseName(target)
            if isinstance(expr, (ast.Name, ast.Getattr)):
                assignments.append( (targetname, self.parseName(expr)) )
            else:
                assignments.append( (targetname, UNPARSED(expr)) )
        elif isinstance(target, (ast.AssTuple, ast.AssList)):
            if isinstance(expr, (ast.Tuple, ast.List)):
                targets = target.nodes
                exprs = expr.nodes
                if len(targets)==len(exprs):
                    for i in range(0,len(targets)):
                        assignments.extend(self.mapAssign(targets[i],exprs[i]))
                else:
                    for i in range(0,len(targets)):
                        assignments.append( (targetname, UNPARSED()) )
            else:
                pass # dont know what to do with this term on the lhs of the assignment
        else:
            pass # dont know what to do with this term on the lhs of the assignment
        return assignments

    def parse_Function(self, node):
        self.resolvesTo[node.name] = FUNCTION(node.name)

    def chaseThrough(self, node):
        for node in node.getChildren():
            if isinstance(node, ast.From):
                # parse "from ... import"s to recognise what symbols are mapped to what imported things
                self.parse_From(node)
            elif isinstance(node, ast.Import):
                # parse resolvesTo to recognise what symbols are mapped to what imported things
                self.parse_Import(node)
            elif isinstance(node, ast.Class):
                # classes need to be parsed so we can work out base classes
                self.parse_Class(node)
            elif isinstance(node, ast.Function):
                self.parse_Function(node)
            elif isinstance(node, ast.Assign):
                # parse assignments that map stuff thats been imported to new names
                self.parse_Assign(node)
            elif isinstance(node, ast.AugAssign):
                # definitely ignore these
                pass
            else:
                pass  # ignore everything else for the moment
        return

    def parseName(self,node):
        if isinstance(node, (ast.Name, ast.AssName)):
            return node.name
        elif isinstance(node, (ast.Getattr, ast.AssAttr)):
            return ".".join([self.parseName(node.expr), node.attrname])
        else:
            return None

    def matchToSymbolName(self,name):
        # go through resolvesTo, if we find one that matches the root of the name
        # then resolve it
        for (symbolName,resolved) in self.resolvesTo.items():
            if symbolName == name:
                return resolved
            else:
                symbolName+="."
                if symbolName == name[:len(symbolName)]:
                    return UNKNOWN(".".join([resolved["name"], name[len(symbolName):]]))
        # not matched against existing resolution table, what else...
        if name in dir(BUILTINS):
            return UNKNOWN("__builtin__."+name)
        else:
            return UNKNOWN(name)

    def listAllClasses(self):
        return [name for (name,info) in self.resolvesTo.items() if info["type"] == "CLASS"]

    def listAllFunctions(self):
        return [name for (name,info) in self.resolvesTo.items() if info["type"] == "FUNCTION"]

    def getClassBasesNames(self,classname):
        info = self.resolvesTo[classname]
        if not info["type"]=="CLASS":
            raise IndexError("Referenced symbol was not directly determined to be a class")
        else:
            return [base["name"] for base in info["bases"]]

if __name__ == "__main__":

    

    import sys
    sourcefile = sys.argv[0]


    # now lets try to sequentially traverse the AST and track imports (and
    # name reassignments of them) so we can eventually determine what the base
    # classes of declared classes are

    AST = compiler.parseFile(sourcefile)
    root = AST.getChildren()[1]           # root statement node

    localModules = {
        "Nodes" : "Pretend.there.is.a.module.path.Nodes",
        }
    
    d = DeclarationTracker(localModules)
    d.chaseThrough(root)
    
    import pprint
    print "-----MAPPINGS:"
    pprint.pprint(d.resolvesTo)
    print "-----CLASSES:"
    for classname in d.listAllClasses():
        bases = d.getClassBasesNames(classname)
        print "class ",classname,"..."
        print "   parsing says bases are:",bases
        print "   bases actually are:    ",[base.__module__+"."+base.__name__ for base in eval(classname).__bases__]
    print "-----FUNCTIONS:"
    for funcname in d.listAllFunctions():
        print "function ",funcname,"...",
        if eval(funcname).__class__.__name__ == "function":
            print "YES"
        else:
            print "NO"
    print "-----"
    
