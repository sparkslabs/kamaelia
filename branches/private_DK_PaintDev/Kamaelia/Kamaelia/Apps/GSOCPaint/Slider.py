#!/usr/bin/env python
# TODO:
# * Convert to vectors?

"""
=============
Slider Widget
=============

An interface widget to give a visual bar where the user can drag
a line up and down to represent a value they're selecting for example
a "Volume" bar.



Example Usage
-------------

Create a slider bar at 10, 460 with the messagePrefix as "Size" and a default value of 9.

    from Kamaelia.Apps.Paint.Slider import Slider

    SizeSlider = Slider(size=(255, 50), messagePrefix = "Size", position = (10, 460), default = 9).activate()
    self.link( (SizeSlider,"outbox"), (self,"outbox"), passthrough = 2 )



How Does it Work?
-----------------

The slider returns a tuple that looks like this (messagePrefix, value)
"""

import pygame
import Axon

from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.UI.Pygame.Display import PygameDisplay


class Slider(Axon.Component.component):
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
            "control"  : "For shutdown messages",
            "callback" : "Receive callbacks from Pygame Display",
            "colours": "Recieve messages from colourSelector",
            }
            
    Outboxes = {"outbox" : "XY positions emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
            }

    def __init__(self, position=None,
                bgcolour=(255, 255, 255), fgcolour=(0, 0, 0),
                messagePrefix = "Slider",
                default = 0,
                positionMsg="Position",
                saturator = False,
                vertical = None,
                size=(100, 100)):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(Slider, self).__init__()

        self.size = size
        self.vertical = vertical
        if vertical == None:
            if self.size[0] >= self.size[1]:
                self.vertical = False
            else: self.vertical = True
        self.mouseDown = False
        self.clickTime = None
        self.mousePositions = []
        self.lastMousePos = (0, 0)
        self.sliderPos = 0
        self.messagePrefix = messagePrefix
        self.position = position
        self.saturator = saturator
        if saturator:
            self.selectedColour = (0,0,0)
            self.colourCombi = 'RG'
        self.default = default
        self.selectedSize = 3
        self.borderWidth = 5
        self.bgcolour = bgcolour
        self.fgcolour = fgcolour

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
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)

        self.send( self.dispRequest,
                    "display_signal")

        for _ in self.waitBox("callback"): yield 1
        self.display = self.recv("callback")
        
        


        # Initial render so we don't see a blank screen
        self.sliderPos = self.default
        self.drawBG()
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
                if (isinstance(cmsg, producerFinished)):
                    self.send(cmsg, "signal")
                    done = True
            while self.dataReady("colours"):
                msg = self.recv("colours")
                if msg[0] == "ColourCombi":
                    self.colourCombi = msg[1]
                else: 
                    if self.colourCombi == 'RG':
                        self.selectedColour = (msg[1][0],msg[1][1],self.sliderPos)
                    elif self.colourCombi == 'RB':
                        self.selectedColour = (msg[1][0],self.sliderPos,msg[1][2])
                    elif self.colourCombi == 'GB':
                        self.selectedColour = (self.sliderPos,msg[1][1],msg[1][2])
                    self.bgcolour = self.selectedColour
            #        self.display.fill( self.selectedColour)
                self.drawBG()
                self.render()
            while self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.display.get_rect().collidepoint(*event.pos):
                            if self.vertical:
                                self.sliderPos = event.pos[1]
                            else:
                                self.sliderPos = event.pos[0]
                            self.drawBG()
                            self.render()
                            self.mouseDown = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.mouseDown:
                            if self.vertical:
                                self.sliderPos = event.pos[1]
                            else:
                                self.sliderPos = event.pos[0]
                            self.drawBG()
                            self.render()
                        self.mouseDown = False
                    
                    if event.type == pygame.MOUSEMOTION and self.mouseDown:
                        if self.display.get_rect().collidepoint(*event.pos):
                            if self.vertical:
                                self.sliderPos = event.pos[1]
                            else:
                                self.sliderPos = event.pos[0]
                            self.drawBG()
                            self.render()
                        else: self.mouseDown = False

    
    def drawBG(self):
        """
            Draws the background colour, for a saturator this means drawing the "missing" RGB colour as a gradient.
        """
        
        if self.saturator:
            if self.colourCombi == 'RG':
                for y in range(0, self.size[1], self.size[1]/25):
                    box = pygame.Rect(0, y, 10, 10)
                    pygame.draw.rect(self.display, (self.selectedColour[0],self.selectedColour[1],y), box, 0)
                    self.selectedColour = (self.selectedColour[0],self.selectedColour[1],self.sliderPos)
            elif self.colourCombi == 'RB':
                for y in range(0, self.size[1], self.size[1]/25):
                    box = pygame.Rect(0, y, 10, 10)
                    pygame.draw.rect(self.display, (self.selectedColour[0],y,self.selectedColour[2]), box, 0)
                    self.selectedColour = (self.selectedColour[0],self.sliderPos,self.selectedColour[2])
            elif self.colourCombi == 'GB':
                for y in range(0, self.size[1], self.size[1]/25):
                    box = pygame.Rect(0, y, 10, 10)
                    pygame.draw.rect(self.display, (y,self.selectedColour[1],self.selectedColour[2]), box, 0)
                    self.selectedColour = (self.sliderPos,self.selectedColour[1],self.selectedColour[2])
                
                
        else: 
            self.display.fill( self.bgcolour )
            pygame.draw.rect(self.display, (0,0,0),
                                self.display.get_rect(), 2)
    #  pygame.draw.rect(self.display, (0,0,0),
    #                      self.display.get_rect(), 2)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        
    def render(self):
        """Draw the border and puck onto the surface"""
        if self.saturator:
            self.send(((self.messagePrefix,self.selectedColour),), "outbox")
        else: 
            self.send(((self.messagePrefix,self.sliderPos),), "outbox")
        if self.vertical:
            box = pygame.Rect(0, self.sliderPos, self.size[0], 5)

        else:
            box = pygame.Rect(self.sliderPos, 0, 5, self.size[1])
        pygame.draw.rect(self.display, (0,0,0), box,0)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")
        

if __name__ == "__main__":
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline(Slider(size=(100,255), position=(10,0 )),
            ConsoleEchoer()).run()


    Axon.Scheduler.scheduler.run.runThreads()  
    
# Licensed to the BBC under a Contributor Agreement: JT/DK
