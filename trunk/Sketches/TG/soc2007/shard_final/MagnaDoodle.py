import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay

# START SHARD: MagnaDoodle -----------------------------------------------------
class MagnaDoodle(Axon.Component.component):
    """
    Auto-generated pygame component
    """
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
        # START SHARD: __init__.shard2 -------------------------------------------------
        super(MagnaDoodle, self).__init__()
        # END SHARD: __init__.shard2 ---------------------------------------------------
        
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
            # START SHARD: wait.shard3 -----------------------------------------------------
            yield 1
            # END SHARD: wait.shard3 -------------------------------------------------------
            
        # END SHARD: wait --------------------------------------------------------------
        
        # START SHARD: GrabDisplay -----------------------------------------------------
        self.display = self.recv("callback")
        # END SHARD: GrabDisplay -------------------------------------------------------
        
        # START SHARD: main.shard5 -----------------------------------------------------
        self.drawBG()
        self.blitToSurface()
        # END SHARD: main.shard5 -------------------------------------------------------
        
        # START SHARD: SetEventOptions -------------------------------------------------
        self.addListenEvent("MOUSEBUTTONDOWN")
        self.addListenEvent("MOUSEBUTTONUP")
        self.addListenEvent("MOUSEMOTION")
        # END SHARD: SetEventOptions ---------------------------------------------------
        
        # START SHARD: main.shard6 -----------------------------------------------------
        done = False
        # END SHARD: main.shard6 -------------------------------------------------------
        
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
                # START SHARD: eventhandler ----------------------------------------------------
                for event in self.recv("inbox"):
                    # START SHARD: shard0 ----------------------------------------------------------
                    # START SHARD: shard0.shard1 ---------------------------------------------------
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # START SHARD: MOUSEBUTTONDOWN_handler -----------------------------------------
                        #print 'down'
                        if  event.button == 1:
                            self.drawing = True
                        elif event.button == 3:
                            self.oldpos = None
                            self.drawBG()
                            self.blitToSurface()
                        # END SHARD: MOUSEBUTTONDOWN_handler -------------------------------------------
                        
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # START SHARD: MOUSEBUTTONUP_handler -------------------------------------------
                        #print 'up'
                        if event.button == 1:
                            self.drawing = False
                            self.oldpos = None
                        # END SHARD: MOUSEBUTTONUP_handler ---------------------------------------------
                        
                    elif event.type == pygame.MOUSEMOTION:
                        # START SHARD: MOUSEMOTION_handler ---------------------------------------------
                        #print 'move'
                        if self.drawing and self.innerRect.collidepoint(*event.pos):
                            if self.oldpos == None:
                                self.oldpos = event.pos
                            else:
                                pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
                                self.oldpos = event.pos
                            self.blitToSurface()
                        # END SHARD: MOUSEMOTION_handler -----------------------------------------------
                        
                    # END SHARD: shard0.shard1 -----------------------------------------------------
                    
                    # END SHARD: shard0 ------------------------------------------------------------
                    
                # END SHARD: eventhandler ------------------------------------------------------
                
            # END SHARD: LoopOverPygameEvents ----------------------------------------------
            
            # START SHARD: mainLoop.shard4 -------------------------------------------------
            self.pause()
            yield 1
            # END SHARD: mainLoop.shard4 ---------------------------------------------------
            
        # END SHARD: mainLoop ----------------------------------------------------------
        
    
    # END SHARD: main --------------------------------------------------------------
    
# END SHARD: MagnaDoodle -------------------------------------------------------

