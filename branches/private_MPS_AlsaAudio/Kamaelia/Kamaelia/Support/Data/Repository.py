#!/usr/bin/python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
===========================================
Kamaelia component repository introspection
===========================================

This support code scans through a Kamaelia installation detecting components and
picking up relevant information such as doc strings, initializer arguments and
the declared Inboxes and Outboxes.
 
It not only detects components and prefabs, but also picks up modules, classes
and functions - making this a good source for documentation generation.



Example Usage
-------------

Simple lists of component/prefab names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fetch a flat listing of all components. The key is the module path (as a tuple)
and the value is a list of the names of the components found::
    
    >>> r=Repository.GetAllKamaeliaComponents()
    >>> r[('Kamaelia','Util','Console')]
    ['ConsoleEchoer', 'ConsoleReader']

Fetch a *nested* listing of all components. The leaf is a list of entity names::

    >>> r=Repository.GetAllKamaeliaComponentsNested()
    >>> r['Kamaelia']['Util']['Console']
    ['ConsoleEchoer', 'ConsoleReader']
    
Fetch a flat listing of all prefabs::

    >>> p=Repository.GetAllKamaeliaPrefabs()
    >>> p[('Kamaelia','File','Reading')]
    ['RateControlledFileReader', 'RateControlledReusableFileReader',
    'ReusableFileReader', 'FixedRateControlledReusableFileReader']
    
Fetch a *nested* listing of all prefabs::

    >>> p=Repository.GetAllKamaeliaPrefabsNested()
    >>> p['Kamaelia']['File']['Reading']
    ['RateControlledFileReader', 'RateControlledReusableFileReader',
    'ReusableFileReader', 'FixedRateControlledReusableFileReader']

Fetching a flat listing of components as defined in a specific directory (rather
than the current Kamaelia installation)::

    >>> r=Repository.GetAllKamaeliaComponents(baseDir="/data/my-projects/my-components/")
    

Detailed introspections::
~~~~~~~~~~~~~~~~~~~~~~~~~

We can ask for a complete introspection of the current Kamaelia installation::
    
   >>> docTree=Repository.ModuleDoc("Kamaelia","/usr/lib/python/site-packages/Kamaelia")
   >>> docTree.resolve(roots={"Kamaelia":docTree})

And look up a particular module::

   >>> m=docTree.find("Util.Console")
   >>> m
  <Repository.ModuleDoc object at 0x40403b0c>
   
Then find components declared in that module::

   >>> cs=m.listAllComponents()
   >>> cs
   [('ConsoleReader', <Repository.ClassScope object at 0x41511bac>), ('ConsoleEchoer', <Repository.ClassScope object at 0x4115990c>)]
   >>> (name,c)=cs[0]
   >>> name
   'ConsoleReader'
   >>> c
   <Repository.ClassScope object at 0x41511bac>
    
And look at properties of that component::
    
    >>> c.module
    'Kamaelia.Util.Console'
    >>> c.inboxes
    {'control': 'NOT USED', 'inbox': 'NOT USED'}
    >>> c.outboxes
    {'outbox': 'Lines that were typed at the console', 'signal': 'NOT USED'}
    >>> print c.doc
    ConsoleReader([prompt][,eol]) -> new ConsoleReader component.
    
    Component that provides a console for typing in stuff. Each line is output
    from the "outbox" outbox one at a time.
    
    Keyword arguments:
    
    - prompt  -- Command prompt (default=">>> ")
    - eol     -- End of line character(s) to put on end of every line outputted (default is newline)
    
This includes methods defined in it::

    >>> c.listAllFunctions()
    [('main', <Repository.FunctionScope object at 0x4166822c>), ('__init__', <Repository.FunctionScope object at 0x4166224c>)]
    >>> name,f=c.listAllFunctions()[1]
    >>> name
    '__init__'
    >>> f
    <Repository.FunctionScope object at 0x4166224c>
    
We can look at the docs for the function:
    
    >>> f.doc
    'x.__init__(...) initializes x; see x.__class__.__doc__ for signature'
    
We can ask for a string summarising the method's arguments::
    
    >>> f.argString
    'self[, prompt][, eol]'
    
Or a list naming each argument, consisting of (argname, summary-representation)
pairs::
    
    >>> f.args
    [('self', 'self'), ('prompt', '[prompt]'), ('eol', '[eol]')]



Obtaining introspection data
----------------------------

To get a detailed introspection you create a ModuleDoc object. You can
either point it at a specific directory, or just let it introspect the currently
installed Kamaelia repository.

You can specify the module path corresponding to that directory (the "root
name"). The default is simply "Kamaelia". If for example, you point it at the
Kamaelia.Chassis directory; you should explain that the root name is
"Kamaelia.Chassis". Or if, for example, you are using this code to document
Axon, you would specify a root name of "Axon".

After instantiating your ModuleDoc object; remember to call its "resolve" method
to allow it to resolve references to base classes, and determine method the
resolution order for classes.



How are components and prefabs detected?
----------------------------------------

Components and prefabs are detected in sourcefiles by looking for declarations
of an __kamaelia_components__ and __kamaelia_prefabs__ variables, for example::

    __kamaelia_components__ = [ "IcecastClient", "IcecastDemux", "IcecastStreamWriter" ]
    __kamaelia_prefabs__ = [ "IcecastStreamRemoveMetadata" ]

They should be declared individually, at module level, and should consist of a
simple list of strings giving the names of the components/prefabs present.



Structure of detailed introspections
------------------------------------

The introspection is a hierarchy of Scope objects, each representing a delcaration
scope - such as a module, class, function, etc. These are built up to reflect
the structure of the library if it is imported.

* ModuleDoc objects represent each module. They may contain:
    
    * Other ModuleDoc objects
    
    * ImportScope objects
    
    * ClassScope objects (representing classes and components)
    
    * FunctionScope objects (repesenting functions and prefabs)
    
    * UnparsedScope objects (anything that wasn't parsed)
    
ClassScope and FunctionScope objects may also contain any of these. For example,
methods in a class will be represented as FunctionScope objects within the
ClassScope object.
    
The find() method of any given scope can be used to lookup a symbol in that scope,
or its children. For example, you could call find() on the "Kamaelia.Chassis"
ModuleDoc object with the argument "Graphline.Graphline" to retrieve the graphline
component (its full path is "Kamaelia.Chassis.Graphline.Graphline")

The listAllXXXXX() methods enumerate items - such as classes, functions,
components, prefabs or modules.



Implementation Details
----------------------

This code uses the python compiler.ast module to parse the source of python
files, rather than import them. This allows introspection of code that might not
necessarily run on the system at hand - perhaps because not all dependancies can
be satisfied.

Basic tracking of assignment operations is performed, so the following is fair
game::
    
    from Axon.Component import component as flurble
    
    class Boo(flurble):
        pass
    
    Foo=Boo

However anything more comple is not processed. For example, functions and
classes declared within "if" statement will not be found::

    if 1:
        class WillNotBeDetected:
            pass
    
        def AlsoWillNotBeDetected():
            pass

The simplified functions that only return lists of component/prefab names (
GetAllKamaeliaComponentsNested, GetAllKamaeliaComponents,
GetAllKamaeliaPrefabsNested and GetAllKamaeliaPrefabs) simply run the full
introspection of the codebase but then throw most of the information away.

"""


import os
import sys

import compiler
from compiler import ast

import __builtin__ as BUILTINS

from os.path import isdir
from os.path import isfile
from os.path import exists
from os.path import join as pathjoin


class Scope(object):
    """\
    Representation of a declaration scope - could be a module, class, function, import, etc.
    Basically something that might contain other symbols.
    
    """

    def __init__(self, type="Module", ASTChildren=None, imports=None, localModules={}, rootScope=None):
        """\
        Arguments:
        
        - type          -- Descriptive name saying what kind of scope this is.
        - ASTChildren   -- List of AST nodes for whatever is within this scope. Will be parsed.
        - imports       -- Scope acting as a container/root for tracking any imports. Should be shared between all Scope objects.
        - localModules  -- Dict mapping module names that might be present in the same lexical level as this module, or deeper; mapping them to their full module names. Eg. for Axon.Component this might contain a mapping for "AxonException" to "Axon.AxonException"
        - rootScope     -- Scope object for current lexical root - eg. the Module containing this scope.
        """

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
	try:
		ASTChildren=ASTChildren.getChildNodes()   # python 2.3 complains if you try to iterate over the node itself
	except:
		pass

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
        """Parse a 'from ... import' AST node."""
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
        """Parse an import AST node."""
        for (name,destName) in node.names:
            # if module being referred to is in the local directory, map to the full pathame
            if name in self.localModules:
                fullname = self.localModules[name]
            else:
                fullname = name
            
            # force creation of the import, by looking for it (ImportScope objects do this)
            theImport=self.imports.find(fullname)
            
            # is it being imported as a particular name, or just as itself? (eg. import Axon.Component as Flurble)
            if destName == None:
                # work out the path to the root of the entity being imported (eg. "Axon.Component" for "import Component.component")
                fullnamesplit = fullname.split(".")
                namesplit=name.split(".")
                assert(namesplit==fullnamesplit[-len(namesplit):])
                head=fullnamesplit[:len(fullnamesplit)-len(namesplit)+1]
                
                theImport=self.imports.find(".".join(head))
                self.assign(namesplit[0],theImport)
            else:
                self.assign(destName, theImport)
        
    def _parse_Class(self, node):
        """Parse a class statement AST node"""
        self.assign(node.name, ClassScope(node,self.imports,self.localModules,self.rootScope,self))
        
    def _parse_Function(self, node):
        """Parse a function 'def' statement AST node"""
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
                        resolved = UnparsedScope(ast.Name(expr),self.imports,self.localModules,self.rootScope)
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
                assignments.append( (targetname, expr) )
        elif isinstance(target, (ast.AssTuple, ast.AssList)):
            if isinstance(expr, (ast.Tuple, ast.List)):
                targets = target.nodes
                exprs = expr.nodes
                if len(targets)==len(exprs):
                    for i in range(0,len(targets)):
                        assignments.extend(self._mapAssign(targets[i],exprs[i]))
                else:
                    for i in range(0,len(targets)):
                        assignments.append( (targetname, exprs) )
            else:
                pass # dont know what to do with this term on the lhs of the assignment
        else:
            pass # dont know what to do with this term on the lhs of the assignment
        return assignments

    def _parse_Name(self,node):
        """Parse a name AST node (some combination of Name/AssignName/GetAttr nodes)"""
        if isinstance(node, (ast.Name, ast.AssName)):
            return node.name
        elif isinstance(node, (ast.Getattr, ast.AssAttr)):
            return ".".join([self._parse_Name(node.expr), node.attrname])
        else:
            return ""
        
    def resolveName(self,provisionalName):
        """\
        Returns the name you suggest this module should have; or a different one
        if this module feels it knows better :-)
        
        Used by ImportScopes to explain that although they may have been imported into
        one place; they are actually from somewhere else.
        """
        return provisionalName

    def find(self, name, checkRoot=True):
        """\
        Find a given named symbol and return the scope object representing it.
        Returns the found scope object, or raises ValueError if none can be found.
        
        This operation recurses automatically to subscopes.
        
        Arguments:
        
        - name       -- the path name of the thing to find below here.
        - checkRoot  -- Optional. If it isn't found here, check the root scope too? (default=True)
        """
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

    def locate(self,value):
        """\
        Find where a given scope object is. Returns the pathname leading up to it,
        or raises ValueError if it couldn't be found.
        
        Effectively the reverse of the find() operation.
        
        Example::
        
            >>> myScope.locate(subSubScopeObject)
            'A.B.C'
        
        Arguments:
        
        - value  -- The scope object to locate.
        """
        for symbol in self.symbols:
            if value==self.symbols[symbol]:
                return symbol
        for symbol in self.symbols:
            try:
                return symbol+"."+self.symbols[symbol].locate(value)
            except ValueError:
                pass
        raise ValueError("Can't locate it!")

    def assign(self, name, value, checkRoot=True):
        """\
        Sets a given named symbol to be the supplied value. The name can be a
        path (dot separated), in which case it will be followed through to assign
        the symbol at the end of the path.
        
        ValueError will be raised if the path doesn't exist.
        
        Example::
        
            >>> myScope.assign("Flurble", Scope(...))
            >>> myScope.assign("Flurble.Plig", Scope(..))
        
        Arguments:
        
        - name       -- the path name of the thing to set
        - value      -- the object to assign as that name (eg. a scope object)
        - checkRoot  -- Optional. Check the root scope too? (default=True)
        """
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

    def listAllClasses(self,**options):
        return self.listAllMatching(ClassScope,**options)
            
    def listAllFunctions(self,**options):
        return self.listAllMatching(FunctionScope,**options)
    
    def listAllModules(self,**options):
        return self.listAllMatching(ModuleScope,**options)
    
    def listAllNonImports(self,**options):
        return self.listAllNotMatching((ImportScope,ModuleScope),**options)
            
    def listAllMatching(self,types, noRecurseTypes=None, recurseDepth=0):
        """\
        Returns a list of (pathName, object) pairs for all children of the
        specified type. Will recurse as deeply as you specify. You can also block
        it from recursing into certain scope types. By default, recusion stops
        at ModuleScope objects.
        
        Arguments::
        
        - types           -- tuple of classes that can be returned (default is ModuleScope)
        - noRecurseTypes  -- tuple of classes that will *not* be recursed into (default=none)
        - recurseDepth    -- Optional. Maximum recursion depth (default=0)
        """
        if noRecurseTypes==None:
            noRecurseTypes=(ModuleScope,)
        found=[]
        for symbol in self.symbols:
            item=self.symbols[symbol]
            if isinstance(item,types):
                found.append((symbol,item))
            if recurseDepth>0 and not isinstance(item,noRecurseTypes):
                subfound=item.listAllMatching(types,noRecurseTypes,recurseDepth-1)
                for (name,thing) in subfound:
                    found.append((symbol+"."+name,thing))
        return found
            
    def listAllNotMatching(self,types, noRecurseTypes=None, recurseDepth=0):
        """\
        Returns a list of (pathName, object) pairs for all children *not* matching the
        specified type. Will recurse as deeply as you specify. You can also block
        it from recursing into certain scope types. By default, recusion stops
        at ModuleScope objects.
        
        Arguments::
        
        - types           -- tuple of classes that can *not* be returned (default is ModuleScope)
        - noRecurseTypes  -- tuple of classes that will *not* be recursed into (default=none)
        - recurseDepth    -- Optional. Maximum recursion depth (default=0)
        """
        if noRecurseTypes==None:
            noRecurseTypes=(ModuleScope,)
        found=[]
        for symbol in self.symbols:
            item=self.symbols[symbol]
            if not isinstance(item,types):
                found.append((symbol,item))
            if recurseDepth>0 and not isinstance(item,noRecurseTypes):
                subfound=item.listAllMatching(types,noRecurseTypes,recurseDepth-1)
                for (name,thing) in subfound:
                    found.append((symbol+"."+name,thing))
        return found
                
    def resolve(self,_resolvePass=None,roots={}):
        """\
        Post processing step for resolving imports, base classes etc.
        
        Call this method after you have finished instantiating
        your whole tree of Scope objects.
        
        Arguments:
        
        - _resolvePass  -- For internal use. Don't specify when calling manually.
        - roots         -- list of master root scope objects - eg. the object representing the top level "Axon" or "Kamaelia" module.
        """
        if _resolvePass==None:
            self.resolve(_resolvePass=1,roots=roots)
            self.resolve(_resolvePass=2,roots=roots)
        else:
            for (name,item) in self.symbols.items():
                try:
                    item.resolve(_resolvePass=_resolvePass,roots=roots)
                except AttributeError:
                    # item doesn't have a 'resolve' method
                    pass
            
class ModuleScope(Scope):
    """\
    Scope object representing module scopes.
    """
    def __init__(self, AST, localModules={}):
        super(ModuleScope,self).__init__("Module",AST.node.nodes,None,localModules,None)
        self.ast=AST
        if AST.doc is not None:
            self.doc = AST.doc
        else:
            self.doc = ""


class ClassScope(Scope):
    """\
    Scope object representing class scopes.
    
    Determines what its base classes are, and the method resolution order. A list
    of (name,baseScopeObject) pairs is placed in self.bases. A list of scope objects
    is placed into self.allBasesInMethodResolutionOrder.
    
    Bases will be a mixture of ClassScope and ImportScope objects.
    
    These lists won't be properly set until the resolve() post-pocessing method
    has been called.
    
    Sets the following attributes:
            
    - doc        -- class's doc string, or the empty string if none.
    - bases      -- list of (name,scope object) pairs describing the class's bases
    - allBasesInMethodResolutionOrder  -- list of scope objects for the bases in method resolution order
    - ast        -- the AST for this
    """
    def __init__(self, AST, imports, localModules, rootScope, parentScope):
        super(ClassScope,self).__init__("Class",AST.code,imports,localModules,rootScope)
        self.ast=AST

        if AST.doc is not None:
            self.doc = AST.doc
        else:
            self.doc = ""
        
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
        
    def resolve(self,_resolvePass=None,roots={}):
        """\
        Resolve pass 1:
        
        * resolves bases, where passible to ClassScope objects - eg. checking if
          imports actually refer to stuff in this tree of scope objects, and
          dereferening them.
          
        Resolve pass 2:
        
        * determines the method resolution order
        """
        super(ClassScope,self).resolve(_resolvePass,roots)
        if _resolvePass==1 and len(roots):
            # resolve bases that are imports that could actually be classes in one of the root hierarchies
            newBases = []
            for baseName,base in self.bases:
                history=[]
                baseNameFrags = baseName.split(".")
                # chase through the (chain of) imports to see if we can find them
                # in the documentation object tree roots provided
                while isinstance(base,ImportScope) or base is None:
                    history.append(baseName)
                        
                    success=False
                    for rootName,rootMod in roots.items():
                        rootNameFrags=rootName.split(".")
                        head=baseNameFrags[:len(rootNameFrags)]
                        tail=baseNameFrags[len(rootNameFrags):]
                        if rootNameFrags == head:
                            try:
                                base=rootMod.find(".".join(tail))
                                baseName=baseName
                                success=True
                            except ValueError:
                                continue
                        if baseName in history:
                            continue
                    
                    if not success:
                        # ok, hit a dead end
                        break
                    if baseName in history:
                        # ok, we've gone circular
                        break
                            
                newBases.append((baseName,base))

            self.bases=newBases
        
        elif _resolvePass==2:
            # now determine the method resolution order
            self.allBasesInMethodResolutionOrder = _determineMRO(self)
            super(ClassScope,self).resolve(_resolvePass,roots)

def _determineMRO(klass):
    """\
    Pass a ClassScope object representing a class, and this method returns a
    list of scope objects presenting the base classes in method resolution order.
    
    This function applies the C3 algorithm, as used by python, to determine the
    method resolution order.
    """
    order=[klass]
    if not isinstance(klass,ClassScope):
        return order
    
    bases=[]
    for baseName,base in klass.bases:
        bases.append(base)
        
    mergedBases = [_determineMRO(base) for base in bases]
    mergedBases.extend([[base] for base in bases])
    while len(mergedBases) > 0:
        for baselist in mergedBases:
            head = baselist[0]
            foundElsewhere = [True for merged in mergedBases if (head in merged[1:])]
            if foundElsewhere == []:
                order.append(head)
                for baselist in mergedBases:
                    if baselist[0]==head:
                        del baselist[0]
                mergedBases = [baselist for baselist in mergedBases if baselist != []]
                break
        if foundElsewhere:
            raise RuntimeError("FAILURE")
    return order
    
    
class FunctionScope(Scope):
    """\
    Scope object representing a declared function.
    
    Sets the following attributes:
                    
    - doc        -- function's doc string, or the empty string if none.
    - argString  -- string describing the arguments this method takes
    - argNames   -- list of (name, annotatedName) tuples repesenting, in order, the arguments of the method
    - ast        -- the AST for this
    """
    def __init__(self, AST, imports, localModules, rootScope):
        super(FunctionScope,self).__init__("Class",None,imports,localModules,rootScope) # don't bother parsing function innards
        self.ast=AST

        if AST.doc is not None:
            self.doc = AST.doc
        else:
            self.doc = ""
        
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
    """\
    Scope object representing an import.
    
    Sets the following attributes:
                    
    - doc        -- empty string
    - importPathName  -- the full import path name leading to this entity, eg. "Axon.Component"
    """
    def __init__(self,importPathName="",imports=None):
        if importPathName=="" and imports==None:
            imports=self
        super(ImportScope,self).__init__("Module",None,imports,[],None)  # its an opaque imported module, no local modules, etc to concern ourselves with
        
        self.doc = ""
        self.importPathName=importPathName
        
    def resolveName(self,provisionalName):
        """Returns the full (real) path name of this import"""
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
    """\
    Scope object representing something that wasn't parsed - eg. a symbol
    that refers to something that isn't a simple class, function etc.
    
    Sets the following attributes:
    
    - doc  -- empty string
    - ast  -- the AST tree for this unparsed entity
    """
    def __init__(self, AST, imports, localModules, rootScope):
        super(UnparsedScope,self).__init__("Unparsed",AST,imports,localModules,rootScope)
        self.doc=""
        self.ast=AST
        


class ModuleDoc(ModuleScope):
    def __init__(self, moduleName, filePath, localModules={}):
        """\
        Arguments:
        
        - moduleName  -- the full module pathname for this module
        - filePath    -- the full filepath of this module or this subdirectory
        - localModules -- dictionary mapping localmodule pathnames to the global namespace; eg. Chassis -> Kamaelia.Chassis
        """
        self.ignoreFilenames=[".svn","__init__.py"]
        
        if isdir(filePath):
            subModules,localModules,AST = self.scanSubdirs(filePath,moduleName)
            
        else:
            subModules = {}
            localModules = localModules
            AST = self.scanSelfOnly(filePath)
        
        # now we've already done children and have built up localModule name mappings
        # we can initialise ourselves properly (parsing the AST)
        print "Parsing:",moduleName
        
        super(ModuleDoc,self).__init__(AST,localModules)
        self.localModules = localModules    # just to be safe
        
        # add "module" attribute to ourselves
        self.module = moduleName
        
        # go identify __kamaelia_components__ and __kamaelia_prefabs__ and refashion them
        self.identifyComponentsAndPrefabs()
        self.augmentComponentsAndPrefabs()
        
        # add "module" attribute to all our non import children too
        for (symbol,item) in self.listAllNonImports():
            item.module = moduleName
        
        # merge subModules into self.symbols
        for name in subModules:
            self.assign(name, subModules[name])


    def scanSubdirs(self, filePath,moduleName):
        subModules={}
        
        # try to ingest __init__.py
        filename=pathjoin(filePath,"__init__.py")
        if exists(filename):
            AST=compiler.parseFile(filename)
        else:
            AST=compiler.parse("")
            
        subdirs = [name for name in os.listdir(filePath) if isdir(pathjoin(filePath,name)) and name not in self.ignoreFilenames]
        sourcefiles = [name for name in os.listdir(filePath) if not name in subdirs and name[-3:]==".py" and name not in self.ignoreFilenames]
        
        localModules={} # we're a subdirectory, ignore what we were passed
        
        # recurse througth directory contents, doing subdirectories first
        # ignore localModules we were passed; and build our own as the localModules of all children
        for subDir in subdirs:
            subModName=moduleName+"."+subDir
            subMod = ModuleDoc(subModName, pathjoin(filePath,subDir))
            subModules[subDir] = subMod
            # merge the subdir's local modules into our own local modules
            for key in subMod.localModules:
                localModules[subDir+"."+key] = subMod.localModules[key]
                
        # add localstuff to localModules too
        for file in sourcefiles:
            modName=file[:-3] # strip ".py"
            localModules[modName] = moduleName+"."+modName
            
        # now go through other module files in this directory with us
        for file in sourcefiles:
            modName=file[:-3]
            mod = ModuleDoc(moduleName+"."+modName, pathjoin(filePath,file), localModules)
            subModules[modName] = mod
            
        return subModules,localModules,AST
            
    def scanSelfOnly(self,filePath):
        # ingest file as it stands
        assert(exists(filePath))
        assert(isfile(filePath))
        AST=compiler.parseFile(filePath)
        return AST

    def identifyComponentsAndPrefabs(self):
        try:
            components = self.find("__kamaelia_components__")
            components = _stringsInList(components.ast)
        except (ValueError,TypeError):
            components = []
            
        try:
            prefabs = self.find("__kamaelia_prefabs__")
            prefabs = _stringsInList(prefabs.ast)
        except (ValueError,TypeError):
            prefabs = []
            
        self.components = components
        self.prefabs = prefabs
        
        
    def augmentComponentsAndPrefabs(self):
        # parse Inbox/Outbox declarations for components
        for name,component in self.listAllComponents():
            component.isComponent=True
            
            try:
                inboxes = component.find("Inboxes")
                component.inboxes = _parseBoxes(inboxes.ast)
            except ValueError:
                component.inboxes = []
        
            try:
                outboxes = component.find("Outboxes")
                component.outboxes = _parseBoxes(outboxes.ast)
            except ValueError:
                component.outboxes = []
        
        # nothing much to do for prefabs
        for name,prefab in self.listAllPrefabs():
            prefab.isPrefab=True

    def listAllComponents(self,**options):
        return [ (name,cls) for (name,cls) in self.listAllClasses(**options) if name in self.components ]
    
    def listAllPrefabs(self,**options):
        return [ (name,fnc) for (name,fnc) in self.listAllFunctions(**options) if name in self.prefabs ]

    def listAllComponentsAndPrefabs(self,**options):
        return self.listAllComponents(**options) + self.listAllPrefabs(**options)
    
    def listAllModulesIncSubModules(self):
        modules = [(self.module, self)]
        for (_,m) in self.listAllModules(recurseDepth=0):
            modules.extend(m.listAllModulesIncSubModules())
        return modules
    
    def listAllComponentsIncSubModules(self):
        components = [(self.module+"."+name, item) for (name,item) in self.listAllComponents(recurseDepth=5)]
        for (_,m) in self.listAllModules(recurseDepth=0):
            components.extend(m.listAllComponentsIncSubModules())
        return components
    
    def listAllPrefabsIncSubModules(self):
        prefabs = [(self.module+"."+name, item) for (name,item) in self.listAllPrefabs(recurseDepth=5)]
        for (_,m) in self.listAllModules(recurseDepth=0):
            prefabs.extend(m.listAllPrefabsIncSubModules())
        return prefabs

# ------------------------------------------------------------------------------


def _stringsInList(theList):
    # flatten a tree structured list containing strings, or possibly ast nodes
    if isinstance(theList, (ast.Tuple,ast.List)):
        theList = theList.nodes
    elif isinstance(theList, (list,tuple)):
        theList = theList
    else:
        raise TypeError("Not a tuple or list")
        
    found = []
    for item in theList:
        if isinstance(item,str):
            found.append(item)
        elif isinstance(item, ast.Name):
            found.append(item.name)
        elif isinstance(item,(list,tuple,ast.Node)):
            found.extend(_stringsInList(item))
    return found


def _parseBoxes(node):
    if isinstance(node, ast.Dict):
        return _parseDictBoxes(node)
    elif isinstance(node, ast.List):
        return _parseListBoxes(node)

def _parseDictBoxes(dictNode):
    boxes = []
    for (lhs,rhs) in dictNode.items:
        if isinstance(lhs, ast.Const) and isinstance(rhs, ast.Const):
            name = lhs.value
            desc = rhs.value
            if isinstance(name, str) and isinstance(desc, str):
                boxes.append((name,desc))
    return dict(boxes)
            
def _parseListBoxes(listNode):
    boxes = []
    for item in listNode.nodes:
        if isinstance(item, ast.Const):
            name = item.value
            if isinstance(name, str):
                boxes.append((name,''))
    return list(boxes)

# ------------------------------------------------------------------------------


# METHODS PROVIDING
# BACKWARD COMPATIBILITY WITH OLD Repository.py

def GetAllKamaeliaComponentsNested(baseDir=None):
    """\
    Return a nested structure of dictionaries. Keys are module names. Values
    are either nested sub-dictionaries, or component names. The structure
    maps directly to the module directory structure.

    If no base-directory is specified, then the current Kamaelia installation
    will be scanned.

    Keyword arguments:

    - baseDir  -- Optional. Top directory of the code base to scan, or None for the current Kamaelia installation (default=None)
    """
    flatList = GetAllKamaeliaComponents(baseDir)
    flatList.sort()
    return _nest(flatList)

def GetAllKamaeliaComponents(baseDir=None):
    """\
    Return a flat dictionary mapping module paths to lists of component names
    contained in that module. Module paths are tuples containing each element
    of the path, eg ("Kamaelia","File","Reading")

    If no base-directory is specified, then the current Kamaelia installation
    will be scanned.

    Keyword arguments:

    - baseDir  -- Optional. Top directory of the code base to scan, or None for the current Kamaelia installation (default=None)
    """
    if baseDir is None:
        import Kamaelia
        baseDir=os.path.dirname(Kamaelia.__file__)
    
    rDocs = ModuleDoc("Kamaelia",baseDir)
    
    names = {}
    for name in [name for (name,item) in rDocs.listAllComponentsIncSubModules()]:
        path,name = tuple(name.split(".")[:-1]), name.split(".")[-1]
        names[path] = names.get(path,[]) + [name]
    return names

def GetAllKamaeliaPrefabsNested(baseDir=None):
    """\
    Return a nested structure of dictionaries. Keys are module names. Values
    are either nested sub-dictionaries, or prefab names. The structure
    maps directly to the module directory structure.

    If no base-directory is specified, then the current Kamaelia installation
    will be scanned.

    Keyword arguments:

    - baseDir  -- Optional. Top directory of the code base to scan, or None for the current Kamaelia installation (default=None)
    """
    flatList = GetAllKamaeliaPrefabs(baseDir)
    flatList.sort()
    return _nest(flatList)
    
def GetAllKamaeliaPrefabs(baseDir=None):
    """\
    Return a flat dictionary mapping module paths to lists of prefab names
    contained in that module. Module paths are tuples containing each element
    of the path, eg ("Kamaelia","File","Reading")

    If no base-directory is specified, then the current Kamaelia installation
    will be scanned.

    Keyword arguments:

    - baseDir  -- Optional. Top directory of the code base to scan, or None for the current Kamaelia installation (default=None)
    """
    if baseDir is None:
        import Kamaelia
        baseDir=os.path.dirname(Kamaelia.__file__)
    
    rDocs = ModuleDoc("Kamaelia",baseDir)
    
    names = {}
    for name in [name for (name,item) in rDocs.listAllPrefabsIncSubModules()]:
        path,name = tuple(name.split(".")[:-1]), name.split(".")[-1]
        names[path] = names.get(path,[]) + [name]
    return names


def _nest(flatList):
    nested={}
    for path in flatList:
        leafModuleName=path[-2]
        componentName=path[-1]
        node=nested
        
        for element in path[:-2]:
            if element in node:
                assert(isinstance(node[element],dict))
            else:
                node[element]=dict()
            node=node[element]
            
        if leafModuleName in node:
            assert(isinstance(node[leafModuleName],list))
        else:
            node[leafModuleName]=list()
        node[leafModuleName].append(componentName)
        
    return nested



        
if __name__ == "__main__":
    file="/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/File/Reading.py"
    #file="/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/Chassis/Pipeline.py"
    #file="/home/matteh/kamaelia/trunk/Code/Python/Kamaelia/Kamaelia/Protocol/RTP/NullPayloadRTP.py"
    modDocs = ModuleDoc("Kamaelia.File.Reading",file,{})

    print "MODULE:"
    print modDocs.doc
    
    print 
    print "PREFABS:"
    for (name,item) in modDocs.listAllPrefabs():
        print name,item.argString
        
    print
    print "COMPONENTS:"
    for (name,item) in modDocs.listAllComponents():
        print name
        print "Inboxes:  ",item.inboxes
        print "Outboxes: ",item.outboxes
        for (name,meth) in item.listAllFunctions():
            print name + "(" + meth.argString + ")"
        print

    import pprint
    pprint.pprint(GetAllKamaeliaComponents(),None,4)
    print
    print "*******************************************************************"
    print
    pprint.pprint(GetAllKamaeliaComponentsNested(),None,4)
    print
    print "*******************************************************************"
    print
    pprint.pprint(GetAllKamaeliaPrefabs(),None,4)
    print
    print "*******************************************************************"
    print
    pprint.pprint(GetAllKamaeliaPrefabsNested(),None,4)
    print
    print "*******************************************************************"
