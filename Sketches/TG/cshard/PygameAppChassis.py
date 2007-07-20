import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay

# START SHARD: PygameAppChassis ------------------------------------------------
class PygameAppChassis(Axon.Component.component):
    Inboxes = { "inbox": "Receive events from PygameDisplay",
                "control": "For shutdown messages",
                "callback": "Receive callbacks from PygameDisplay",
              }
    Outboxes = { "outbox": "not used",
                 "signal": "For shutdown messages",
                 "display_signal": "Outbox used for communicating to the display surface",
               }

    # START SHARD: __init__ --------------------------------------------------------
    def __init__(self, **argd):
        # START SHARD: __init__ --------------------------------------------------------
        super(PygameAppChassis, self).__init__()
        # END SHARD: __init__ ----------------------------------------------------------
        
        # START SHARD: __INIT__ --------------------------------------------------------
        self.backgroundColour = argd.get("bgcolour", (124,124,124))
        self.foregroundColour = argd.get("fgcolour", (0,0,0))
        self.margin = argd.get("margin", 8)
        self.oldpos = None
        self.drawing = False
        self.size = argd.get("size", (200,200))
        self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)
        if argd.get("msg", None) is None:
            argd["msg"] = ("CLICK", self.id)
        self.eventMsg = argd.get("msg", None)
        if argd.get("transparent",False):
            transparency = argd.get("bgcolour", (124,124,124))
        else:
            transparency = None
        self.disprequest = { "DISPLAYREQUEST" : True,
                             "callback" : (self,"callback"),
                             "events" : (self, "inbox"),
                             "size": self.size,
                             "transparency" : transparency }
        if not argd.get("position", None) is None:
            self.disprequest["position"] = argd.get("position",None)
        # END SHARD: __INIT__ ----------------------------------------------------------
        
    
    # END SHARD: __init__ ----------------------------------------------------------
    
    # START SHARD: blitToSurface ---------------------------------------------------
    def blitToSurface(self):
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
    
    # END SHARD: blitToSurface -----------------------------------------------------
    
    # START SHARD: waitBox ---------------------------------------------------------
    def waitBox(self,boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname): return
            else: yield 1
    
    # END SHARD: waitBox -----------------------------------------------------------
    
    # START SHARD: drawBG ----------------------------------------------------------
    def drawBG(self):
        self.display.fill( (255,0,0) )
        self.display.fill( self.backgroundColour, self.innerRect )
    
    # END SHARD: drawBG ------------------------------------------------------------
    
    # START SHARD: addListenEvent --------------------------------------------------
    def addListenEvent(self, event):
        self.send({ "ADDLISTENEVENT" : pygame.__getattribute__(event),
                    "surface" : self.display},
                    "display_signal")
    
    # END SHARD: addListenEvent ----------------------------------------------------
    
    # START SHARD: main ------------------------------------------------------------
    def main(self):
        # START SHARD: RequestDisplay --------------------------------------------------
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send( self.disprequest, "display_signal")
        # END SHARD: RequestDisplay ----------------------------------------------------
        
        # START SHARD: wait ------------------------------------------------------------
        for _ in self.waitBox("callback"):
            # START SHARD: wait ------------------------------------------------------------
            yield 1
            # END SHARD: wait --------------------------------------------------------------
            
        # END SHARD: wait --------------------------------------------------------------
        
        # START SHARD: GrabDisplay -----------------------------------------------------
        self.display = self.recv("callback")
        # END SHARD: GrabDisplay -------------------------------------------------------
        
        # START SHARD: main ------------------------------------------------------------
        self.drawBG()
        self.blitToSurface()
        # END SHARD: main --------------------------------------------------------------
        
        # START SHARD: SetEventOptions -------------------------------------------------
        self.addListenEvent("MOUSEBUTTONDOWN")
        self.addListenEvent("MOUSEBUTTONUP")
        self.addListenEvent("MOUSEMOTION")
        # END SHARD: SetEventOptions ---------------------------------------------------
        
        # START SHARD: main ------------------------------------------------------------
        done = False
        # END SHARD: main --------------------------------------------------------------
        
        # START SHARD: mainLoop --------------------------------------------------------
        while not done:
            # START SHARD: ShutdownHandler -------------------------------------------------
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, Axon.Ipc.producerFinished) or \
                   isinstance(cmsg, Axon.Ipc.shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    done = True
            # END SHARD: ShutdownHandler ---------------------------------------------------
            
            # START SHARD: LoopOverPygameEvents --------------------------------------------
            while self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        exec self.getIShard("MOUSEBUTTONDOWN")
                    elif event.type == pygame.MOUSEBUTTONUP:
                        exec self.getIShard("MOUSEBUTTONUP")
                    elif event.type == pygame.MOUSEMOTION:
                        exec self.getIShard("MOUSEMOTION")
            # END SHARD: LoopOverPygameEvents ----------------------------------------------
            
            # START SHARD: mainLoop --------------------------------------------------------
            self.pause()
            yield 1
            # END SHARD: mainLoop ----------------------------------------------------------
            
        # END SHARD: mainLoop ----------------------------------------------------------
        
    
    # END SHARD: main --------------------------------------------------------------
    
# END SHARD: PygameAppChassis --------------------------------------------------

