
"""
The shardGen class is an interface between a GUI node and the
code generation shard system. Each shardGen object wraps a given
shard class and publishes its required and default constructor
arguments. The same interface is provided for all shards so that they
can be queried consistently. Calling makeShard() will produce an object
of the enclosed shard type, initialised appropriately.
The example in this file recreates the pygame event loop from the
MagnaDoodle component (directly generated in full in MagnaGen.py).

From a GUI perspective, the shardGen object provides the default
parameters for the shard it represents (also marking those that are
compulsory for convenience). Where possible, it can store child shards
in a likewise uninitialised state in the form of other shardGen objects.
This is possible wherever the shard class is initialised with a 'shards'
argument listing its children; occasionally this is not the case, for instance
the 'ifShard' class requires that a condition be attached to each child, so
each branch must be specified directly.
Non-shard arguments should be set in the shardGen.args dict directly.

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



if __name__ == '__main__':
    # example: mouse handler from MagnaDoodle
    from MagnaGen import *

    mh = shardGen(switchShard) # mousehandler
    mh.args['name'] = 'mouseHandler'
    mh.args['switchVar'] = 'event.type'
    mh.args['branches'] = [('pygame.MOUSEBUTTONDOWN', [MOUSEBUTTONDOWN_handler]),
                                           ('pygame.MOUSEBUTTONUP', [MOUSEBUTTONUP_handler]),
                                           ('pygame.MOUSEMOTION', [MOUSEMOTION_handler])]

    # wrap switch in loop that reads from inbox
    pyl = shardGen(forShard) # pyevent loop
    pyl.args['name'] = 'eventhandler'
    pyl.args['forVars'] = ['event']
    pyl.args['inVar'] = r'self.recv("inbox")'
    pyl.children += [mh]

    # wrap event loop in inbox checking loop so that no invalid reads are performed
    ml = shardGen(whileShard) # mainloop
    ml.args['name'] = 'pygameEventLoop'
    ml.args['condition'] = r'self.dataReady("inbox")'
    ml.children += [pyl]

    # add mainloop's shard to ishard dict, children initialised automatically
    ishards['LoopOverPygameEvents'] = ml.makeShard()  # replace previous shard here

    ## exactly as Magna test case in MagnaGen from here ##
    # construct magnadoodle class from the above chassis
    chassis = pygameComponentShard(cmpname = "MagnaDoodle",
                                                             methods = [blitToSurface, waitBox, drawBG, addListenEvent],
                                                             ishards = ishards)

    # wrap magna with the necessary imports
    file = moduleShard("PygameAppChassis", importmodules = ['pygame', 'Axon'],
                                   importfrom = {'Kamaelia.UI.PygameDisplay': ['PygameDisplay']},
                                   shards = [chassis])


    file.writeFile()

    from PygameAppChassis import *
    MagnaDoodle(size=(800,600)).run()

