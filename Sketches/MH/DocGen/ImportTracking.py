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

# ------------------------------------------------------------------------------

if __name__ == "__main__":

    import sys
    sourcefile = sys.argv[0]

    import compiler
    from compiler import ast

    # now lets try to sequentially traverse the AST and track imports (and
    # name reassignments of them) so we can eventually determine what the base
    # classes of declared classes are

    AST = compiler.parseFile(sourcefile)
    root = AST.getChildren()[1]           # root statement node

    resolvesTo = {}
    classes = {}
    
    def parse_From(node, resolvesTo):
        sourceModule, items = node.getChildren()
        for (name, destName) in items:
            mapsTo = ".".join([sourceModule,name])
            if destName == None:
                destName = name
            resolvesTo[destName] = mapsTo
            
    def parse_Import(node, resolvesTo):
        items = node.getChildren()[0]

        for (name,destName) in items:
            if destName == None:
                destName = name
            resolvesTo[destName] = name
            
    def parse_Class(node, resolvesTo,classes):
        name = node.name
        bases = node.bases
        resolvedBases = []
        for base in bases:
            expBase = parseName(base)
            resolvedBase = matchToImport(resolvesTo,expBase)
            resolvedBases.append(resolvedBase)
        classes[name] = resolvedBases
        resolvesTo[name] = name  # XXX LOCAL NAME, DOES IT NEED SCOPING CONTEXT?
        
    def parse_Assign(node, resolvesTo, classes):
        for target in node.nodes:
            # for each assignment target, go clamber through mapping against the assignment expression
            # we'll only properly parse things with a direct 1:1 mapping
            # if, for example, the assignment relies on understanding the value being assigned, eg. (a,b) = c
            # then we'll silently fail
            assignments = mapAssign(target,node.expr)
            resolvedAssignments = []
            for (target,expr) in assignments:
                resolved = matchToImport(resolvesTo,expr)
                resolvedAssignments.append((target,resolved))
            for (target,expr) in resolvedAssignments:
                resolvesTo[target] = expr
                if expr in classes.keys():
                    classes[target] = classes[expr]

            
    def mapAssign(target, expr):
        assignments = []
        if isinstance(target, ast.AssName):
            if isinstance(expr, (ast.Name, ast.Getattr)):
                assignments.append( (parseName(target), parseName(expr)) )
        elif isinstance(target, (ast.AssTuple, ast.AssList)):
            if isinstance(expr, (ast.Tuple, ast.List)):
                targets = target.nodes
                exprs = expr.nodes
                if len(targets)==len(exprs):
                    for i in range(0,len(targets)):
                        assignments.extend(mapAssign(targets[i],exprs[i]))
        else:
            pass
        return assignments

    
    def chaseThrough(node, resolvesTo,classes):
        for node in node.getChildren():
            if isinstance(node, ast.From):
                # parse "from ... import"s to recognise what symbols are mapped to what imported things
                parse_From(node, resolvesTo)
            elif isinstance(node, ast.Import):
                # parse resolvesTo to recognise what symbols are mapped to what imported things
                parse_Import(node, resolvesTo)
            elif isinstance(node, ast.Class):
                # classes need to be parsed so we can work out base classes
                parse_Class(node, resolvesTo,classes)
            elif isinstance(node, ast.Assign):
                # parse assignments that map stuff thats been imported to new names
                parse_Assign(node, resolvesTo,classes)
            elif isinstance(node, ast.AugAssign):
                # definitely ignore these
                pass
            else:
                pass  # ignore everything else for the moment
        return
        
    def parseName(node):
        if isinstance(node, (ast.Name, ast.AssName)):
            return node.name
        elif isinstance(node, (ast.Getattr, ast.AssAttr)):
            return ".".join([parseName(node.expr), node.attrname])
        else:
            return None
        
    def matchToImport(resolvesTo,name):
        # go through resolvesTo, if we find one that matches the root of the name
        # then resolve it
        for (importName,resolved) in resolvesTo.items():
            if importName == name:
                return resolved
            else:
                importName+="."
                if importName == name[:len(importName)]:
                    return ".".join([resolved, name[len(importName):]])
        return name
    
    chaseThrough(root, resolvesTo, classes)
    
    import pprint
    print "-----MAPPINGS:"
    pprint.pprint(resolvesTo)
    print "-----CLASSES:"
    for cls in classes:
        bases = classes[cls]
        print "class ",cls,"..."
        print "   parsing says bases are:",bases
        print "   bases actually are:    ",[base.__module__+"."+base.__name__ for base in eval(cls).__bases__]
    print "-----"
    
