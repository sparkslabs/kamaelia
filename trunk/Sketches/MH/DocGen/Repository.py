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
    
   >>> docTree=Repository.SourceTreeDocs()

And look up a particular module::

   >>> m=docTree.flatModules[('Kamaelia','Util','Console')]
   >>> m
   <Kamaelia.Support.Data.Repository.ModuleDocs object at 0x2aaaac4c7790>
   
Then find components declared in that module::

   >>> c=m.components[0]
   >>> c
   <Kamaelia.Support.Data.Repository.KamaeliaComponentDocs object at 0x2aaaac6d61d0>
    
And look at properties of that component::
    >>> c.name
    'ConsoleEchoer'
    >>> c.module
    'Kamaelia.Util.Console'
    >>> c.inboxes
    {'control': 'Shutdown signalling', 'inbox': 'Stuff that will be echoed to standard output'}
    >>> c.outboxes
    {'outbox': "Stuff forwarded from 'inbox' inbox (if enabled)", 'signal': 'Shutdown signalling'}
    >>> print c.docString
       ConsoleEchoer([forwarder][,use_repr]) -> new ConsoleEchoer component.
    
       A component that outputs anything it is sent to standard output (the
       console).
    
       Keyword arguments:
    
       - forwarder  -- incoming data is also forwarded to "outbox" outbox if True (default=False)
       - use_repr   -- use repr() instead of str() if True (default=False)
    
This includes methods defined in it::

    >>> meth=c.methods[0]
    >>> meth.name
    '__init__'
    >>> meth.module
    'Kamaelia.Util.Console'
    >>> meth.docString
    'x.__init__(...) initializes x; see x.__class__.__doc__ for signature'

We can ask for a string summarising the method's arguments::

    >>> meth.argString
    'self[, forwarder][, use_repr]'

Or a list naming each argument, consisting of (argname, summary-representation)
pairs::
    
    >>> meth.args
    [('self', 'self'), ('forwarder', '[forwarder]'), ('use_repr', '[use_repr]')]



Obtaining introspection data
----------------------------

To get a detailed introspection you create a SourceTreeDocs object. You can
either point it at a specific directory, or just let it introspect the currently
installed Kamaelia repository.

You can specify the module path corresponding to that directory (the "root
name"). The default is simply "Kamaelia". If for example, you point it at the
Kamaelia.Chassis directory; you should explain that the root name is
"Kamaelia.Chassis". Or if, for example, you are using this code to document
Axon, you would specify a root name of "Axon".

Finally you can also specify a list of filenames to be excluded.


    
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

The SourceTreeDoc object contains dictionaries pointing you at various ModuleDocs
objects. These in turn contain ClassDocs, FunctionDocs, PrefabDocs and ComponentDocs
objects. ComponentDocs and ClassDocs objects will contain MethodDocs objects:

* SourceTreeDoc object

  * ModuleDocs objects
  
    * ComponentDocs objects
    
      * MethodDocs objects
      
    * PrefabDocs objects
    
    * ClassDocs objects
    
      * MethodDocs objects
      
    * FunctionDocs objects

**SourceTreeDocs** objects have the following attributes:

* *nestedModules* - a nested set of dictionaries reflecting the structure of
  modules. At each level, the key is the module name. The value is a list of
  other dicts and ModuleDocs objects.

  For example, nestedModules["Kamaelia"]["Chassis"]["Pipeline"] would return
  the ModuleDocs object documenting the module Kamaelia.Chassis.Pipeline

* *flatModules* - a simple flat dictionary. The keys are tuples giving the
  full path of the module. The value is a corresponding ModuleDocs object.

  For example the key ("Kamaelia","Chassis","Pipeline") will return a
  ModuleDocs object documenting the module Kamaelia.Chassis.Pipeline

  
**ModuleDocs** objects contain the following attributes:

* *docString* - the python doc string for the module

* *components* - list of KamaeliaComponentDocs objects describing prefabs
  defined in this module

* *prefabs* - list of KamaeliaPrefabDocs objects describing prefabs defined in
  this module
  
* *classes* - list of ClassDocs objects describing non-component classes
  defined in this module

* *functions* - list of FunctionDocs objects describing functions defined in
  this module (not including prefabs)

  
**KamaeliaComponentDocs** objects contain the following attributes:

* *name* - the name of the component (eg. "Pipeline")

* *module* - the full module name for where it is located - for example:
  "Kamaelia.Chassis.Pipeline"
  
* *docString* - the python doc string for the component

* *inboxes* and *outboxes* - dicts mapping inbox/outbox names to any associated
  documentation string or an empty string. For example: {"inbox":"Send data here"}

* *methods* - list of MethodDocs objects describing methods defined in this
  component (basically the same as FunctionDocs objects)

  
**KamaeliaPrefabDocs**, **FunctionDocs** and **MethodDocs** objects are all, in practice,
the same format. They contain the following attributes:

* *name* - the name of the prefabs (eg. "RateControlledFileReader")

* *module* - the full module name for where it is located - for example:
  "Kamaelia.File.Reading"

* *docString* - the python doc string for the prefab

* *argString* - a string representation of the arguments the function/method/prefab
  takes. Square brackets are used to indicate optionality, and single and
  double asterisks to indicate argument and dictionary lists (as in normal
  python syntax). For example: "self, \*components"

* *args* - an ordered list detailing the individual arguments the
  function/method/prefab takes. Each tuple is a pair (name,argStringRepresentation)
  giving the argument name, and the 'argString' style representation.

  
**ClassDocs** objects contain the following attributes:

* *name* - the name of the component (eg. "SourceTreeDocs")

* *module* - the full module name for where it is located - for example:
  "Kamaelia.Support.Data.Repository"
  
* *docString* - the python doc string for the component

* *methods* - list of MethodDocs objects describing methods defined in this
  component (basically the same as FunctionDocs objects)



Implementation Details
----------------------

This code uses the python compiler.ast module to parse the source of python
files, rather than import them. This allows introspection of code that might not
necessarily run on the system at hand - perhaps because not all dependancies can
be satisfied.

A consequence of this is that if something is created by executed statements,
rather than simply declared, it will not be picked up. For example::

    def foo():
        class MyComponent(component):
            pass
        return MyComponent

    wontBePickedUpByRepositoryIntrospection = foo()
    
    alsoWontBePickedUp = lambda : "burble"

Functions and classes declared within if statement will also not be found::

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


import compiler
from compiler import ast
import os

class SourceTreeDocs(object):
    """\
    SourceTreeDocs([baseDir][,rootName][,excludeFilenames]) -> new SourceTreeDocs object

    Parses a code base to determine what modules, components, prefabs, functions
    and classes are declared in it.

    If no base-directory is specified, then the current Kamaelia installation
    will be scanned.

    self.nestedModules and self.flatModules contain the resulting data. For
    example, ``x.nestedModules["Kamaelia"]["Chassis"]["Pipeline"]`` or
    ``x.flatModules[("Kamaelia","Chassis","Pipeline")]`` will both return a
    ModuleDocs object documenting that module

    Keyword arguments:

    - baseDir           -- Optional. Top directory of the code base to scan, or None for the current Kamaelia installation (default=None)
    - rootName          -- Optional. The module path corresponding to the directory specified (default="Kamaelia")
    - excludeFilenames  -- Optional. List of filenames to be ignored (default=[])
    """
    def __init__(self, baseDir=None, rootName="Kamaelia", excludeFilenames=[]):
        super(SourceTreeDocs,self).__init__()

        # if no base directory specified, locate the base directory of the
        # current kamaelia installation
        if baseDir:
            self.baseDir = baseDir
        else:
            import Kamaelia
            self.baseDir = os.path.dirname(Kamaelia.__file__)
            
        self.excludeFilenames = excludeFilenames

        # build the initial path to the specified 'root' in the dictionaries
        # of modules
        root=rootName.split(".")
        self.flatModules={}
        self.nestedModules={}
        
        nested=self.nestedModules
        for node in root:
            nested[node] = {}
            nested=nested[node]

        # recurse through the source directories ingesting them
        self._ingest(self.baseDir, self.flatModules, nested, base=root)
        self._build(self.nestedModules, [], self.flatModules)
        
        
    def _ingest(self,dirName,flatModules,nestedModules,base):
        """\
        **Internal method**
        
        Recursively scans the code base specified by dirName and ingests any
        modules found. Skips any filenames specified for exclusion at
        initialisation.

        Keyword arguments:

        - dirName        -- directory to be scanned for python modules
        - flatModules    -- dict into which (module-path,ModuleDocs object) pairs will be inserted
        - nestedModules  -- dict into which (module-name,ModuleDocs object) and (module-name,sub-dict) pairs will be inserted
        """
        dirEntries = os.listdir(dirName)
        containsPythonFiles = False
        
        for filename in dirEntries:
            filepath = os.path.join(dirName, filename)
            if filename in self.excludeFilenames:
                continue
            
            elif os.path.isdir(filepath):
                subTree = {}
                subBase = base + [filename]
                foundPythonFiles = self._ingest(filepath, flatModules, subTree, subBase)
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

    def _build(self, subtree, pathToHere, namesBelowHere):
        # iterate/recurse through the modules ingested and get each to build its
        # documentation, resolving references to other modules too

        for name in subtree:
            if isinstance(subtree[name], dict):
                newPath = list(pathToHere) + [name]

                # copy items that lie in teh same subtree
                subsetOfNames = {}
                for itemname in namesBelowHere.keys():
                    if itemname[:len(newPath)] == newPath:
                        subsetOfNames[itemname] = namesBelowHere[itemname]

                self._build(subtree[name], newPath, subsetOfNames)
                    
            else:
                moduleDocObj = subtree[name]
                moduleDocObj.buildAndResolve(pathToHere, namesBelowHere)
        

def isPythonFile(Path, File):
    """Returns True if the specified file looks like it is a python source file"""
    FullEntry = os.path.join(Path, File)
    if os.path.isfile(FullEntry):
        if len(File) > 3:
            if File[-3:] == ".py":
                return True
    return False


class ClassDocs(object):
    """\
    Information about a declared class.

    See module level docs for information on the attributes this will be loaded
    up with.
    """
    pass

class FunctionDocs(object):
    """\
    Information about a declared function/method/prefab.

    See module level docs for information on the attributes this will be loaded
    up with.
    """
    pass

MethodDocs         = FunctionDocs
KamaeliaPrefabDocs = FunctionDocs

class KamaeliaComponentDocs(ClassDocs):
    """\
    Information about a declared component.

    See module level docs for information on the attributes this will be loaded
    up with.
    """
    pass

ANY=object()

class ModuleDocs(object):
    """\
    ModuleDocs(filepath, modulePath) -> new ModuleDocs object.

    Inspects the named python sourcefile and detects components, prefabs,
    classes and functions declared in it. Once initalised:

    - **self.docString**  is the module level documentation string
    - **self.prefabs, **self.components**, **self.classes**, and **self.functions**
      are lists of prefabs, components, classes and functions declared in the module.

    Keyword arguments:

    - filepath    -- full filepath of the python source file
    - modulePath  -- tuple of the path of this module, eg ("Kamaelia","File","Reading") or ("Kamaelia","Chassis") ... note there's not "__init__"
    """
    def __init__(self, filepath, modulePath):
        super(ModuleDocs,self).__init__()
        self.modulePath = modulePath
        assert("__init__" not in modulePath)
        assert("__init__.py" not in modulePath)

        self._AST = compiler.parseFile(filepath)


    def buildAndResolve(self, pathToHere, namesBelowHere):
        self._extractModuleDocString()
        self._findKamaeliaEntities()
        self._findOtherEntities()
        
        self.prefabs = []
        for prefabName in self._prefabNames:
            doc = self._documentNamedFunction(prefabName, self.modulePath)
            self.prefabs.append(doc)
        
        self.components = []
        for componentName in self._componentNames:
            doc = self._documentNamedComponent(componentName, self.modulePath)
            self.components.append(doc)
        
        self.classes = []
        for className in self._otherClassNames:
            doc = self._documentNamedClass(className, self.modulePath)
            self.classes.append(doc)
            
        self.functions = []
        for funcName in self._otherFunctionNames:
            doc = self._documentNamedFunction(funcName, self.modulePath)
            self.functions.append(doc)


    def _extractModuleDocString(self):
        assert(isinstance(self._AST, ast.Module))
        self.docString = self._AST.doc or ""

    def _findKamaeliaEntities(self):
        # find the __kamaelia_compoents__ declaration
        stmt = self._AST.getChildren()[1]
        assert(isinstance(stmt, ast.Stmt))
        components = self._findAssignments( "__kamaelia_components__",
                                           stmt,
                                           [ast.Class, ast.Function, ast.Module]
                                         )
        prefabs    = self._findAssignments( "__kamaelia_prefabs__",
                                           stmt,
                                           [ast.Class, ast.Function, ast.Module]
                                         )

        # flatten the results
        components = _stringsInList([x for (_,x) in components])
        prefabs    = _stringsInList([x for (_,x) in prefabs])

        # and remove any repeats (unlikely)
        self._componentNames = dict([(x,x) for x in components]).keys()
        self._prefabNames = dict([(x,x) for x in prefabs]).keys()
        
    def _findOtherEntities(self):
        stmt = self._AST.getChildren()[1]
        assert(isinstance(stmt, ast.Stmt))
        
        # find other class, method etc top level declarations in the source
        functions = self._findFunctions(ANY, stmt, [ast.Class, ast.Module, ast.Function, ast.If])
        classes   = self._findClasses(ANY, stmt, [ast.Class, ast.Module, ast.Function, ast.If])
        
        # convert from ast to name
        functions = [func.name for func in functions]
        classes   = [clss.name for clss in classes]
        
        # remove anything already matched up as being a prefab or component
        functions = [name for name in functions if name not in self._prefabNames]
        classes   = [name for name in classes   if name not in self._componentNames]

        self._otherFunctionNames = functions
        self._otherClassNames   = classes
        

    def _findAssignments(self, target, node, ignores):
        # recurse to find an assignment statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Assign):
                for lhs in child.nodes:
                    if isinstance(lhs, ast.AssName):
                        if lhs.name == target or target==ANY:
                            rhs = child.expr
                            found.append((lhs.name, rhs))
                        
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self._findAssignments(target, child, ignores)
                
        return found

    def _findFunctions(self, target, node, ignores):
        # recurse to find a function statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Function):
                if child.name == target or target == ANY:
                    found.append(child)
            
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self._findFunctions(target, child, ignores)
                
        return found
    
    def _documentNamedFunction(self, prefabName, modulePath):
        fnode = self._findFunctions( prefabName,
                                    self._AST.getChildren()[1],
                                    [ast.Class, ast.Function, ast.Module]
                                  )
        assert(len(fnode)==1)
        fnode=fnode[0]
        assert(prefabName == fnode.name)
        return self._documentFunction(fnode, modulePath)
        
    def _documentFunction(self, fnode, modulePath):
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

    
    def _findClasses(self, target, node, ignores):
        # recurse to find a function statement for the given target
        # but ignoring any branches matching the node classes listed
        
        found=[]
        for child in node.getChildren():
            if isinstance(child, ast.Class):
                if child.name == target or target == ANY:
                    found.append(child)
            
            elif not isinstance(child, tuple(ignores)) and \
                     isinstance(child, ast.Node):
                found += self._findClasses(target, child, ignores)
                
        return found
    
    def _findBoxDecl(self, codeNode, boxTypeName):
        for child in codeNode.getChildren():
            if isinstance(child, ast.Assign):
                lhs = child.nodes[0]
                if isinstance(lhs, ast.AssName):
                    if lhs.name == boxTypeName:
                        rhs = child.expr
                        if isinstance(rhs, ast.Dict):
                            return self._parseDictBoxes(rhs)
                        elif isinstance(rhs, ast.List):
                            return self._parseListBoxes(rhs)
        return []
                
    def _parseDictBoxes(self, dictNode):
        boxes = []
        for (lhs,rhs) in dictNode.items:
            if isinstance(lhs, ast.Const) and isinstance(rhs, ast.Const):
                name = lhs.value
                desc = rhs.value
                if isinstance(name, str) and isinstance(desc, str):
                    boxes.append((name,desc))
        return dict(boxes)
                
    def _parseListBoxes(self, listNode):
        boxes = []
        for item in listNode.nodes:
            if isinstance(item, ast.Const):
                name = item.value
                if isinstance(name, str):
                    boxes.append((name,''))
        return list(boxes)
    
    def _documentNamedComponent(self, componentName, modulePath):
        cnode = self._findClasses( componentName,
                                  self._AST.getChildren()[1],
                                  [ast.Class, ast.Function, ast.Module]
                                )
        assert(len(cnode)>=1)
        cnode = cnode[0]
        assert(componentName == cnode.name)
        cDoc = cnode.doc or ""
        inboxDoc  = self._findBoxDecl(cnode.code, "Inboxes")
        outboxDoc = self._findBoxDecl(cnode.code, "Outboxes")
        
        methodNodes = self._findFunctions(ANY, cnode.code, [ast.Class, ast.Function, ast.Module])
        methods = [self._documentFunction(node, modulePath) for node in methodNodes]
        
        theComp = KamaeliaComponentDocs()
        theComp.name = componentName
        theComp.docString = cDoc
        theComp.inboxes = inboxDoc
        theComp.outboxes = outboxDoc
        theComp.methods = methods
        theComp.module = ".".join(modulePath)
        return theComp
    
    def _documentNamedClass(self, className, modulePath):
        cnode = self._findClasses( className,
                                  self._AST.getChildren()[1],
                                  [ast.Class, ast.Function, ast.Module, ast.If]
                                )
        assert(len(cnode)>=1)
        cnode = cnode[0]
        assert(className == cnode.name)
        cDoc = cnode.doc or ""
        
        methodNodes = self._findFunctions(ANY, cnode.code, [ast.Class, ast.Function, ast.Module])
        methods = [self._documentFunction(node, modulePath) for node in methodNodes]

        theClass = ClassDocs()
        theClass.name = className
        theClass.docString = cDoc
        theClass.methods = methods
        theClass.module = ".".join(modulePath)
        return theClass


def _stringsInList(theList):
    # flatten a tree structured list containing strings, or possibly ast nodes
    
    if isinstance(theList,ast.Node):
        theList = theList.nodes
        
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
    """\
    Return a nested structure of dictionaries. Keys are module names. Values
    are either nested sub-dictionaries, or component names. The structure
    maps directly to the module directory structure.

    If no base-directory is specified, then the current Kamaelia installation
    will be scanned.

    Keyword arguments:

    - baseDir  -- Optional. Top directory of the code base to scan, or None for the current Kamaelia installation (default=None)
    """
    rDocs = SourceTreeDocs(baseDir)
    moduleTree = rDocs.nestedModules
    reduced = _reduceToNames(moduleTree, keepComponents=True, keepPrefabs=False)
    if reduced["Kamaelia"].has_key("Support"):
        del reduced["Kamaelia"]["Support"]
    return reduced

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
    rDocs = SourceTreeDocs(baseDir)
    modules = rDocs.flatModules
    return _reduceToNames(modules, keepComponents=True, keepPrefabs=False)

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
    rDocs = SourceTreeDocs(baseDir)
    moduleTree = rDocs.nestedModules
    reduced = _reduceToNames(moduleTree, keepComponents=False, keepPrefabs=True)
    if reduced["Kamaelia"].has_key("Support"):
        del reduced["Kamaelia"]["Support"]
    return reduced
    
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
    rDocs = SourceTreeDocs(baseDir)
    modules = rDocs.flatModules
    return _reduceToNames(modules, keepComponents=False, keepPrefabs=True)


def _reduceToNames(tree, keepComponents=True, keepPrefabs=True):
    """\
    **Internal method**

    Transforms a full module documentation object tree (nested dictionaries)
    converting documentation objects down to simple names of components and
    prefabs. Module, function and classes are filtered out.

    The original structure of nested dictionaries is maintained. Only the leaves
    are converted.

    Keyword arguments:

    - tree           -- The documentation tree (nested dictionaries)
    - keepComponents -- Optional. Set to True (default=True) to include components in the final output.
    - keepPrefabs    -- Optional. Set to True (default=True) to include prefabs in the final output.
    """
    output={}
    for key in tree.keys():
        value=tree[key]
        if isinstance(value,dict):
            output[key] = _reduceToNames(value, keepComponents, keepPrefabs)
        elif isinstance(value, ModuleDocs):
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
    modDocs.buildAndResolve(["Kamaelia","File","Reading"],{})

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
    print
    print "*******************************************************************"
    print
    rDocs = SourceTreeDocs(None)
    pprint.pprint(rDocs.flatModules)
    print
    pprint.pprint(rDocs.nestedModules)
    print
