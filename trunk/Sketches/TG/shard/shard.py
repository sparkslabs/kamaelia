import inspect

"""
Trying the non-metaclass way of doing things
Return single-argument functions to allow decorator-style
use (when this is supported for classes...)
"""
# attributes that shouldn't be overwritten
ignoreList = dir(object)
ignoreList += ['__dict__', '__module__', '__doc__', '__metaclass__', '__weakref__']
ignoreList += ['__requiresMethods']  # any additional or custom attrs

def addShards(*shardList):
    """
    Adds all given shards at once: eliminates repeated overwriting
    of attributes and allows dependency calculation
    
    Any application of this method must satisfy all dependencies
    between shards and container class, as unsatisfied
    dependencies cause errors
    
    If container class declares its requirements, these will also be checked
    """
    
    # merge all shards, later entries override earlier ones
    attrDict = {}
    for shard in shardList:
        attrDict.update( dict(inspect.getmembers(shard)) ) # getmembers used to get inherited attrs
    
    # filter out attrs on ignoreList
    for name in ignoreList:
        try:
            attrDict.pop(name)
        except KeyError:
            continue    # don't care if it isn't there
            
    # getmembers gives unbound methods; convert to function objects
    for name, attr in attrDict.items():
        if inspect.ismethod(attr):
            attrDict[name] = attr.im_func
    
    # calculate if any requirements/dependencies remain
    requiredMethods = []
    for shard in shardList:
        if hasattr(shard, '__requiresMethods'):
            requiredMethods += shard.__requiresMethods
    
    for provided in attrDict.keys():
        try:
            requiredMethods.remove(provided)
        except ValueError:
            continue   # don't care if method provided isn't required
    
    # define and return attr-setting function
    def shardify(cls):
        
        # check dependencies of added shards are satisfied by container cls
        reqM = requiredMethods[:]
        for attr in dir(cls):
            try:
                reqM.remove(attr)
            except ValueError:
                continue   # don't care if method provided isn't required
        
        if reqM:  # dependencies of shards outstanding
            errmess = 'required methods missing from %s: %s' % (cls.__name__, reqM)

            raise TypeError, errmess
        
        # if container class declares requirements, check these too
        if hasattr(cls, '__requiresMethods'):
            cls.__requiresMethods = list(cls.__requiresMethods)
            for name in attrDict.keys():
                try:
                    cls.__requiresMethods.remove(name)
                except ValueError:
                    continue   # don't care if method provided isn't required
            
            if cls.__requiresMethods:  # dependencies of container cls outstanding
                errmess = 'required methods missing from', cls.__name__
                errmess += ':', cls.__requiresMethods
                raise TypeError, errmess
        
        # no requirements remaining, set shard methods as cls attributes
        for name, attr in attrDict.items():
            if name in cls.__dict__:
                raise TypeError, '%s already has %s' % (repr(cls), name)
            setattr(cls, name, attr)
    
    return shardify


def requires(*methodList):
    """
    Optional decorator for shard classes to list any dependencies
    
    If a shard uses methods it does not provide/import, it should declare
    them using this function or by setting the __requiresMethods attribute
    manually
    
    If this attribute is not present, it will be assumed no additional
    methods are required
    """
    def setDependents(shard):
        shard.__requiresMethods = methodList
    
    return setDependents