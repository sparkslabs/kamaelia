#!/usr/bin/env python
# TODO:
# * Convert to vectors?

"""
=============
Colour Selector Widget
=============

A Colour Selector tool, which represents all colours in the RGB spectrum.
One surface is used to plot the colours for selection and a slider used to
manipulate the other colour, buttons used to change with colours are plotted.

Example Usage
-------------

Create a ColourSelector at 10,170 (from top-left corner) of size 255,255
this provides best colour display.

    from Kamaelia.Apps.Paint.ColourSelector import ColourSelector

    colSel = ColourSelector(position = (10,170), size = (255,255)).activate()
    self.link( (colSel,"outbox"), (self,"outbox"), passthrough = 2 )



How Does it Work?
-----------------

The Component requests a surface and by default plots the red colours 
against green. The border is also drawn, this is here to represent what colour
is currently selected. As the user moves around on the surface selecting various
colours, the border updates to represent this.

The colours are plotted only once to reduce CPU usage, if I were to have a marker
at the point of the selected colour a "crosshair" perhaps I would need to have the 
background constantly redrawing increasing CPU usgae greatly.

The pygame slider code is used to control the colour which isn't being plotted.
(Try it out, you'll see what I mean) 

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
