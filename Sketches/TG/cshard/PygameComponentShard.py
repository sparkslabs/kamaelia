from Shard import *
from ClassShard import *
from LoopShard import *
from InitShard import initShard
from FunctionShard import functionShard

"""
Experiment to try and recreate MPS/Shards with code gen
setup, i.e. generation of PygameAppChassis

At the moment 15 line-main method construction takes 17 lines
in __init__. Not sure this is so great.
"""

indentation = "    "
nl = "\n"

class pygameComponentShard(classShard):
    # required addin shards
    requires_methods = set(( "blitToSurface", "waitBox", "drawBG", "addListenEvent" ))
    requires_ishards = set(("MOUSEBUTTONDOWN", "MOUSEBUTTONUP", "MOUSEMOTION",
                       "HandleShutdown", "LoopOverPygameEvents", "RequestDisplay",
                       "GrabDisplay", "SetEventOptions" ))
    
    # default information supplied by this class
    sclasses = ["Axon.Component.component"]
    dstr = ''
    inbxs = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
    outbxs = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
    
    
    def __init__(self, cmpname = None, *methods, **ishards):
        
        mshards = []
        # add methods to shard list, importing as necessary
        for m in methods:
            if isfunction(m):
                m = shard(name = m.func_name, code = self.getMethod(m))
            mshards += [m]
        
        # check all dependencies satisfied
        error = ""
        mgiven = set([s.name for s in mshards if isinstance(s, shard)])
        
        if not self.requires_methods <= mgiven:
            error += "need methods "+ str(self.requires_methods - mgiven)
        if not self.requires_ishards <= set(ishards.keys()):
            error += "need ishards "+ str(self.requires_ishards - set(ishards.keys()))
        
        if not error == "":
            raise DependencyError, error
        
        # create default methods and add in shards
        compInit = initShard(clsname = cmpname, exkwarg = 'argd',
                                         shards = [ishards['__INIT__']])
        
        waitLoop = forShard(name = 'wait', inVar = r'self.waitBox("callback")',
                                         shards = [['yield 1\n']])
                                         
        mainLoop = whileShard(name = 'mainLoop', condition = 'not done',
                                              shards = [ishards['HandleShutdown'],
                                                              ishards['LoopOverPygameEvents'],
                                                              ['self.pause()\n', 'yield 1\n']])
        
        compMain = functionShard(funcname = "main", args = ['self'],
                                                    shards = [ishards["RequestDisplay"], waitLoop,
                                                    ishards['GrabDisplay'],
                                                    ['self.drawBG()\n', 'self.blitToSurface()\n'],
                                                    ishards['SetEventOptions'], ['done = False\n'],
                                                    mainLoop])
        
        # construct class with full shard set
        classShard.__init__(self, cmpname, superclasses = self.sclasses,
                                       docstring = self.dstr, inboxes = self.inbxs,
                                       outboxes = self.outbxs,
                                       shards = [compInit] + mshards + [compMain])

from MagnaDoodleShards import __INIT__
from MagnaDoodleShards import *
from InlineShards import *
from Shards import *


chassis = pygameComponentShard("PygameAppChassis",
                                                         blitToSurface, waitBox, drawBG, addListenEvent,
                                                         __INIT__ = __INIT__,
                                                         MOUSEBUTTONDOWN = MOUSEBUTTONDOWN_handler,
                                                         MOUSEBUTTONUP = MOUSEBUTTONUP_handler,
                                                         MOUSEMOTION = MOUSEMOTION_handler,
                                                         SetEventOptions = SetEventOptions,
                                                         HandleShutdown = ShutdownHandler,
                                                         LoopOverPygameEvents = LoopOverPygameEvents,
                                                         RequestDisplay = RequestDisplay,
                                                         GrabDisplay = GrabDisplay)

chassis.writeFile()
