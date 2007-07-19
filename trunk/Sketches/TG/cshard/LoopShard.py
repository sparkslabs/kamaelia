import Shard

class forShard(Shard.shard):
    def __init__(self, name = None, forVars = [], inVar = '[]', shards = [], indent = 0):
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
        indent = indent level to start the loop statement at; loop body
                       indented automatically
        """
        
        shard.__init__(name = name, indent = indent, shards = shards, indent = indent+1)
        
        forline = "for "
        if not forVars:
            forline += "_, "
        else:
            for var in forVars:
                forline += var + ", "
        forline = forline[:-2] + " in " + inVar + ":\n"
        
        self.code = self.addIndent([forline], indent) + self.code


class whileShard(Shard.shard):
    def __init__(self, name = None, condition = 'True', shards = [], indent = 0):
        """
        Generates a while-loop
        
        Arguments:
        name = name for this shard, given an auto-generated name if left
        condition = continuation condition as a string, defaults to 'True',
                           i.e. an infinite loop
        shards = list of shards to include in body. As usual, these can be
                       shard objects, lines of code, or function names that
                       contain the required code
        indent = indent level to start the loop statement at; loop body
                       indented automatically
        """
        
        shard.__init__(name = name, indent = indent, shards = shards, indent = indent+1)
        
        self.code = self.addIndent(["while "+condition+":\n"], indent) + self.code

