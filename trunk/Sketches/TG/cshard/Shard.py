from cshard import getshard  #, annotate

"""
Rough first pass at shard constructor: aims to treat shard objects,
named functions and lists of strings (code) equivalently

Current thought is to subclass shard to create Connectors,
e.g. ifshard(shard) can construct if-statements as shards,
functionshard(shard) can replace the current makefunction, etc.
Would replace the more '2-stage' approaches so far by making
everything a shard.

TODO:
Replace dummy uses of 'if code' with a reasonable test
"""


class shard(object):
    
    @staticmethod
    def namegen(name = 'shard'):
        """
        Generates names for anonymous shards
        """
        
        i = 0
        while True:
            yield name+str(i)
            i += 1
    
    namer = namegen()
    
    def __init__(self, name = None, indent = 0, annotate = False, function = None, code = None, *shards):
        super(Shard, self).__init__()
        
        self.indent = indent
        
        if function:
            self.name = function.name()
            self.code = getshard(f, indent)
        elif code:
            self.name = name if name else namer.next()
            self.code = code
        else:
            self.name = name if name else namer.next()
            self.code = []
            for s in shards:
                if s is function:
                    s = shard(function = s)
                elif s is code:
                    s = shard(name = name, code = s)
                code += s.annotate() if annotate else s.code
    
    
    def annotate(self, delimchar = '-'):
        """
        Marks out start and end of shard code with comments
    
        Arguments:
        delimchar = single character string containing character to be used
                            in marking out shard limit across the page
    
        Returns:
        list of lines of code surrounded by delimiter comments as specified
        """

        start = r"# START SHARD: " + self.name + " "
        start = indent([start], indentlevel)[0]
        start = start.ljust(80, delimchar) + "\n"
    
        end = r"# END SHARD: " + self.name + " "
        end = indent([end], indentlevel)[0]
        end = end.ljust(80, delimchar) + "\n"
    
        return [start] + self.code + [end]
                