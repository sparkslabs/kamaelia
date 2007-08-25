"""
From a GUI perspective, the shardGen object provides the default
parameters for the shard object it represents (also marking those
that are compulsory for convenience). It can store child shards in a
likewise uninitialised state in the form of other shardGen objects.
Shard information is set in the shardGen.args dict directly.

From a code generation perspective, the object supplies the initialised
shard object which automatically generates its own code. Initalisation
of child shards is done by the shardGen object, so a call to makeShard
on a root shardGen object will provide a completely initialised hierarchy
of shards.
"""

class shardGen(object):
    
    """
    Shard paramenter values should be set in the args dict, child shards
    can be set directly or in shardGen form as shardGen.children. Child
    shardGen objects are initialised and added (where required) by the
    makeShard method
    """
    
    def __init__(self, shard):
        self.shard = shard
        
        self.children = [] # for child shardGen objects
        self.args = shard.initargs.copy()
        if hasattr(shard, 'required'):
            self.required = shard.required
        else:
            self.required = []
    
    def makeShard(self):
        if self.args.has_key('shards'):
            for sg in self.children:
                self.args['shards'] += [sg.makeShard()]
        
        return self.shard(**self.args)
    