import Shard

"""
Makes class shards
"""

indentation = "    "
nl = "\n"

class classShard(Shard.shard):
    
    def __init__(self, clsname, superclasses = [], docstring = '', inboxes = {},
                        outboxes = {}, shards = [], indent = 0):
        """
        Creates a class as a shard from given components
        
        Arguments:
        clsname = name of class as string
        superclasses = sequence of class names to inherit from. If empty
                                or unspecified, this will default to 'object'
        docstring = formatted string of comments, default
        inboxes = dict of inbox names to default values, generally a description.
                         Default (inbox, control) boxes are always generated
        outboxes = dict of outbox names to default values, generally a description.
                           Default (outbox, signal) boxes are always generated
        shards = list of shards (any of shard objects, lines of code, function names)
                       to form body of class, i.e. class variables and methods.
                       Note: methods should be given as appropriate function shards,
                       function objects have the body of the function imported only
        indent = level of indentation at which to begin class statement (body of
                      class indented automatically). Defaults to 0
        
        Returns:
        shard object containing a definition of the class as specified
        """
        
        bodyind = indent+1
        super(classShard, self).__init__(name = clsname, indent = bodyind, shards = shards)
        
        defline = self.addindent(self.makeclass(clsname, superclasses), indent)
        docstr = self.addindent(self.makedoc(docstring) if docstring else [], bodyind)
        inboxes = self.addindent(self.makeboxes(inboxes = True, boxes = inboxes), bodyind)
        outboxes = self.addindent(self.makeboxes(inboxes = False, boxes = outboxes), bodyind)
        
        self.code = defline + docstr + inboxes + outboxes + [nl] + self.code
    
    
    def makeclass(self, name, superclasses = None):
        """
        Creates class statement
    
        Arguments:
        name = string of class name
        superclasses = sequence of class names to inherit from. If empty
                                 or unspecified, this will default to 'object'
                             
        Returns:
        list of a single string that contains class statement
        """
    
        str = "class " + name
    
        if not superclasses:
            return [str + "(object):"+ nl]
    
        str += "(" + superclasses[0]
        for supercls in superclasses[1:]:
            str += ", " + supercls
    
        return [str + "):" + nl]


    def makedoc(self, doc):
        """
        Creates docstring
    
        Arguments:
        doc = formatted string for docstring
    
        Returns:
        list of strings containing lines of docstring
        """

        tag = "\"\"\"" + nl
        docstr = tag + doc + nl + tag
        return docstr.splitlines(True)


    def makeboxes(self, inboxes = True, default = True, boxes = {}):
        """
        Makes in and outboxes.
    
        Arguments:
        inboxes = True if inboxes are to be made (default), False if outboxes wanted
        default = make standard in and control boxes (Inbox) or out and signal
                        boxes (Outbox) as appropriate, default is True
        boxes = additional boxnames mapped to default values as strings. This will
                      generally be a description if they are initialised in the body of a class.
    
        Returns:
        list of strings containing the lines of box statements
        """
        
        # default box statements
        inbox = r'"inbox": "This is where we expect to receive messages for work",' + nl
        control = r'"control": "This is where control signals arrive",' + nl
        outbox = r'"outbox": "This is where we expect to send results/messages to after doing work",' + nl
        signal = r'"signal": "This is where control signals are sent out",' + nl
        inopen = "Inboxes = { "
        outopen = "Outboxes = { "
    
        if not default and not boxes:
            return []
    
        lines = []
        pre = ""
    
        if inboxes:
            pre = " "*len(inopen)
            if default:
                lines += [inopen + inbox, pre + control]
            
        else:  #outbox
            pre = " "*len(outopen)
            if default:
                lines += [outopen + outbox, pre + signal]
    
        if not default:  # need a custom box on initial line
            boxnm, val = boxes.popitem()
            str = '\"' + boxnm + '\": ' + val + ',' + nl
            lines += [(inopen if inbox else outopen) + str]
    
        for boxnm, val in boxes.items():
            lines += [pre + '\"' + boxnm + '\": ' + val + ',' + nl]
        
        return lines + [pre[:-2] + "}\n"]  #line up and add closing brace
