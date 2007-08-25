from Shard import *
from ComponentShard import *
from LoopShard import *
from InitShard import initShard
from FunctionShard import functionShard

"""
Example to recreate Sketches/MPS/Shard/Shards.py with code generation
setup, i.e. class with the same functionality as ShardedPygameAppChassis

Current test (MagnaGen.py) successfully generates and runs MagnaDoodle
using this as a base
"""

class pygameComponentShard(componentShard):

    """
    Generates a pygame kamaelia component if all required methods
    and shards are supplied, else raises a DependencyError

    Arguments:
    name = string of component name, will be used as class
                 name. If None, an auto-generated name will be
                 used.
    shards = the methods and inline shards to be added into the class,
                   as function objects or shard objects. At minimum these
                   must include this class's required methods and ishards,
                   else a DependencyError will be raised. Objects must be
                   named as the method or ishard they are supplying.
                   Any additional shards, e.g. extra methods, will be included
                   'as is' in the body of the class
    """
    
    # use shard classmethods to state minimum required shards to generate this
    shard.addReqMethods("blitToSurface", "waitBox", "drawBG", "addListenEvent" )
    shard.addReqIShards("ShutdownHandler", "LoopOverPygameEvents", "RequestDisplay",
                                        "__INIT__", "GrabDisplay", "SetEventOptions" )

    # default information supplied by this class
    sclasses = ["Axon.Component.component"]
    dstr = 'Auto-generated pygame component'
    inbxs = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
    outbxs = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
    
    # default initialisation parameters
    initargs = {}
    initargs['cmpname'] = None
    initargs['methods'] = []
    initargs['ishards'] = {}

    def __init__(self, name = None, shards = []):
        
        mshards = []
        ishards = {}
        
        for s in shards:
            if isinstance(s, shard):
                sname = s.name
            else: # assume function
                sname = s.func_name
            
            if sname in self.requiredIShards:
                ishards[sname] = s
            else:
                mshards.append(s)
        
        mshards = self.makeMethodShards(mshards)
        self.checkDependencies(mshards, ishards)
        
        # create default methods and add in shards
        compInit = initShard(clsname = name, exkwarg = 'argd',
                                         shards = [ishards['__INIT__']])
        
        waitLoop = forShard(name = 'wait', inVar = r'self.waitBox("callback")',
                                         shards = [['yield 1\n']])
        
        mainLoop = whileShard(name = 'mainLoop', condition = 'not done',
                                              shards = [ishards['ShutdownHandler'],
                                                              ishards['LoopOverPygameEvents'],
                                                              ['self.pause()\n', 'yield 1\n']])
        
        compMain = functionShard(funcname = "main", args = ['self'],
                                                    shards = [ishards["RequestDisplay"], waitLoop,
                                                    ishards['GrabDisplay'],
                                                    ['self.drawBG()\n', 'self.blitToSurface()\n'],
                                                    ishards['SetEventOptions'], ['done = False\n'],
                                                    mainLoop])
        
        # construct pygame component with default and supplied shards
        componentShard.__init__(self, name, superclasses = self.sclasses,
                                       docstring = self.dstr, inboxes = self.inbxs,
                                       outboxes = self.outbxs,
                                       shards = [compInit] + mshards + [compMain])
