from Shard import *

class switchShard(shard):

    """
    Generates a switch-type if statement. General form is:
    ...
    elif <switchVar> <compare> <conditions[i]>:
        shards[i]
    ...
    
    Arguments:
    name = name of new shard, default None. If no name is specified
                 a default name will be generated
    switchVar = the switch variable as a string, e.g. 'event.type'
    conditions = list of variables (as strings) to compare against
                         switchVar, one for each branch. Any branches without
                         conditions will be placed in an 'else' branch. Any
                         conditions without branches will be ignored
    compare = string of comparison operator. The same operator
                      will be used for all branches, default is '=='
    shards = list containing one shard for each branch, in the same
                    order as the relevant condition. If there are fewer
                    conditions than shards, those remaining will be placed
                    in an 'else' branch
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['switchVar'] = ''
    initargs['conditions'] = []
    initargs['shards'] = []
    initargs['compare'] = '=='
    
    # compulsory init parameters
    required = ['switchVar', 'shards', 'conditions']


    def __init__(self, name = None, switchVar = '', conditions = [], shards = [], compare = '=='):
        
        if not (switchVar or shards or conditions):
            raise ArgumentError, 'a switch variable and at least one branch and condition must be provided'
        
        compare = ' ' + compare + ' '
        
        ifbr, cond = shards.pop(0), conditions.pop(0)
        ifline = ['if ' + switchVar + compare + cond + ':\n']
        ifbranch = shard('if branch', shards = [ifbr])
        
        code = ifline + ifbranch.addindent()
        
        if len(conditions) > len(shards):
            conditions = conditions[0:len(shards)] # ignore excess conditions
        
        while conditions:
            elifbr, cond = shards.pop(0), conditions.pop(0)
            elifline = ['elif ' + switchVar + compare + cond + ':\n']
            sh = shard('elif branch', shards = [elifbr])
            code += elifline + sh.addindent()
        
        if shards: # shards remaining, place into else branch
            sh = shard('else branch', shards = shards)
            code += ['else:\n'] + sh.addindent()
        
        super(switchShard, self).__init__(shards = [code])
        