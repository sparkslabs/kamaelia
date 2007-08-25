import Shard

nl = "\n"

class moduleShard(Shard.docShard):
    
    """
    Creates import statements followed by the given shards
    
    Arguments:
    importmodules = strings of module names to be imported
    importfrom = mapping from modules to sequences of
                          objects to be imported from each
    docstring = formatted string of comments, default is empty
    shards = list of shards to make up the body of the module
    
    Returns:
    shard object containing import statements
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['importmodules'] = []
    initargs['importfrom'] = {}
    initargs['docstring'] = ''
    initargs['shards'] = []
    
    
    def __init__(self, name = None, importmodules = [], importfrom = {},
                        docstring = '', shards = []):
        
        super(moduleShard, self).__init__(name = name, docstring = docstring,
                                                             shards = shards)
        
        lines = ["import "+nm + nl for nm in importmodules]
        
        if importfrom:
            for module, objects in importfrom.items():
                str = ""
                try:
                    str += "from " + module +" import " + objects[0]
                except IndexError:
                    raise TypeError, "module cannot be mapped to an empty sequence"
                for object in objects[1:]:
                    str += ", " + object
                lines += [str + nl]
        
        if docstring:
            self.docstring += [nl, nl]
            
        self.code = lines + [nl] + self.docstring + self.code
