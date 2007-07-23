import inspect

"""
Shard constructor that treats shard objects,
named functions and lists of strings (code) equivalently

Subclass to create more specific connectors, e.g.
branching, looping, methods, function calls, etc.
"""

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
        return type(c[0]) == type('') if c else True
    else: return False

def isfunction(f):
    """
    Tests if argument is a function
    """

    return callable(f)


class DependencyError(Exception): pass

indentation = "    "
nl = "\n"

class shard(object):

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


    # instance methods
    def __init__(self, name = None, annotate = True, function = None,
                        code = None, shards = [], indent = 0):
        """
        Initialisation to create shards from lines of code, existing functions,
        or a combination of these and existing shard objects

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

        super(shard, self).__init__()

        self.indent = indent

        if function:
            self.name = function.func_name
            self.code = self.addindent(self.getshard(function), indent)
            #self.shards = self.makeShards([function])

        elif code:
            self.name = name if name else self.namer.next()
            self.code = self.addindent(code, indent)
            #self.shards = self.makeShards([code])

        else:
            self.name = name if name else self.namer.next()
            self.code = []
            #self.shards = self.makeShards(shards)
            for s in self.makeShards(shards):
                if annotate:
                    self.code += self.addindent(s.annotate(), indent)
                else:
                    self.code += self.addindent(s.code, indent)


    def makeShards(self, things):
        """
        Converts functions or lines of code to shard objects

        Arguments:
        things = any mix of shard objects, functions or lines
                      of code to convert, in a sequence

        Returns:
        list of inline shards equivalent to arguments
        """

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
        inlines = set(ishards.keys() if isinstance(ishards, dict) else ishards)

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

        return [c[len(lines[0]) - len(lines[0].lstrip()):] for c in lines] # remove leading indentation


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


    def writeFile(self, filename = None):
        """
        Writes code from this shard into a file.

        Arguments:
        filename = filename to write to. No checking of name clashes
                          is performed, defaults to shard object name with
                          a .py extension

        Returns:
        file containing shard code
        """

        if not filename:
            filename = self.name + '.py'

        file = open(filename,"w")
        file.writelines(self.code)
        file.close()

        return file



class docShard(shard):

    def __init__(self, name = None, annotate = False, docstring = '', shards = []):
        """
        As shard constructor, but additionally sets a self.docstring
        attribute to be a list of the lines of the docstring, indented one
        level further than given indentation

        Additional argument:
        docstring = formatted string of comments, default is empty
        """

        super(docShard, self).__init__(name = name, annotate = annotate, shards = shards)

        self.docstring = self.makedoc(docstring) if docstring else []


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
