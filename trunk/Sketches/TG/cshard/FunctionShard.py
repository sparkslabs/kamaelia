import Shard

"""
Generates function definition code as shard object
"""

indentation = "    "
nl = "\n"

class functionShard(Shard.docShard):
    
    def __init__(self, funcname, indent = 0, args = [], kwargs = {}, exarg = None,
                        exkwarg = None, docstring = '', shards = []):
        """
        Generate code for a new function
        
        Arguments:
        funcname = name for new shard
        indent = indent = level of indentation to add to function body, default 0
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
        
        bodyind = indent + 1
        
        super(functionShard, self).__init__(name = funcname, indent = bodyind,
                                                              docstring = docstring, shards = shards)
        
        args = self.makearglist(args, kwargs, exarg, exkwarg)
        defline = self.addindent(["def "+funcname+"("+args+"):\n"], indent)
        
        self.code = defline + self.docstring + self.code + [nl]
    
    
    def makearglist(self, args, kwargs, exarg = None, exkwarg = None):
        """
        Generates argument list for a function
        
        Arguments:
        args = list of names of arguments or None if none
        kwargs = dict of keyword argument names to default values as strings,
                        or None if none
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
