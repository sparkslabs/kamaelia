import Shard

"""
Wrapper shard for adding imports to a module of shards
"""

nl = "\n"

class moduleShard(Shard.docShard):
    
    def __init__(self, name = None, importmodules = [], importfrom = {},
                        docstring = '', shards = []):
        """
        Creates import statements
        
        Arguments:
        importmodules = strings of module names to be imported
        importfrom = mapping from modules to sequences of
                              objects to be imported from each
        docstring = formatted string of comments, default is empty
        
        Returns:
        shard object containing import statements
        """
        
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
