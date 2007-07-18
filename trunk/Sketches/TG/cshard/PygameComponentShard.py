from ClassShard import *
from ShardCore import *

"""
Experiment to try and recreate MPS/Shards with code gen
setup, i.e. generation of PygameAppChassis
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
    sclasses = ["Axon.Component.component", "Shardable"]
    dstr = ''
    inbxs = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
    outbxs = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
    
    def __init__(self, componentname = "PygameAppChassis", methods = [], ishards = {}):
        
        mshards = []
        # add methods to shard list, importing as necessary
        for m in methods:
            if type(m) == type(""):
                mshards += [Shard(name = m, code = getMethod(m))]
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
                                         shards = ishards['__INIT__'])
        # need to replace 'shards' below with construction of main method
        compMain = functionShard(funcname = "main", indent = 1, args = ['self'],
                                                    shards = [ishards["RequestDisplay"], ...]):
        
        # construct class with full shard set
        classShard.__init__(self, componentname, superclasses = self.sclasses,
                                       docstring = self.dstr, inboxes = self.inbxs, outboxes = outbxs,
                                       shards = [compInit] + mshards + [compMain])
        
   #~ def main(self):
      #~ """Main loop."""
      #~ exec self.getIShard("RequestDisplay")
      #~ for _ in self.waitBox("callback"):
          #~ yield 1 # This can't be Sharded or ISharded
      #~ exec self.getIShard("GrabDisplay")

      #~ self.drawBG()
      #~ self.blitToSurface()
      #~ exec self.getIShard("SetEventOptions")
      #~ done = False
      #~ while not done:
         #~ exec self.getIShard("HandleShutdown")
         #~ exec self.getIShard("LoopOverPygameEvents")
         #~ self.pause()
         #~ yield 1 # This can't be Sharded or ISharded
        