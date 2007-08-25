from Shard import *
import inspect

class classShard(docShard):

    """
    Creates a class as a shard from given components.
    
    Arguments:
    clsname = name of class as string, defaults to None, but this must be
                     provided else shard Init will fail
    superclasses = sequence of class names to inherit from. If empty
                            or unspecified, this will default to 'object'
    docstring = formatted string of comments, default is empty
    shards = list of shards (any of shard objects, lines of code, functions)
                   to form body of class, i.e. class variables and methods.
                   Note: methods should be given as appropriate shard objects,
                   function objects have the body of the function imported only
    
    Returns:
    shard object containing a definition of the class as specified
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['clsname'] = None
    initargs['superclasses'] = []
    initargs['docstring'] = ''
    initargs['shards'] = []
    
    # compulsory init parameters
    required = ['clsname']
    
    
    def __init__(self, clsname = None, superclasses = [], docstring = '', shards = []):
        
        if not clsname:
            raise ArgumentError, 'classname must be a non-empty string'
        
        super(classShard, self).__init__(name = clsname, docstring = docstring,
                                                          shards = shards)
        
        defline = self.makeclass(clsname, superclasses)
        
        self.code = defline + self.addindent(self.docstring) + [nl] \
                            + self.addindent(self.code, 1)
    
    
    def makeclass(self, name, superclasses = None):
        """
        Creates class statement
        
        Arguments:
        name = string of class name
        superclasses = sequence of class names to inherit from. If empty
                                 or unspecified, this will default to 'object'
        
        Returns:
        list of a single string that contains class statement
        """
        
        str = "class " + name
        
        if not superclasses:
            return [str + "(object):"+ nl]
        
        str += "(" + superclasses[0]
        for supercls in superclasses[1:]:
            str += ", " + supercls
        
        return [str + "):" + nl]
    
    
    def makeMethodShards(self, functions):
        """
        Converts function objects to method shards, adds
        self parameter if not present
        
        Arguments:
        functions = sequence of function or shard objects;
                           shards are added to output, functions
                           are converted to shard objects containing
                           code for the method
        Returns:
        list of shard objects corresponding to given functions
        """
        
        mshards = []
        for m in functions:
            if isfunction(m):
                lines = inspect.getsource(m).splitlines(True) # get code
                # check for self parameter, add as necessary
                if lines[0].find(m.func_name+"(self") == -1:
                    nm, br, argsln = lines[0].partition("(")
                    lines[0] = nm + br + "self, " + argsln
                # make shard
                m = shard(name = m.func_name, code = lines + [nl])
            
            mshards += [m]
        
        return mshards
