import inspect

"""
Code generation stuff. Can componentise later.
"""

indentation = "    "
nl = "\n"

def indent(lines, level = 1):
    """
    Indents strings with spaces
    
    Arguments:
    strings = list of strings, as input from calling getsource()
                   on a free function
    level = number of levels to be indented, defaults to 1
    
    Returns:
    list of strings prefixed by specified amount of whitespace
    """
    
    if level < 0:
        level = -level
        return [ line[len(indentation*level):] for line in lines ]
        
    elif level == 0: # need to remove raw indentation of 1 level
        return lines
    
    elif level > 0: # need to add indentation
        return [indentation*level + line for line in lines]


def importmodules(*modulenames, **importfrom):
    """
    Creates import statements
    
    Arguments:
    *modulenames = strings of module names to be imported
    importfrom = mapping from modules to sequences of
                          objects to be imported from each
                          
    Returns:
    list of strings containing each line of import statements
    """
    
    lines = ["import " +name + nl for name in modulenames]
    
    if importfrom:
        for module, objects in importfrom.items():
            str = ""
            try:
                str += "from " + module +" import " + objects[0]
            except IndexError:
                raise TypeError, "module cannot be mapped to an empty sequence"
            for object in objects[1:]:
                str += ", " + object
            str += nl
            lines += [str]
    
    return lines + [nl]


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


def makearglist(args, kwargs, exarg = None, exkwarg = None):
    """
    Generates argument list for a function
    
    Arguments
    """
    
    arglist = ""
    
    if args:
        for arg in args:
            arglist += arg + ', '
    
    if kwargs:
        for kw, val in kwargs.items():
            arglist += kw + ' = ' + val + ', '
        
    if exarg:
        arglist += '*'+exarg+', '
        
    if exkwarg:
        arglist += '**'+exkwarg+', '
        
    return arglist[:-2]


def makefunction(name, args, kwargs, exarg = None, exkwarg = None, *shardlist):
    """
    Generate code for a new function
    
    Arguments:
    name = string of function name
    args = named arguments as strings
    kwargs = keyword arguments mapped to their default values
    exarg = name of an 'extra arguments' parameter, default None (not included)
    exkwarg = name of an 'extra keyword arguments' parameter, default None
    shardlist = list of shards to be pasted into the body of the function    ----------------->>  hmm...
    """
    ## shardlist - need a construct to make imported shards/code lines/functions
    ## and constructed shards equivalent
    
    args = makearglist(args, kwargs, exarg, exkwarg)
    defline = "def "+name+"("+args+"):\n"
    
    return defline


def getshard(function, indentlevel = 0):
    """
    Gets shard code for generation
    
    Arguments:
    function = shard function to get
    indentlevel = level of indentation prefixed to lines, default is 0
    
    Returns:
    list of lines of code, indented as specified
    """
    # get code, throwaway def line
    lines = inspect.getsource(function).splitlines(True)[1:]
        
    # remove any whitespace lines at start
    while lines[0].isspace(): lines.pop(0)
    
    # remove docstrings
    while True:
        if lines[0].count(r'"""') % 2 == 1:
            lines.pop(0)  # remove line with opening doctag
            while lines[0].count(r'"""') % 2 == 0:
                lines.pop(0)  # remove lines till tag match
            lines.pop(0) # remove matching tag
        
        if lines[0].count(r'"""') == 0:
            break  # no docstring, start of code
        else:  # docstring tags closed, continue till code line found
            lines.pop(0)
    
    i = len(lines[0]) - len(lines[0].lstrip())
    
    return indent([ line[i:] for line in lines ], indentlevel)


def annotateshard(shardcode, shardname, indentlevel = 0, delimchar = '-'):
    """
    Marks out start and end of shard code with comments
    
    Arguments:
    shardcode = list of lines of code, e.g. in form given by getshard()
    shardname = string containing name of shard
    indentlevel = indentation level of delimiter comments, default of 0
    delimchar = single character string containing character to be used
                        in marking out shard limit across the page
    
    Returns:
    list of lines of code surrounded by delimiter comments as specified
    """

    start = r"# START SHARD: " + shardname + " "
    start = indent([start], indentlevel)[0]
    start = start.ljust(80, delimchar) + "\n"
    
    end = r"# END SHARD: " + shardname + " "
    end = indent([end], indentlevel)[0]
    end = end.ljust(80, delimchar) + "\n"
    
    return [start] + shardcode + [end]
    

# kept from shard class stuff as decorator can apply to functions as well as classes
def requires(*methodList):
    """
    Optional decorator for shard functions to list any dependencies.
    
    If a shard uses methods it does not provide/import, it should declare
    them using this function or by setting the __requiresMethods attribute
    manually.
    
    If this attribute is not present, it will be assumed no additional
    methods are required.
    """
    def setDependents(shard):
        shard.__requiresMethods = methodList
        return shard
    
    return setDependents
