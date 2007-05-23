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

import Kamaelia.Chassis.Graphline as Graphline, Kamaelia.Chassis.Carousel as Carousel

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

    imports = {}
    classes = {}
    
    def parse_From(node, imports):
        sourceModule, items = node.getChildren()
        for (name, destName) in items:
            mapsTo = ".".join([sourceModule,name])
            if destName == None:
                destName = name
            imports[destName] = mapsTo
            
    def parse_Import(node, imports):
        items = node.getChildren()[0]

        for (name,destName) in items:
            if destName == None:
                destName = name
            imports[destName] = name
            
    def parse_Class(node, imports,classes):
        name = node.name
        bases = node.bases
        resolvedBases = []
        print name,bases
        for base in bases:
            expBase = parseName(base)
            print "!!",expBase,base
            resolvedBase = matchToImport(imports,expBase)
            resolvedBases.append(resolvedBase)
        classes[name] = resolvedBases
        imports[name] = name  # XXX LOCAL NAME, DOES IT NEED SCOPING CONTEXT?
    
    def chaseThrough(node, imports,classes):
        for node in node.getChildren():
            if isinstance(node, ast.From):
                # parse "from ... import"s to recognise what symbols are mapped to what imported things
                parse_From(node, imports)
            elif isinstance(node, ast.Import):
                # parse imports to recognise what symbols are mapped to what imported things
                parse_Import(node, imports)
            elif isinstance(node, ast.Class):
                parse_Class(node, imports,classes)
                pass  # classes need to be parsed so we can work out base classes
            elif isinstance(node, ast.Assign):
                pass  # parse assignments that map stuff thats been imported to new names
            else:
                pass  # ignore everything else for the moment
        return
        
    def parseName(node):
        if isinstance(node, ast.Name):
            return node.name
        elif isinstance(node, ast.Getattr):
            return ".".join([parseName(node.expr), node.attrname])
        else:
            return node.__class__.__name__
        
    def matchToImport(imports,name):
        # go through imports, if we find one that matches the root of the name
        # then resolve it
        for (importName,resolved) in imports.items():
            if importName == name:
                return resolved
            else:
                importName+="."
                if importName == name[:len(importName)]:
                    return ".".join([resolved, name[len(importName):]])
        return name
    
    chaseThrough(root, imports, classes)
    
    import pprint
    print "-----MAPPINGS:"
    pprint.pprint(imports)
    print "-----CLASSES:"
    pprint.pprint(classes)
    print "-----"
    
