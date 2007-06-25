"""
Trying the non-metaclass way of doing things
"""
# 
ignoreList = ['__module__', '__doc__', '__metaclass__']

def addShard(attrDict):
    """Adds the single given shard to a class"""
    
    # filter out attrs on ignoreList
    for name in ignoreList:
        try:
            attrDict.pop(name)
        except KeyError:
            continue    # don't care if it isn't there
            
    def shardify(cls):
        for name, attr in attrDict.items():
            if name in cls.__dict__:
                raise TypeError, '%s already has %s' % (repr(cls), name)
            setattr(cls, name, attr)
    
    return shardify


def addShards(shardList):
    """
    Adds all given shards at once: eliminates repeated overwriting
    of attributes and allows dependency calculation (if shards specify these)
    
    (Can only apply this method once to a class if dependency requirements
    cause errors)
    """
    
    # merge all shards, later entries override earlier ones
    attrDict = {}
    for shard in shardList:
        attrDict.update(shard.__dict__)
    
    # filter out attrs on ignoreList
    for name in ignoreList:
        try:
            attrDict.pop(name)
        except KeyError:
            continue    # don't care if it isn't there
    
    # calculate if any requirements/dependencies remain
    
    # define and return attr-setting function
    def shardify(cls):
        for name, attr in attrDict.items():
            if name in cls.__dict__:
                raise TypeError, '%s already has %s' % (repr(cls), name)
            setattr(cls, name, attr)
    
    return shardify