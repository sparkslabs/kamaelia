from Shard import docShard, ArgumentError

nl = "\n"

class functionShard(docShard):

    """
    Generate code for a new function
    
    Arguments:
    funcname = name for new shard, must be provided else shard init will fail
    args = named arguments as strings
    kwargs = keyword arguments mapped to their default values
    exarg = name of an 'extra arguments' parameter, default None (not included)
    exkwarg = name of an 'extra keyword arguments' parameter, default None
    docstring = formatted string of comments, default is empty
    shards = list of shards to be pasted into the body of the function, any combination
                   of shard objects, lines of code or function names
    
    Returns:
    shard object containing definition of function as specified
    """

    # default initialisation parameters
    initargs = {}
    initargs['funcname'] = None
    initargs['args'] = []
    initargs['kwargs'] = {}
    initargs['exarg'] = None
    initargs['exkwarg'] = None
    initargs['docstring'] = ''
    initargs['shards'] = []


    def __init__(self, funcname = None, args = [], kwargs = {}, exarg = None,
                        exkwarg = None, docstring = '', shards = []):
        
        if not funcname:
            raise ArgumentError, 'function name must be provided'
        
        super(functionShard, self).__init__(name = funcname, docstring = docstring,
                                                              shards = shards)
        
        args = self.makearglist(args, kwargs, exarg, exkwarg)
        defline = ["def "+funcname+"("+args+"):\n"]
        
        self.code = defline + self.addindent(self.docstring + self.code, 1) + [nl]
    
    
    def makearglist(self, args, kwargs, exarg = None, exkwarg = None):
        """
        Generates argument list for a function
        
        Arguments:
        args = list of names of arguments or None if none
        kwargs = dict of keyword argument names to default values as strings,
                        or None if none
        exarg = name of an 'extra arguments' parameter, default None (not included)
        exkwarg = name of an 'extra keyword arguments' parameter, default None
        """
        
        arglist = ""
        
        if args:
            for arg in args:
                arglist += arg + ', '
        
        if kwargs:
            for kw, val in kwargs.items():
                arglist += kw + ' = ' + val + ', '
            
        if exarg:
            arglist += '*'+exarg+', '
            
        if exkwarg:
            arglist += '**'+exkwarg+', '
            
        return arglist[:-2] # remove trailing comma and space
