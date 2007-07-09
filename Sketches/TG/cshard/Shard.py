from cshard import getshard, indent

"""
Rough first pass at shard constructor: aims to treat shard objects,
named functions and lists of strings (code) equivalently

Current thought is to subclass shard to create Connectors,
e.g. ifshard(shard) can construct if-statements as shards,
functionshard(shard) can replace the current makefunction, etc.
Would replace the more '2-stage' approaches so far by making
everything a shard from import.

TODO:
"""


class shard(object):
    
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
        islist = type(c) == type([])
        ofstring = type(c[0]) == type('') if c else True
        
        return islist and ofstring
    
    def isfunction(f):
        """
        Tests if argument is a function
        """
        
        return callable(f)
    
    indentation = "    "
    nl = "\n"
    namer = namegen()
    
    def __init__(self, name = None, indent = 0, annotate = False, function = None, code = None, *shards):
        """
        Initialisation to create shards from lines of code, existing functions,
        or a combination of these and existing shard objects
        
        Arguments:
        name = name of new shard, default None. If no name is specified
                     a default name will be generated (except where shard is
                     created from a single function, where the function's name
                     will be used)
        indent = level of indentation to add to imported code, default 0
        annotate = whether to add annotations for imported code into
                           new shard's generated code, default False
        function = if shard is being made from a single function, it can be
                         entered here. Used mainly internally to initialise function
                         objects passed into *shards. If present, any following
                         arguments are ignored, default is None
        code = as function, but if initialisation is for single code block
        *shards = the shards that will compose the body of the new shard,
                         in the order in which they will be added. Arguments here
                         can be any combination of existing shard objects, function
                         objects, and lists of code lines (e.g. as imported by
                         getshard); these will be initialised as necessary
        
        Returns:
        shard object containing the name and code of the new shard
        """
        
        super(Shard, self).__init__()
        
        self.indent = indent
        
        if function:
            self.name = function.name()
            self.code = getshard(f, indent)
        elif code:
            self.name = name if name else namer.next()
            self.code = code
        else:
            self.name = name if name else namer.next()
            self.code = []
            for s in shards:
                if isfunction(s):
                    s = shard(function = s)
                elif iscode(s):
                    s = shard(name = name, code = s)
                
                code += s.annotate() if annotate else s.code
    
    
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
        start = indent([start], indentlevel)[0]
        start = start.ljust(80, delimchar) + "\n"
    
        end = r"# END SHARD: " + self.name + " "
        end = indent([end], indentlevel)[0]
        end = end.ljust(80, delimchar) + "\n"
    
        return [start] + self.code + [end]
    
    def indent(self, level = 1):
        """
        Indents code with spaces
    
        Arguments:
        level = number of levels to be indented, defaults to 1
    
        Returns:
        object's code attribute prefixed by specified amount of whitespace
        """
    
        if level < 0: # remove indentation
            level = -level
            return [ line[len(indentation*level):] for line in code ]
        
        elif level == 0:
            return code
    
        elif level > 0: # add indentation
            return [indentation*level + line for line in code]
        
    