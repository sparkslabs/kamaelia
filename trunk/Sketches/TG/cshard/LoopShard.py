from Shard import shard

class forShard(shard):
    
    """
    Generates code for a for-loop
    
    Arguments:
    name = name for this shard, given an auto-generated name if left
    forVars = list of loop variable names as strings, default empty,
                    which means that variable is ignored, i.e. '_' used
    inVar = sequence or generator to loop over, passed as a string
    shards = list of shards to include in body. As usual, these can be
                   shard objects, lines of code, or function names that
                   contain the required code
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['forVars'] = []
    initargs['inVar'] = '[]'
    initargs['shards'] = []
    
    
    def __init__(self, name = None, forVars = [], inVar = '[]', shards = []):
        
        super(forShard, self).__init__(name = name, shards = shards)
        
        forline = "for "
        if not forVars:
            forline += "_, "
        else:
            for var in forVars:
                forline += var + ", "
        forline = forline[:-2] + " in " + inVar + ":\n"
        
        self.code = [forline] + self.addindent(self.code, 1)


class whileShard(shard):
    
    """
    Generates a while-loop
    
    Arguments:
    name = name for this shard, given an auto-generated name if left
    condition = continuation condition as a string, defaults to 'True',
                       i.e. an infinite loop
    shards = list of shards to include in body. As usual, these can be
                   shard objects, lines of code, or function names that
                   contain the required code
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['condition'] = 'True'
    initargs['shards'] = []
    
    
    def __init__(self, name = None, condition = 'True', shards = []):
        
        super(whileShard, self).__init__(name = name, shards = shards)
        
        self.code = ["while "+condition+":\n"] + self.addindent(self.code, 1)

