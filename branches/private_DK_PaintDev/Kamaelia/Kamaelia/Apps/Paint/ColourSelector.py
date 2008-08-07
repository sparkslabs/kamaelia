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
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
from Slider import Slider

class ColourSelector(Axon.Component.component):
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
                "saturator" :"Messages to be sent to the saturator",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
   
    def __init__(self, bouncingPuck=True, position=None,
                 bgcolour=(255, 255, 255), fgcolour=(0, 0, 0),
                 messagePrefix = "Colour",
                 positionMsg="Position",
                 colours="RG",
                 selectedColour = (0,0,0),
                 size=(100, 100), editable=True):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(ColourSelector, self).__init__()

        self.size = size

        self.selectedColour = selectedColour
        self.mouseDown = False
        self.mousePositions = []
        self.lastMousePos = (0, 0)
        self.puckPos = [self.size[0]/2, self.size[1]/2]
        

        self.borderWidth = 5
        self.bgcolour = bgcolour
        self.fgcolour = fgcolour
        self.colours = colours
        self.position = position
        self.messagePrefix = messagePrefix

        self.editable = editable

        self.dispRequest = {"DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),
                            "events" : (self, "inbox"),
                            "size": self.size,
                           }

        if position:
            self.dispRequest["position"] = position
        else:
            self.position = (0,0)
    def waitBox(self, boxName):
        """Wait for a message on boxName inbox"""
        while 1:
            if self.dataReady(boxName):
                return
            else:
                yield 1
      
    def main(self):
        """Main loop."""
    #    pgd = PygameDisplay( width=300, height=550 ).activate()
     #   PygameDisplay.setDisplayService(pgd)

        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)

        self.send( self.dispRequest,
                    "display_signal")

        for _ in self.waitBox("callback"): yield 1
        self.display = self.recv("callback")

        # colour buttons
        rgbutton = Button(caption="Red/Green",position=(self.position[0],self.position[1]+self.size[1]+5), msg = ("ColourCombi", "RG")).activate()
        rbbutton = Button(caption="Red/Blue",position=(self.position[0]+70,self.position[1]+self.size[1]+5), msg = ("ColourCombi", "RB")).activate()
        gbbutton = Button(caption="Green/Blue",position=(self.position[0]+140,self.position[1]+self.size[1]+5), msg = ("ColourCombi", "GB")).activate()
        self.link( (rgbutton,"outbox"), (self,"buttons") )
        self.link( (rbbutton,"outbox"), (self,"buttons") )
        self.link( (gbbutton,"outbox"), (self,"buttons") )
        # saturator
        saturator = Slider(vertical = True, saturator = True, messagePrefix= "Colour", size=(10,255), position=(self.position[0]+self.size[0]+5,self.position[1] )).activate()
        self.link( (self,"saturator"), (saturator,"colours") )
        self.link( (saturator,"outbox"), (self,"outbox"), passthrough = 2 )


      


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
                if bmsg[0]=="ColourCombi":
                    self.colours = bmsg[1]
                    self.send(bmsg, "saturator")
                    self.drawBG()
                    
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if (isinstance(cmsg, producerFinished)):
                    self.send(cmsg, "signal")
                    done = True

            while self.dataReady("inbox"):
                for event in self.recv("inbox"):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.display.get_rect().collidepoint(*event.pos):
                            self.mouseDown = True
                            self.puckPos = event.pos
                            self.render()
                                    

                    if event.type == pygame.MOUSEBUTTONUP and self.mouseDown:
                        if self.mouseDown:
                            self.puckPos = event.pos
                            self.render()
                        self.mouseDown = False
                    
                    if event.type == pygame.MOUSEMOTION and self.mouseDown:
                        if self.display.get_rect().collidepoint(*event.pos):
                            self.puckPos = event.pos
                            self.render()
                        else: self.mouseDown = False


    
    def drawBG(self):
        if (self.colours == "RG"):
            for y in range(0, self.size[0], self.size[0]/100):
                for x in range(0, self.size[1], self.size[1]/100):
                    box = pygame.Rect(x, y, 10, 10)
                    pygame.draw.rect(self.display, (x,y,0), box, 0)
        elif (self.colours == "RB"):
            for y in range(0, self.size[0], self.size[0]/100):
                for x in range(0, self.size[1], self.size[1]/100):
                    box = pygame.Rect(x, y, 10, 10)
                    pygame.draw.rect(self.display, (x,0,y), box, 0)
        elif (self.colours == "GB"):
            for y in range(0, self.size[0], self.size[0]/100):
                for x in range(0, self.size[1], self.size[1]/100):
                    box = pygame.Rect(x, y, 10, 10)
                    pygame.draw.rect(self.display, (0,x,y), box, 0)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        
    def render(self):
        """Draw the border and puck onto the surface"""
     #                    self.display.get_rect(), self.borderWidth)
     #   print self.selectedColour
        if (self.colours == "RG"):
            self.selectedColour = (self.puckPos[0], self.puckPos[1], 0)
        elif (self.colours == "RB"):
            self.selectedColour = (self.puckPos[0], 0, self.puckPos[1])
        elif (self.colours == "GB"):
            self.selectedColour = (0, self.puckPos[0], self.puckPos[1])
        pygame.draw.rect(self.display, self.selectedColour, self.display.get_rect(), self.borderWidth)
        self.send((self.messagePrefix,self.selectedColour), "saturator")
        #refresh the screen
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        

if __name__ == "__main__":
    from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline

    Pipeline(ColourSelector(position = (100,100), size = (255,255)), ConsoleEchoer()).run()
    Axon.Scheduler.scheduler.run.runThreads()
    
# Licensed to the BBC under a Contributor Agreement: JT/DK
