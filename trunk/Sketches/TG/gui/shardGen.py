
class shardGen(object):
    
    """
    Interface for gui to all shard objects, supplies required parameters,
    default values and a method for retrieving the initialised shard object.
    Paramenter values should be set directly in the args dict
    """
    
    def __init__(self, shard):
        self.shard = shard
        self.args = shard.initargs.copy()
        if hasattr(shard, 'required'):
            self.required = shard.required
        else:
            self.required = []
    
    def makeShard(self):
        return self.shard(**self.args)