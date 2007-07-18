import FunctionShard

class initShard(FunctionShard.functionShard):
    
    def __init__(self, clsname, args = [], kwargs = {}, exarg = None,
                        exkwarg = None, docstring = '', shards = []):
        superinit = ["super(" + clsname+", self).__init__()"]
        
        functionShard.__init__(funcname = '__init__', indent = 1, args = args,
                                           kwargs = kwargs, exarg = exarg, exkwarg = exkwarg,
                                           docstring = docstring, shards = [superinit] + shards)