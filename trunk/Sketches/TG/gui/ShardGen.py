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
argument listing its children; occasionally a shard will not have children,
e.g. the function call shard (FuncAppShard.py)
Non-shard arguments should be set in the shardGen.args dict directly.

From a code generation perspective, the object supplies the initialised
shard object which automatically generates its own code. Initalisation
of child shards is done by the shardGen object, so a call to makeShard
on a root shardGen object will provide a completely initialised hierarchy
of shards.
"""

from pickle import dump, HIGHEST_PROTOCOL
import os


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
    
    def writeFile(self, filepath = None):
        if not hasattr(self, 'label'):
            self.label = self.shard.__name__
            
        if not filepath:
            filepath = os.sep.join([os.environ['HOME'], self.label +'.py'])
        
        file = open(filepath, 'w')
        dump(self, file, HIGHEST_PROTOCOL)
        file.close()
        
        return file



if __name__ == '__main__':
    # example: mouse handler from MagnaDoodle
    from MagnaGen import *
    from ExampleMagnaShards import __INIT__ # needs to be specifically imported

    mh = shardGen(switchShard) # mousehandler
    mh.args['name'] = 'mouseHandler'
    mh.args['switchVar'] = 'event.type'
    mh.args['conditions'] = ['pygame.MOUSEBUTTONDOWN', 'pygame.MOUSEBUTTONUP',
                                              'pygame.MOUSEMOTION']
    mh.args['shards'] = [MOUSEBUTTONDOWN_handler, MOUSEBUTTONUP_handler,
                                       MOUSEMOTION_handler]

    # wrap switch in loop that reads from inbox
    pyl = shardGen(forShard) # pyevent loop
    pyl.args['name'] = 'eventhandler'
    pyl.args['forVars'] = ['event']
    pyl.args['inVar'] = r'self.recv("inbox")'
    pyl.children += [mh]

    # wrap event loop in inbox checking loop so that no invalid reads are performed
    ml = shardGen(whileShard) # mainloop
    ml.args['name'] = 'LoopOverPygameEvents'
    ml.args['condition'] = r'self.dataReady("inbox")'
    ml.children += [pyl]



    # add mainloop's shard to shard list, children initialised automatically
    shards = [blitToSurface, waitBox, drawBG, addListenEvent, __INIT__,
                    SetEventOptions, ShutdownHandler, RequestDisplay, GrabDisplay,
                    ml.makeShard()]  # replace previous shard here


    ## exactly as Magna test case in MagnaGen from here ##
    # construct magnadoodle class from the above chassis
    chassis = pygameComponentShard(name = "MagnaDoodle", shards = shards)

    # wrap magna with the necessary imports
    file = moduleShard("MagnaDoodle", importmodules = ['pygame', 'Axon'],
                                   importfrom = {'Kamaelia.UI.PygameDisplay': ['PygameDisplay']},
                                   shards = [chassis])


    file.writeFile('MagnaDoodle.py') # default puts file in homedir, override
    
    from MagnaDoodle import *
    MagnaDoodle(size=(800,600)).run()

