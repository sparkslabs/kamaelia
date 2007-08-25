from Shard import *
import inspect

"""
Makes class shards
"""

nl = "\n"

class classShard(docShard):

    """
    Creates a class as a shard from given components
    
    Arguments:
    clsname = name of class as string, defaults to None, but this must be
                     provided else shard Init will fail
    superclasses = sequence of class names to inherit from. If empty
                            or unspecified, this will default to 'object'
    docstring = formatted string of comments, default is empty
    inboxes = dict of inbox names to default values, generally a description.
                     Default (inbox, control) boxes are always generated
    outboxes = dict of outbox names to default values, generally a description.
                       Default (outbox, signal) boxes are always generated
    shards = list of shards (any of shard objects, lines of code, functions)
                   to form body of class, i.e. class variables and methods.
                   Note: methods should be given as appropriate shard objects,
                   function objects have the body of the function imported only
    
    Returns:
    shard object containing a definition of the class as specified
    """

    # default initialisation parameters
    initargs = {}
    initargs['clsname'] = None
    initargs['superclasses'] = []
    initargs['docstring'] = ''
    initargs['inboxes'] = {}
    initargs['outboxes'] = {}
    initargs['shards'] = []
    
    # compulsory init parameters
    required = ['clsname']


    def __init__(self, clsname = None, superclasses = [], docstring = '', inboxes = {},
                        outboxes = {}, shards = []):

        
        if not clsname:
            raise ArgumentError, 'classname must be given'
        
        super(classShard, self).__init__(name = clsname, docstring = docstring,
                                                          shards = shards)
        
        defline = self.makeclass(clsname, superclasses)
        inboxes = self.addindent(self.makeboxes(inboxes = True, boxes = inboxes), 1)
        outboxes = self.addindent(self.makeboxes(inboxes = False, boxes = outboxes), 1)
        
        self.code = defline + self.addindent(self.docstring) + inboxes + outboxes + [nl] \
                           + self.addindent(self.code, 1)


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


    def makeboxes(self, inboxes = True, default = True, boxes = {}):
        """
        Makes in and outboxes.

        Arguments:
        inboxes = True if inboxes are to be made (default), False if outboxes wanted
        default = ensure standard in and control boxes (Inbox) or out and signal
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
            # overwrite standard inbox descriptions if supplied
            if 'inbox' in boxes.keys():
                inbox = '\"inbox\": ' + '\"' + boxes['inbox'] + '\"' + ',' + nl
                boxes.pop('inbox')
            if 'control' in boxes.keys():
                control = '\"control\": ' + '\"' + boxes['control'] + '\"' + ',' + nl
                boxes.pop('control')

            pre = " "*len(inopen)
            if default:
                lines += [inopen + inbox, pre + control]

        else:  #outbox
            # overwrite standard outbox descriptions if supplied
            if 'outbox' in boxes.keys():
                outbox = '\"outbox\": ' + '\"' + boxes['outbox'] + '\"' + ',' + nl
                boxes.pop('outbox')
            if 'signal' in boxes.keys():
                signal = '\"signal\": ' + '\"' + boxes['signal'] + '\"' + ',' + nl
                boxes.pop('signal')

            pre = " "*len(outopen)
            if default:
                lines += [outopen + outbox, pre + signal]

        if not default:  # need a custom box on initial line
            boxnm, val = boxes.popitem()
            str = '\"' + boxnm + '\": ' + val + ',' + nl
            if inbox:
                lines += [inopen + str]
            else:
                lines += [outopen + str]

        for boxnm, val in boxes.items():
            lines += [pre + '\"' + boxnm + '\": ' + '\"' + val + '\"' + ',' + nl]

        return lines + [pre[:-2] + "}\n"]  #line up and add closing brace


    def makeMethodShards(self, functions):
        """
        Converts function objects to method shards, adds
        self parameter if not present

        Arguments:
        functions = sequence of function or shard objects;
                           shards are added to output, functions
                           are converted to shard objects containing
                           code for the method
        Returns:
        list of shard objects corresponding to given functions
        """

        mshards = []
        for m in functions:
            if isfunction(m):
                lines = inspect.getsource(m).splitlines(True) # get code
                # check for self parameter, add as necessary
                if lines[0].find(m.func_name+"(self") == -1:
                    nm, br, argsln = lines[0].partition("(")
                    lines[0] = nm + br + "self, " + argsln
                # make shard
                m = shard(name = m.func_name, code = lines + [nl])

            mshards += [m]

        return mshards