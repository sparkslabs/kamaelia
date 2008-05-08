#!/usr/bin/env python
# TODO:
# * Additional functionality?
# * Convert to vectors?
# * Clean up & document

import pygame
import Axon
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class XYBounce(Axon.Component.component):
    Inboxes = {"inbox"    : "Receive events from Pygame Display",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display",
               "newframe" : "Recieve messages indicating a new frame is to be drawn"
              }
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
   
    def __init__(self, size=(100, 100)):
        super(XYBounce, self).__init__()
        self.size = size

        self.bouncing = False

        self.mouseDown = False
        self.mousePositions = []
        self.lastMousePos = (0, 0)

        self.puckRadius = 10
        self.puckPos = [self.size[0]/2, self.size[1]/2]
        self.puckVel = [0, 0]

        self.borderWidth = 5

        self.dispRequest = {"DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),
                            "events" : (self, "inbox"),
                            "size": self.size,
                           }

    def waitBox(self, boxName):
        while 1:
            if self.dataReady(boxName):
                return
            else:
                yield 1
      
    def main(self):
        """Main loop."""
        displayService = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayService)

        self.send(self.dispRequest,
                  "display_signal")
        
        # Wait until we get a display
        while 1:
            yield WaitComplete(self.waitBox("callback"))
            break
        self.display = self.recv("callback")

        # Initial render so we don't see a blank screen
        self.render()
      
        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                   "surface" : self.display},
                  "display_signal")

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                   "surface" : self.display},
                  "display_signal")

        self.send({"ADDLISTENEVENT" : pygame.MOUSEMOTION,
                   "surface" : self.display},
                  "display_signal")

        done = False
        while not done:
            if not self.anyReady():
                self.pause()
            yield 1

            while self.dataReady("control"):
                cmsg = self.recv("control")
                if (isinstance(cmsg, producerFinished) or
                    isinstance(cmsg, shutdownMicroprocess)):
                    self.send(cmsg, "signal")
                    done = True
         
            while self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.display.get_rect().collidepoint(*event.pos):
                            self.mouseDown = True
                            self.bouncing = False
                            self.mousePositions = []
                            self.puckVel = [0, 0]
                            self.puckPos = list(event.pos)
                            self.lastMousePos = event.pos

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.mouseDown = False
                        if len(self.mousePositions) > 10:
                            # Click and drag
                            self.bouncing = True
                            for i in xrange(2):
                                # Use the average of the last 50 relative
                                # mouse positions
                                positions = [x[i] for x in self.mousePositions]
                                self.puckVel[i] = sum(positions)
                                self.puckVel[i] /= float(len(positions))
                        else:
                            # Just a click
                            self.puckVel = [0, 0]
                            self.render()
                    
                    if event.type == pygame.MOUSEMOTION and self.mouseDown:
                        if self.display.get_rect().collidepoint(*event.pos):
                            # We are dragging inside the display
                            # Keep a buffer of 50 mouse positions
                            if len(self.mousePositions) > 50:
                                del self.mousePositions[0]
                            relPos = []
                            for i in xrange(2):
                                relPos.append(event.pos[i] -
                                              self.lastMousePos[i])
                            self.mousePositions.append(relPos)
                            # Move the puck to where the mouse is and remember
                            # where it is
                            self.puckPos = list(event.pos)
                            self.lastMousePos = event.pos
                            self.render()

            if self.dataReady("newframe"):
                # Time to render a new frame
                # Clear any backlog of render messages
                while self.dataReady("newframe"):
                    self.recv("newframe")

                # Change the direction of the puck if it hits a wall
                if self.puckPos[0] <= 0:
                    self.puckVel[0] *= -1
                    if self.bouncing:
                        self.send(("left", (1)), "outbox")
                if self.puckPos[0] >= self.size[0]:
                    self.puckVel[0]  *= -1
                    if self.bouncing:
                        self.send(("right", (1)), "outbox")
                if self.puckPos[1] <= 0:
                    self.puckVel[1] *= -1
                    if self.bouncing:
                        self.send(("top", (1)), "outbox")
                if self.puckPos[1] >= self.size[1]:
                    self.puckVel[1] *= -1
                    if self.bouncing:
                        self.send(("bottom", (1)), "outbox")

                if self.puckVel[0] or self.puckVel[1]:
                    # Update the position
                    for i in xrange(2):
                        self.puckPos[i] += self.puckVel[i]
                    self.render()
            
      
    def render(self):
        self.display.fill((255, 255, 255))
        pygame.draw.rect(self.display, (0, 0, 0),
                         self.display.get_rect(), self.borderWidth)
        pygame.draw.circle(self.display, (0, 0, 0),
                           [int(x) for x in self.puckPos], self.puckRadius)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        self.send(("position", (float(self.puckPos[0])/self.size[0],
                                float(self.puckPos[1])/self.size[1])),
                  "outbox")

if __name__ == "__main__":
    from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
    from Kamaelia.Util.Console import ConsoleEchoer

    FPS = 60
    
    clock = Clock(float(1)/FPS).activate()
    xyBounce = XYBounce().activate()
    ce = ConsoleEchoer().activate()
    clock.link((clock, "outbox"), (xyBounce, "newframe"))
    xyBounce.link((xyBounce, "outbox"), (ce,"inbox"))
    Axon.Scheduler.scheduler.run.runThreads()  
