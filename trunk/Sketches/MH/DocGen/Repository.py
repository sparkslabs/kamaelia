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
import sys

from ImportTracking import Scope
from ImportTracking import ModuleScope
from ImportTracking import ClassScope
from ImportTracking import ImportScope
from ImportTracking import FunctionScope
from ImportTracking import UnparsedScope

from os.path import isdir
from os.path import isfile
from os.path import exists
from os.path import join as pathjoin

class ModuleDoc(ModuleScope):
    def __init__(self, moduleName, filePath, localModules={}):
        """\
        Arguments:
        
        - moduleName  -- the full module pathname for this module
        - filePath    -- the full filepath of this module or this subdirectory
        - localModules -- dictionary mapping localmodule pathnames to the global namespace; eg. Chassis -> Kamaelia.Chassis
        """
        self.ignoreFilenames=[".svn"]
        
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
        return self.listAllComponents() + self.listAllPrefabs(**options)
    
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
    
    return [name.split(".") for (name,item) in rDocs.listAllComponentsIncSubModules()]

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
    
    return [name.split(".") for (name,item) in rDocs.listAllPrefabsIncSubModules()]


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
