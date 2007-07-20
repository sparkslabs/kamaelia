from Shard import *

class ArgumentError(Exception): pass

nl = "\n"

class switchShard(shard):
    
    def __init__(self, switchVar = None, branches = [], elseshards = [], compare = '=='):
        """
        Generates a switch-type if statement
        
        Arguments:
        switchVar = the switch variable as a string, e.g. 'event.type'
        branches = list of pairs of string values to shard lists (default empty),
                           e.g. [('MouseUp', [HandleMouseUpShard]), ...]
        elseshards = list of shards in else branch, default empty. Else
                              branch will not be generated in this case
        compare = string of comparison operator. The same operator
                          will be used for all branches, default is '=='
        """
        
        if not (switchVar or branches):
            raise ArgumentError, 'both switchVar and at least one branch must be provided'
        
        compare = ' ' + compare + ' '
        
        br, sh = branches.pop(0)
        ifline = ['if ' + switchVar + compare + br + ':\n']
        sh = shard('branch0', shards = sh).addindent()
        
        for pair in branches:
            br, sh = pair
            ...
        
        super(switchShard, self).__init__(shards = [ifline + sh + ...])
        
        
        