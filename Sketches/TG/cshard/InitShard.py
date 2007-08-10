from FunctionShard import functionShard
from Shard import ArgumentError

class initShard(functionShard):

    """
    Generates a default __init__ method for a class, consisting of
    a call to super().__init__ followed by the specified shards
    
    Arguments:
    clsname = string name of the class containing this __init__,
                      must be provided
    args = list of any arguments in addition to 'self' that init needs,
                default is empty
    kwargs = dict of any keywords arguments that init needs,
                    default is empty
    exarg = name of an 'extra arguments' parameter, default None (not included)
    exkwarg = name of an 'extra keyword arguments' parameter, default None
    docstring = string of documentation to be included in the init method
    shards = list of shards to be the body of the init, default empty
    """

    # default initialisation parameters
    initargs = {}
    initargs['clsname'] = None
    initargs['args'] = []
    initargs['kwargs'] = {}
    initargs['exarg'] = None
    initargs['exkwarg'] = None
    initargs['docstring'] = ''
    initargs['shards'] = []
    
    
    def __init__(self, clsname = None, args = [], kwargs = {}, exarg = None,
                        exkwarg = None, docstring = '', shards = []):
        
        if not clsname:
            raise ArgumentError, 'class name must be provided'
        
        superinit = ["super(" + clsname+", self).__init__()\n"]
        
        super(initShard, self).__init__(funcname = '__init__', args = ['self']+ args,
                                           kwargs = kwargs, exarg = exarg, exkwarg = exkwarg,
                                           docstring = docstring, shards = [superinit] + shards)