import Shard

class classShard(Shard.shard):
    def makeclass(name, superclasses = None):
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


    def makedoc(doc):
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


    def makeboxes(inboxes = True, default = True, **boxes):
        """
        Makes in and outboxes.
    
        Arguments:
        inboxes = True if inboxes are to be made (default), False if outboxes wanted
        default = make standard in and control boxes (Inbox) or out and signal
                        boxes (Outbox) as appropriate, default is True
        ** boxes = additional boxnames with default values. This will generally
                          be a description if they are initialised in the body of a class.
    
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
