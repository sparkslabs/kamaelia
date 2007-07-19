from ClassShard import *
from LoopShard import *

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
    
    
    def __init__(self, componentname = "PygameAppChassis", *methods, **ishards):
        
        mshards = []
        # add methods to shard list, importing as necessary
        for m in methods:
            print m
            if type(m) == type(""):
                mshards += [Shard(name = m, code = self.getMethod(m))]
            else:
                mshards += [m]

        # check all dependencies satisfied
        error = ""
        mgiven = set([s.name for s in mshards if isinstance(m, Shard)])
        if not requires_methods <= mgiven:
            error += "need methods "+ str(requires_methods - mgiven)
        if not requires_ishards <= set(ishards.keys()):
            error += "need ishards "+ str(requires_ishards - set(ishards.keys()))
        
        if not error == "":
            raise Fail, error
        
        # create default methods and add in shards
        compInit = initShard(clsname = componentname, exkwarg = 'argd',
                                         shards = [ishards['__INIT__']])
        
        waitLoop = forShard(name = 'wait', inVar = r'self.waitBox("callback")',
                                         shards = [['yield 1\n']], indent = 2)
                                         
        mainLoop = whileShard(name = 'mainLoop', condition = 'not done', indent = 2,
                                              shards = [ishard['HandleShutdown'],
                                                              ishard['LoopOverPygameEvents'],
                                                              ['self.pause()\n', 'yield 1\n']])
        
        compMain = functionShard(funcname = "main", indent = 1, args = ['self'],
                                                    shards = [ishards["RequestDisplay"], waitLoop,
                                                    ishards['GrabDisplay'],
                                                    ['self.drawBG()\n', 'self.blitToSurface()\n'],
                                                    ishard['SetEventOptions'], ['done = False\n'],
                                                    mainLoop])
        
        # construct class with full shard set
        classShard.__init__(self, componentname, superclasses = self.sclasses,
                                       docstring = self.dstr, inboxes = self.inbxs, outboxes = outbxs,
                                       shards = [compInit] + mshards + [compMain])

#~ import MagnaDoodleShards
#~ import Shards
#~ import InlineShards

from MagnaDoodleShards import *
from InlineShards import *
from Shards import *

#~ print
#~ for d in dir():
    #~ print d
#~ print

#~ import inspect
#~ print inspect.getsource(waitBox)

chassis = pygameComponentShard('blitToSurface', 'waitBox', 'drawBG', 'addListenEvent',
                                                         MOUSEBUTTONDOWN = MOUSEBUTTONDOWN_handler,
                                                         MOUSEBUTTONUP = MOUSEBUTTONUP_handler,
                                                         MOUSEMOTION = MOUSEMOTION_handler,
                                                         SetEventOptions = SetEventOptions,
                                                         HandleShutdown = ShutdownHandler,
                                                         LoopOverPygameEvents = LoopOverPygameEvents,
                                                         RequestDisplay = RequestDisplay,
                                                         GrabDisplay = GrabDisplay)
