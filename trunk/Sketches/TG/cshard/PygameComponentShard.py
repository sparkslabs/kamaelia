from Shard import *
from ClassShard import *
from LoopShard import *
from InitShard import initShard
from FunctionShard import functionShard

"""
Experiment to try and recreate MPS/Shards with code gen
setup, i.e. class to replace PygameAppChassis

Current test successfully generates and runs MagnaDoodle
"""

indentation = "    "
nl = "\n"

class pygameComponentShard(classShard):
    
    # required shards
    shard.addReqMethods("blitToSurface", "waitBox", "drawBG", "addListenEvent" )
    shard.addReqIShards("HandleShutdown", "LoopOverPygameEvents", "RequestDisplay",
                                          "GrabDisplay", "SetEventOptions" )
    
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
    
    
    def __init__(self, cmpname, *methods, **ishards):
        """
        Generates a pygame kamaelia component if all required methods
        and shards are supplied, else raises a DependencyError
        
        Arguments:
        cmpname = string of component name, will be used as class
                            name. If None, an auto-generated name will be
                            used. (No default argument used as it will capture
                            the first method supplied if left blank)
        methods = the methods to be added into the class, as function
                          objects or shard objects. At minimum these must
                          include this class's required methods, else a
                          DependencyError will be raised. Objects must be
                          named as the method they are supplying
        ishards = the inline shards required should be specified as
                        keyword arguments to the shard or function object
                        from which they are to be imported. Non-required
                        shards will be ignored
        """
        
        mshards = self.makeMethodShards(methods)
        
        self.checkDependencies(mshards, ishards)
        
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

from ModuleShard import moduleShard
from BranchShard import *

# construct mouse event handling switch
mousehandler = switchShard('mouseHandler', switchVar = 'event.type',
                                            branches = [('pygame.MOUSEBUTTONDOWN', [MOUSEBUTTONDOWN_handler]),
                                                                ('pygame.MOUSEBUTTONUP', [MOUSEBUTTONUP_handler]),
                                                                ('pygame.MOUSEMOTION', [MOUSEMOTION_handler])])

# wrap switch in loop that reads from inbox
pyeventloop = forShard(name = 'eventhandler', forVars = ['event'], inVar = r'self.recv("inbox")',
                                      shards = [mousehandler])

# wrap event loop in inbox checking loop so that no invalid reads are performed
pyeventloop = whileShard(name = 'pygameEventLoop', condition = r'self.dataReady("inbox")',
                                          shards = [pyeventloop])

# construct magnadoodle class from the above chassis
chassis = pygameComponentShard("MagnaDoodle",
                                                         blitToSurface, waitBox, drawBG, addListenEvent,
                                                         __INIT__ = __INIT__,
                                                         SetEventOptions = SetEventOptions,
                                                         HandleShutdown = ShutdownHandler,
                                                         LoopOverPygameEvents = pyeventloop,  # replace previous shard here
                                                         RequestDisplay = RequestDisplay,
                                                         GrabDisplay = GrabDisplay)

# wrap magna with the necessary imports
file = moduleShard("PygameAppChassis", importmodules = ['pygame', 'Axon'],
                               importfrom = {'Kamaelia.UI.PygameDisplay': ['PygameDisplay']},
                               shards = [chassis])
file.writeFile()

from PygameAppChassis import *
MagnaDoodle(size=(800,600)).run()