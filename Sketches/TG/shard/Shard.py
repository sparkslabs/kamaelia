
"""
Shard System:
----------------------

The shard system is a code generator that combines
fragments of existing components into new ones. These fragments
are called shards and may be pasted 'inline' into generated
functions, etc. or added as complete functions or methods into a class
or module. This system is fairly low-level and requires a considerable amount
of construction when used 'as-is', future work could provide a text-based
or GUI frontend to the system.

A full example is the reconstruction of the MagnaDoodle
component (found in Kamaelia.UI.Pygame) in MagnaGen.py, it uses
both inline and method shards.
An interface for GUI components can be found in ShardGen.py,
along with a simple example.

The system builds a hierarchy of shards, with each object
containing the code it will output. The constructor is generally
the only method that will be used; it takes task-specific
arguments and usually a list of child shards to include. These
are documented in the class docstring.

This is the base shard constructor that accepts any combination
of the following as child shards: shard objects, function objects
and lists of strings (of code).

Subclass this to create more specific connectors, e.g.
branching, looping, methods, function calls, etc.
Simple examples are the docShard class below, and the
classes in LoopShard.py and BranchShard.py. More complex
examples are in ClassShard.py and PygameComponentShard.py.


Shard Dependencies:
---------------------------------

More complex shards may require specific inline or function shards to fill
certain slots, e.g. the PygameComponentShard requires an event handling
shard. These requirements may be declared and checked for with the
dependency handling functions provided.
These are:

* The exception DependencyError, thrown in the constructor when a
dependency is not supplied

* Instance method checkDependencies, which confirms that both shard and
inline shard dependencies are satisfied and throws a DependencyError if they
are not

* Classmethods addReqMethods, addReqIShards, remReqMethods and
remReqIShards, which add or remove required method/function shards
and inline shards from the  requiredMethods and requiredIShards sets


Shard interface:
-------------------------

All shard subclasses MUST obey the following:

* Inherit from the shard base class or a subclass

* Provide a constructor that generates the relevant code and stores
it as a list of lines terminated by newlines in a self.code attribute

* ALL constructor arguments must be named. If an argument is
absolutely required, its value should be checked in the constructor.
An ArgumentError exception is provided in this module if the check fails

* If any argument is required and checked for, it should be listed in
a self.required attribute. The convention used here is to place this
immediately before the class __init__

* Provide a self.initargs attribute that is a dictionary mapping the
constructor arguments to their default values. The convention used
here is to place this immediately before the class __init__

* If the shard permits child shards, these should be supplied as a
shards parameter only. This interface is used by graphical frontends
to ensure that children can be passed in correctly


Shard subclasses may make use of the following:

* The ArgumentError exception, used when a required parameter
is not supplied (i.e. is left at default value)

* The namegen generator which generates names for shards where
a default value will do (although this is usually done in the superclass
init call to shard)

* The dependency declaration, removal and checking methods
described in the Shard Dependencies section above

* The attributes guaranteed to be present by the shard base class:
   - self.code: list of strings of the generated code, newline terminated
   - self.shards: list of shard objects representing those passed to __init__
   - self.name: name of this shard, not necessarily unique
   - self.indent: level of indentation of the code in this shard

* The shard instance method writeFile() for outputting a shard's code

* Newline (nl) and indentation strings have been defined in this module
for convenience and consistency

"""

import inspect
import os

def namegen(name = 'shard'):
        """
        Generates names for anonymous shards
        """

        i = 0
        while True:
            yield name+str(i)
            i += 1

def iscode(c):
    """
    Tests if argument type could be lines of code,
    i.e. list of strings
    """

    if type(c) == type([]):
        if c:
            return type(c[0]) == type('')
        else:
            return True
    else: return False

def isfunction(f):
    """
    Tests if argument is a function
    """

    return callable(f)


class DependencyError(Exception): pass
class ArgumentError(Exception): pass

indentation = "    "
nl = "\n"

class shard(object):
    
    """
    Initialisation creates shards from lines of code, existing functions,
    or a combination of these and existing shard objects.
    As the shard base class, classmethods for handling and checking
    shard dependencies are also given

    Arguments:
    name = name of new shard, default None. If no name is specified
                 a default name will be generated (except where shard is
                 created from a single function, where the function's name
                 will be used)
    annotate = whether to add annotations for imported code into
                       new shard's generated code, default True
    function = if shard is being made from a single function, it can be
                     entered here. Used mainly internally to initialise function
                     objects passed into shards. If present, any following
                     arguments are ignored. Default is None
    code = as function, but if initialisation is for single code block
    shards = the shards that will compose the body of the new shard,
                   in the order in which they will be added. Arguments here
                   can be any combination of existing shard objects, function
                   objects, and lists of code lines (e.g. as imported by
                   getshard); these will be initialised as necessary
    indent = level of indentation to add to imported code, default 0

    Returns:
    shard object containing the name and code of the new shard
    """


    # generator to name anonymous shards
    namer = namegen()

    # dependency checking attributes
    requiredMethods = set()
    requiredIShards = set()

    # classmethods
    @classmethod
    def addReqMethods(self, *methods):
        """
        Adds methods to the list of requirements for this class.
        A DependencyError will be raised if these are not filled
        when the object is constructed

        Arguments:
        methods = string names of additional required methods
        """

        self.requiredMethods = self.requiredMethods | set(methods)

    @classmethod
    def addReqIShards(self, *ishards):
        """
        Adds inline shards to the list of requirements for this class.
        A DependencyError will be raised if these are not filled
        when the object is constructed

        Arguments:
        ishards = string names of additional required shards
        """

        self.requiredIShards = self.requiredIShards | set(ishards)

    @classmethod
    def remReqMethods(self, *methods):
        """
        Removes methods from list of requirements. Methods
        given but not in requirements list will be ignored

        Arguments:
        methods = string names of unrequired methods. If empty,
                          all methods will be removed
        """

        if not methods:
            self.requiredMethods = set()
        else:
            self.requiredMethods = self.requiredMethods - set(methods)

    @classmethod
    def remReqIShards(self, *ishards):
        """
        Removes inline shards from list of requirements. Shards
        given but not in requirements list will be ignored

        Arguments:
        ishards = string names of unrequired shards. If empty,
                        all shards will be removed
        """

        if not ishards:
            self.requiredIShards = set()
        else:
            self.requiredIShards = self.requiredIShards - set(ishards)

    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['annotate'] = True
    initargs['function'] = None
    initargs['code'] = None
    initargs['shards'] = []
    initargs['indent'] = 0
    
    # compulsory init parameters
    required = []
    
    # instance methods
    def __init__(self, name = None, annotate = True, function = None,
                        code = None, shards = [], indent = 0):
        
        super(shard, self).__init__()
        
        self.indent = indent
        
        if function:
            self.name = function.func_name
            self.code = self.addindent(self.getshard(function), indent)
            self.shards = [function]
        
        elif code:
            if name:
                self.name = name
            else:
                self.name = self.namer.next()
            self.code = self.addindent(code, indent)
            self.shards = [code]
        
        else:
            if name:
                self.name = name
            else:
                self.name = self.namer.next()
            self.code = []
            self.shards = self.makeShards(shards)
            for s in self.shards:
                if annotate:
                    self.code += self.addindent(s.annotate(), indent)
                else:
                    self.code += self.addindent(s.code, indent)
    
    
    def makeShards(self, things = None):
        """
        Converts functions or lines of code to shard objects
        
        Arguments:
        things = any mix of shard objects, functions or lines
                      of code to convert, in a sequence. Default
                      is None, in which case self.shards is used
        
        Returns:
        list of inline shards equivalent to arguments
        """
        
        if things == None:
            things = self.shards
        
        shards = []
        for t in things:
            if isfunction(t):
                shards.append(shard(function = t))
            elif iscode(t):
                if not hasattr(self, 'name'):
                    for i in self.__dict__:
                        print i
                    print
                nm = self.name +'.' + self.namer.next()
                shards.append(shard(name = nm, code = t))
            else:
                shards.append(t)
        
        return shards
    
    
    def checkDependencies(self, mshards, ishards):
        """
        Checks that given methods and inline shards satisfy
        the dependencies listed by the class; raises a
        DependencyError if they are not

        Arguments:
        mshards = sequence of method shard objects
        ishards = list of, or dict whose keys are, the names
                        of the supplied inline shards
        """
        
        error = ""
        methods = set([s.name for s in mshards])
        if isinstance(ishards, dict):
            inlines = set(ishards.keys())
        else:
            inlines = set(ishards)
        
        if not self.requiredMethods <= methods:
            error += "need methods "+ str(self.requiredMethods - methods)
        if not self.requiredIShards <= inlines:
            error += "need ishards "+ str(self.requiredIShards - inlines)
        
        if not error == "":
            raise DependencyError, error
        
        return True
    
    
    def getshard(self, function):
        """
        Gets shard code for generation
        
        Arguments:
        function = shard function to get
        
        Returns:
        list of lines of code of function
        """
        
        # get code, throwaway def line
        lines = inspect.getsource(function).splitlines(True)[1:]
        
        # remove any whitespace lines
        lines = [line for line in lines if not line.isspace()]
        
        # remove docstrings
        doctag = r'"""'
        while True:
            if lines[0].count(doctag) % 2 == 1:
                lines.pop(0)                            # remove line with opening doctag
                while lines[0].count(doctag) % 2 == 0:
                    lines.pop(0)                        # remove lines till tag match
                lines.pop(0)                            # remove matching tag
            
            if lines[0].count(doctag) == 0:
                break                                     # no docstring, start of code
            else:                                          # docstring tags closed, continue till code line found
                lines.pop(0)
        
        # remove leading indentation
        return [c[len(lines[0]) - len(lines[0].lstrip()):] for c in lines]


    def annotate(self, delimchar = '-'):
        """
        Marks out start and end of shard code with comments
        
        Arguments:
        delimchar = single character string containing character to be used
                            in marking out shard limit across the page
        
        Returns:
        list of lines of code surrounded by delimiter comments as specified
        """
        
        start = r"# START SHARD: " + self.name + " "
        start = self.addindent([start], self.indent)[0]
        start = start.ljust(80, delimchar) + nl
        
        end = r"# END SHARD: " + self.name + " "
        end = self.addindent([end], self.indent)[0]
        end = end.ljust(80, delimchar) + nl
        
        return [start] + self.code + [end] + [nl]
    
    
    def addindent(self, lines = None, level = 1):
        """
        Indents code with spaces
        
        Arguments:
        level = number of levels to be indented, defaults to 1
        
        Returns:
        object's code attribute prefixed by specified amount of whitespace
        """
        
        if lines == None:
            lines = self.code
        
        if level < 0: # remove indentation
            level = -level
            return [ line[len(indentation*level):] for line in lines ]
        
        elif level == 0:
            return lines
        
        elif level > 0: # add indentation
            return [indentation*level + line for line in lines]
    
    
    def writeFile(self, filepath = None):
        """
        Writes code from this shard into a file.
        
        Arguments:
        filename = filename to write to. No checking of name clashes
                          is performed, defaults to shard object name with
                          a .py extension in user's home directory
        
        Returns:
        file containing shard code
        """
        
        if not filepath:
            filepath = os.sep.join([os.environ['HOME'], self.name+'.py'])
        
        file = open(filepath,"w")
        file.writelines(self.code)
        file.close()
        
        return file
    
    
    
class docShard(shard):
    
    """
    Shard creation is as shard base class, but additionally sets a
    self.docstring attribute to be a list of the lines of the docstring,
    indented one level further than given indentation

    Arguments:
    name = name of new shard, default None. If no name is specified
                 a default name will be generated
    annotate = whether to add annotations for imported code into
                       new shard's generated code, default True
    docstring = formatted string of comments, default is empty
    shards = the shards that will compose the body of the new shard,
                   in the order in which they will be added. Arguments here
                   can be any combination of existing shard objects, function
                   objects, and lists of code lines (e.g. as imported by
                   getshard); these will be initialised as necessary

    Returns:
    shard object containing the name and code of the new shard
    """
        
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['annotate'] = True
    initargs['docstring'] = ''
    initargs['shards'] = []
    
    
    def __init__(self, name = None, annotate = True, docstring = '', shards = []):
        
        super(docShard, self).__init__(name = name, annotate = annotate, shards = shards)
        
        if docstring:
            self.docstring = self.makedoc(docstring)
        else:
            self.docstring = []
    
    
    def makedoc(self, doc, indent = 0):
        """
        Creates docstring
        
        Arguments:
        doc = formatted string for docstring
        
        Returns:
        list of strings containing lines of docstring
        """
        
        tag = "\"\"\"" + nl
        docstr = tag + doc + nl + tag
        
        return self.addindent(docstr.splitlines(True), indent)
