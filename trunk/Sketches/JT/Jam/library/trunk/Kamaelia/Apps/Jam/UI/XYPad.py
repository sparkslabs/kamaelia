#!/usr/bin/env python
# TODO:
# * Convert to vectors?

"""
=============
XY Pad Widget
=============

An XY pad widget with a draggable, bouncing puck.  Pick up  data on the
"outbox" outbox to receive the position of the puck and messages indicating
when it has touched one of the sides.



Example Usage
-------------

Create an XY pad which redraws 60 times per second:

    from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock

    clock = Clock(float(1)/60).activate()
    xyPad = XYPad().activate()
    clock.link((clock, "outbox"), (xyPad, "newframe"))



How Does it Work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the surface of the XY pad.  It binds listeners for
mouse click and motion to the service.

The component works in one of two different modes, bouncing and non-bouncing.
This is specified upon initialization by the bouncingPuck argument.

In the bouncing mode the puck will continue to move once it has been set into
motion by a mouse drag.  If the mouse button remains down for longer than 0.1
seconds it is deemed to be a drag.  In the bouncing mode the component sends a
(message, 1) tuple to the "outbox" outbox each time the puck collides with one
of the sides.  The messages can be changed using the collisionMsg argument.
They default to "top", "right", "bottom", "left".

In the non-bouncing mode the puck remains stationary after it has been dragged.

Both modes send a (positionMsg, (x, y)) tuple to the "outbox" outbox if the
puck moves.

The XY pad only redraws the surface and updates the puck position when it
receives a message on its "newframe" inbox.  Note that although providing
messages more frequently here will lead to more frequent updates, it will also
lead to higher CPU usage.

The visual appearance of the pad can be specified by arguments to the
constructor.  The size, position and colours are all adjustable.

If a producerFinished or shutdownMicroprocess message is received on its
"control" inbox, it is passed on out of its "signal" outbox and the component
terminates.
"""

import time
import pygame
import Axon

from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class XYPad(Axon.Component.component):
    """\
    XYPad([bouncingPuck, position, bgcolour, fgcolour, positionMsg,
           collisionMsg, size]) -> new XYPad component.
    
    Create an XY pad widget using the Pygame Display service.  Sends messages
    for position and direction changes out of its "outbox" outbox.

    Keyword arguments (all optional):
    bouncingPuck -- whether the puck will continue to move after it has been
                    dragged (default=True)
    position     -- (x,y) position of top left corner in pixels
    bgcolour     -- (r,g,b) fill colour (default=(255,255,255))
    fgcolor      -- (r, g, b) colour of the puck and border
    positionMsg  -- sent as the first element of a (positionMsg, 1) tuple when
                   the puck moves
    collisionMsg -- (t, r, b, l) sent as the first element of a
                    (collisionMsg[i], 1) tuple when the puck hits a side
                    (default = ("top", "right", "bottom", "left"))
    size         -- (w,h) in pixels (default=(100, 100))

    """
    Inboxes = {"inbox"    : "Receive events from Pygame Display",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display",
               "newframe" : "Recieve messages indicating a new frame is to be drawn"
              }
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
   
    def __init__(self, bouncingPuck=True, position=None,
                 bgcolour=(255, 255, 255), fgcolour=(0, 0, 0),
                 positionMsg="position",
                 collisionMsg = ("top", "right", "bottom", "left"),
                 size=(100, 100)):
        super(XYPad, self).__init__()

        self.size = size
        
        # Does the puck bounce around
        self.bouncingPuck = bouncingPuck
        # Is the puck currently bouncing around
        self.isBouncing = False

        self.mouseDown = False
        self.clickTime = None
        self.mousePositions = []
        self.lastMousePos = (0, 0)

        self.puckRadius = 10
        self.puckPos = [self.size[0]/2, self.size[1]/2]
        self.puckVel = [0, 0]

        self.borderWidth = 5
        self.bgcolour = bgcolour
        self.fgcolour = fgcolour

        self.positionMsg = positionMsg
        self.collisionMsg = collisionMsg

        self.dispRequest = {"DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),
                            "events" : (self, "inbox"),
                            "size": self.size,
                           }

        if position:
            self.dispRequest["position"] = position

    def waitBox(self, boxName):
        """Wait for a message on boxName inbox"""
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
                        self.clickTime = time.time()
                        if self.display.get_rect().collidepoint(*event.pos):
                            self.mouseDown = True
                            self.isBouncing = False
                            self.mousePositions = []
                            self.puckVel = [0, 0]
                            self.puckPos = list(event.pos)
                            self.lastMousePos = event.pos

                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.mouseDown:
                            if (self.bouncingPuck and
                                time.time() - self.clickTime > 0.1):
                                # Click and drag
                                self.isBouncing = True
                                if len(self.mousePositions):
                                    for i in xrange(2):
                                        # Use the average of the last 50
                                        # relative mouse positions
                                        positions = [x[i] for x in self.mousePositions]
                                        self.puckVel[i] = sum(positions)
                                        self.puckVel[i] /= float(len(positions))
                            else:
                                # Just a click
                                self.puckVel = [0, 0]
                                self.render()
                        self.mouseDown = False
                    
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
                if self.isBouncing:
                    if self.puckPos[0] <= 0:
                        # Left wall
                        self.puckVel[0] *= -1
                        self.send((self.collisionMsg[3], 1), "outbox")
                    if self.puckPos[0] >= self.size[0]:
                        # Right wall
                        self.puckVel[0]  *= -1
                        self.send((self.collisionMsg[1], 1), "outbox")
                    if self.puckPos[1] <= 0:
                        # Top wall
                        self.puckVel[1] *= -1
                        self.send((self.collisionMsg[0], 1), "outbox")
                    if self.puckPos[1] >= self.size[1]:
                        # Bottom wall
                        self.puckVel[1] *= -1
                        self.send((self.collisionMsg[2], 1), "outbox")

                if self.isBouncing:
                    # Update the position
                    for i in xrange(2):
                        self.puckPos[i] += self.puckVel[i]
                    self.render()
            
      
    def render(self):
        """Draw the border and puck onto the surface"""
        self.display.fill(self.bgcolour)
        pygame.draw.rect(self.display, self.fgcolour,
                         self.display.get_rect(), self.borderWidth)
        pygame.draw.circle(self.display, self.fgcolour,
                           [int(x) for x in self.puckPos], self.puckRadius)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        self.send((self.positionMsg, (float(self.puckPos[0])/self.size[0],
                                float(self.puckPos[1])/self.size[1])),
                  "outbox")

if __name__ == "__main__":
    from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
    from Kamaelia.Util.Console import ConsoleEchoer

    FPS = 60
    
    clock = Clock(float(1)/FPS).activate()
    clock2 = Clock(float(1)/FPS).activate()
    xyPad = XYPad().activate()
    xyPad2 = XYPad(size=(200, 200), bouncingPuck = False, position = (210, 0),
                   bgcolour=(0, 0, 0), fgcolour=(255, 255, 255),
                   positionMsg="p2").activate()
    ce = ConsoleEchoer().activate()
    clock.link((clock, "outbox"), (xyPad, "newframe"))
    clock2.link((clock2, "outbox"), (xyPad2, "newframe"))
    xyPad.link((xyPad, "outbox"), (ce,"inbox"))
    xyPad2.link((xyPad2, "outbox"), (ce,"inbox"))
    Axon.Scheduler.scheduler.run.runThreads()  
