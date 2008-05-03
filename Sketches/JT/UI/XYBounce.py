#!/usr/bin/env python
import pygame
import Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class XYBounce(Axon.Component.component):
    Inboxes = {"inbox"    : "Receive events from Pygame Display",
              "control"  : "For shutdown messages",
              "callback" : "Receive callbacks from Pygame Display"}
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
   
    def __init__(self, size=(100, 100)):
        super(XYBounce, self).__init__()
        self.size = size
        self.puckPos = (50, 50)
        self.disprequest = {"DISPLAYREQUEST" : True,
                          "callback" : (self,"callback"),
                          "events" : (self, "inbox"),
                          "size": self.size,
                          }
      
    def main(self):
        """Main loop."""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)

        self.send(self.disprequest,
                  "display_signal")
        
        # Wait until we get a display
        while 1:
            if self.dataReady("callback"):
                self.display = self.recv("callback")
                break
            else:
                yield 1
      
        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                   "surface" : self.display},
                  "display_signal")

        done = False
        while not done:
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if (isinstance(cmsg, producerFinished) or
                    isinstance(cmsg, shutdownMicroprocess)):
                    self.send(cmsg, "signal")
                    done = True
         
            while self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bounds = self.display.get_rect()
                        if bounds.collidepoint(*event.pos):
                            self.puckPos = event.pos
                            self.send(event.pos, "outbox")
            self.render()
            self.pause()
            yield 1
            
      
    def render(self):
        self.display.fill((255, 255, 255))
        rect = pygame.Rect(0, 0, *self.size)
        #This is inefficient - don't need to keep redrawing this
        pygame.draw.rect(self.display, (0, 0, 0), rect, 5)
        pygame.draw.circle(self.display, (0, 0, 0), self.puckPos, 10)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

if __name__ == "__main__":
    from Kamaelia.Util.Console import ConsoleEchoer
   
    xyBounce = XYBounce().activate()
    ce = ConsoleEchoer().activate()
    xyBounce.link((xyBounce, "outbox"), (ce,"inbox"))
    Axon.Scheduler.scheduler.run.runThreads()  
