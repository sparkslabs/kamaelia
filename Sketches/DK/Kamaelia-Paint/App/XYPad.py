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

If the editable argument to the constructor is set to be false the pad will not
respond to mouse presses.

As well as being controlled by the mouse an XY pad can be controlled externally,
for example by a second XY pad.  Position and velocity messages received on the
"remoteChanges" inbox are used to change the motion of the puck.  Position
messages are of the form ("Position", (xPos, yPos)), and velocity messages are
of the form ("Velocity", (xVel, yVel)).

In order to allow communication between two XY pads the component outputs
position and velocity messages to the "localChanges" outbox.  By connecting the
"localChanges" outbox of one XY pad to the "remoteChanges" inbox of another,
the second pad can duplicate the motion of the first.

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
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock

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
    messagePrefix -- string to be prepended to all messages
    positionMsg  -- sent  as the first element of a (positionMsg, 1) tuple when
                   the puck moves
    collisionMsg -- (t, r, b, l) sent as the first element of a
                    (collisionMsg[i], 1) tuple when the puck hits a side
                    (default = ("top", "right", "bottom", "left"))
    size         -- (w,h) in pixels (default=(100, 100))

    """
    Inboxes = {"inbox"    : "Receive events from Pygame Display",
               "remoteChanges"  : "Receive messages to alter the state of the XY pad",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display",
               "newframe" : "Recieve messages indicating a new frame is to be drawn",
               "buttons" : "Recieve interrupts from the buttons"
              }
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "localChanges" : "Messages indicating change in the state of the XY pad emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
   
    def __init__(self, bouncingPuck=True, position=None,
                 bgcolour=(255, 255, 255), fgcolour=(0, 0, 0),
                 messagePrefix = "",
                 positionMsg="Position",
                 colours="RG",
                 selectedColour = (0,0,0),
                 saturation=False,
                 collisionMsg = ("Top", "Right", "Bottom", "Left"),
                 size=(100, 100), editable=True):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(XYPad, self).__init__()

        self.size = size
        
        # Does the puck bounce around
        self.bouncingPuck = bouncingPuck
        # Is the puck currently bouncing around
        self.isBouncing = False
        self.selectedColour = selectedColour
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
        self.colours = colours

        self.messagePrefix = messagePrefix
        self.positionMsg = positionMsg
        self.collisionMsg = collisionMsg

        self.editable = editable

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


        rgbutton = Button(caption="Red/Green",position=(0,0)).activate()
        rbbutton = Button(caption="Red/Blue",position=(0,50)).activate()
        gbbutton = Button(caption="Green/Blue",position=(0,100)).activate()
        self.link( (rgbutton,"outbox"), (self,"buttons") )
        self.link( (rbbutton,"outbox"), (self,"buttons") )
        self.link( (gbbutton,"outbox"), (self,"buttons") )
        FPS = 60
        clock = Clock(float(1)/FPS).activate()
        self.link((clock, "outbox"), (self, "newframe"))





        self.send(self.dispRequest,
                  "display_signal")
        
        # Wait until we get a display
        while 1:
            yield WaitComplete(self.waitBox("callback"))
            break
        self.display = self.recv("callback")

        # Initial render so we don't see a blank screen
        self.drawBG()
      #  self.render()
        if self.editable:
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
            while self.dataReady("buttons"):
                bmsg = self.recv("buttons")
                print bmsg
                if (bmsg[1] == 14):
                    self.colours = "RG"
                    self.drawBG()
                elif (bmsg[1] == 15):
                    self.colours = "RB"
                    self.drawBG()
                elif (bmsg[1] == 16):
                    self.colours = "GB"
                    self.drawBG()
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if (isinstance(cmsg, producerFinished)):
                    self.send(cmsg, "signal")
                    done = True
                elif (cmsg[0]=="CLICK"):
                    if (cmsg[1] == 6):
                        self.colours = "RG"
                        self.drawBG()
                    elif (cmsg[1] == 7):
                        self.colours = "RB"
                        self.drawBG()
                    elif (cmsg[1] == 8):
                        self.colours = "GB"
                        self.drawBG()
         
            while self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event == "CLICK":
                #     print bmsg
                        print self.recv("inbox")
                        if (bmsg == 6):
                            self.colours = "RG"
                            self.drawBG()
                        elif (bmsg == 7):
                            self.colours = "RB"
                            self.drawBG()
                        elif (bmsg == 8):
                            self.colours = "GB"
                            self.drawBG()
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.clickTime = time.time()
                        if self.display.get_rect().collidepoint(*event.pos):
                            self.mouseDown = True
                            self.isBouncing = False
                            self.mousePositions = []
                            self.puckVel = [0, 0]
                            self.puckPos = list(event.pos)
                            self.lastMousePos = event.pos
                            self.send((self.messagePrefix + self.positionMsg,
                                       (float(self.puckPos[0])/self.size[0],
                                        float(self.puckPos[1])/self.size[1])),
                                      "localChanges")

                            self.send((self.messagePrefix + "Velocity",
                                       self.puckVel), "localChanges")
                                    

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
                            self.send((self.messagePrefix + "Velocity",
                                      self.puckVel), "localChanges")
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
                            self.send((self.messagePrefix + self.positionMsg,
                                       (float(self.puckPos[0])/self.size[0],
                                       float(self.puckPos[1])/self.size[1])),
                                      "localChanges")
                            self.render()

            if self.dataReady("remoteChanges"):
                bundle = self.recv("remoteChanges")
                # The action to take is given by the last section of the
                # OSC address - this should maybe be done by a component and
                # we just listen for ("Velocity", (xVel, yVel)) tuples
                action = bundle[0].split("/")[-1]
                if action == "Velocity":
                    if self.bouncingPuck:
                        self.puckVel =  bundle[1]
                        self.isBouncing = 1
                elif action == "Position":
                    for i in xrange(2):
                        self.puckPos[i] = self.size[i] * bundle[1][i]
                self.render()

            if self.dataReady("newframe"):
                # Time to render a new frame
                # Clear any backlog of render messages
                while self.dataReady("newframe"):
                    self.recv("newframe")

                # Change the direction of the puck if it hits a wall
                if self.isBouncing:
                    self.processCollisions()

                if self.isBouncing:
                    # Update the position
                    for i in xrange(2):
                        self.puckPos[i] += self.puckVel[i]
                    self.render()

    def processCollisions(self):
        """
        Detect whether the puck has collided with a wall, and change its
        direction appropriately
        """

        if self.puckPos[0] <= 0:
            # Left wall
            self.puckVel[0] *= -1
            self.send((self.messagePrefix + self.collisionMsg[3], 1), "outbox")
        if self.puckPos[0] >= self.size[0]:
            # Right wall
            self.puckVel[0]  *= -1
            self.send((self.messagePrefix + self.collisionMsg[1], 1), "outbox")
        if self.puckPos[1] <= 0:
            # Top wall
            self.puckVel[1] *= -1
            self.send((self.messagePrefix + self.collisionMsg[0], 1), "outbox")
        if self.puckPos[1] >= self.size[1]:
            # Bottom wall
            self.puckVel[1] *= -1
            self.send((self.messagePrefix + self.collisionMsg[2], 1), "outbox") 
    
    def drawBG(self):
        if (self.colours == "RG"):
            for y in range(0, self.size[0], self.size[0]/25):
                for x in range(0, self.size[1], self.size[1]/25):
                    box = pygame.Rect(x, y, 10, 10)
                    pygame.draw.rect(self.display, (x,y,0), box, 0)
        elif (self.colours == "RB"):
            for y in range(0, self.size[0], self.size[0]/25):
                for x in range(0, self.size[1], self.size[1]/25):
                    box = pygame.Rect(x, y, 10, 10)
                    pygame.draw.rect(self.display, (x,0,y), box, 0)
        elif (self.colours == "GB"):
            for y in range(0, self.size[0], self.size[0]/25):
                for x in range(0, self.size[1], self.size[1]/25):
                    box = pygame.Rect(x, y, 10, 10)
                    pygame.draw.rect(self.display, (0,x,y), box, 0)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
    def render(self):
        """Draw the border and puck onto the surface"""
     #                    self.display.get_rect(), self.borderWidth)

        if (self.colours == "RG"):
            self.selectedColour = (self.puckPos[0], self.puckPos[1], 0)
        elif (self.colours == "RB"):
            self.selectedColour = (self.puckPos[0], 0, self.puckPos[1])
        elif (self.colours == "GB"):
            self.selectedColour = (0, self.puckPos[0], self.puckPos[1])
        pygame.draw.rect(self.display, self.selectedColour,
                         self.display.get_rect(), self.borderWidth)
        # Puck
   #     pygame.draw.circle(self.display, self.fgcolour,
    #                       [int(x) for x in self.puckPos], self.puckRadius)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        self.send((("colour",self.selectedColour),), "outbox")

if __name__ == "__main__":
    from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    

    
  #  xyPad = XYPad().activate()
    xyPad2 = XYPad(size=(255, 255), bouncingPuck = False, position = (70, 0),
                   bgcolour=(0, 0, 0), fgcolour=(255, 255, 255),
                   positionMsg="p2").activate()
    ce = ConsoleEchoer().activate()
   # clock.link((clock, "outbox"), (xyPad, "newframe"))
   # xyPad.link((xyPad, "outbox"), (ce,"inbox"))
    xyPad2.link((xyPad2, "outbox"), (ce,"inbox"))
    Axon.Scheduler.scheduler.run.runThreads()  
    
# Licensed to the BBC under a Contributor Agreement: JT/DK
