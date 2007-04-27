#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
# Fun little tool for editting pictures.
# This is designed with the expectation that multiple surfaces will be
# used to allow translucency.
#


import Axon
import pygame
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.UI.Tk.TkWindow import TkWindow
import Tkinter

component = Axon.Component.component
WaitComplete = Axon.Ipc.WaitComplete

class Palette(TkWindow):
    Inboxes = ["inbox", "control", "colourchange"]
    def __init__(self, title, text):
        self.title = title
        self.text  = text
        super(Palette,self).__init__()

    def bigger(self): self.send("bigger\n", "outbox")
    def smaller(self): self.send("smaller\n", "outbox")
    def red_change(self,arg): 
           self.send("red "+str(arg)+"\n", "outbox")
    def green_change(self,arg): 
           self.send("green "+str(arg)+"\n", "outbox")
    def blue_change(self,arg): 
           self.send("blue "+str(arg)+"\n", "outbox")

    def setupWindow(self):
        self.window.title(self.title)

        self.label = Tkinter.Label(self.window, text=self.text)
        self.label.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)

        self.colour = Tkinter.Canvas(self.window, width="1i", height="1i")
        self.colour.grid(row=0, column=1, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.colour.create_rectangle(0, 0, 100, 100, tags="thing", fill="#000000")

        self.bigger = Tkinter.Button(self.window, text='bigger', command=self.bigger)
        self.smaller = Tkinter.Button(self.window, text='smaller', command=self.smaller)

        self.bigger.grid(row=1, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.smaller.grid(row=2, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)

        self.red = Tkinter.Scale(from_=0, to=255, command=self.red_change)
        self.green = Tkinter.Scale(from_=0, to=255, command=self.green_change)
        self.blue = Tkinter.Scale(from_=0, to=255, command=self.blue_change)

        self.red.grid(row=3, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.green.grid(row=3, column=1, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.blue.grid(row=3, column=2, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

    def main(self):
        X = super(Palette, self).main()
        while 1:
            X.next()
            if self.dataReady("colourchange"):
                colour = self.recv("colourchange")
                R = "#"
                for r in colour:
                    J = hex(r)[2:]
                    if len(J)==1:
                       J = "0"+J
                    R += J
                self.colour.delete("thing")
                self.colour.create_rectangle(0, 0, 100, 100, tags="thing", fill=R)
            yield 1

class PygameApp(Axon.Component.component):
    " This reimplements a variety of ideas already in use in Matt's Pygame App code "
    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def handleAlpha(self):
        if self.dataReady("alphacontrol"):
            alpha = self.recv("alphacontrol")
            self.display.set_alpha(alpha)

    def requestDisplay(self, **argd):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displaysignal"), displayservice)
        self.send(argd, "displaysignal")
        for _ in self.waitBox("displaycontrol"): yield 1
        display = self.recv("displaycontrol")
        self.display = display

class Painter(PygameApp):
    Inboxes = [ "inbox", "control", "alphacontrol", "displaycontrol", "events" ]
    Outboxes = ["signal", "outbox", "displaysignal","colour" ]

    def __init__(self):
        super(Painter,self).__init__()
        self.brush = SimpleBrush()

    def draw(self, data):
        self.brush.render(self.display, data.button, data.pos)
        self.send({"REDRAW":True, "surface":self.display}, "displaysignal")
        
    def main(self):
        yield WaitComplete(
                  self.requestDisplay(DISPLAYREQUEST=True,
                                      callback = (self,"displaycontrol"),
                                      events = (self, "events"),
                                      size = (1024, 768),
                                      position = (0,0)
                            )
              )

        self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                    "surface" : self.display},
                    "displaysignal")
        self.display.fill( (255,255,255) )
        self.send({"REDRAW":True, "surface":self.display}, "displaysignal")
        drag = False
        while 1:
            self.handleAlpha()
            while self.dataReady("events"):
                 message = self.recv("events")
                 for data in message:
                     if data.type == pygame.MOUSEBUTTONDOWN:
                         if 1 <= data.button <=3:
                             self.draw(data)
                         drag = True
                         drag_button = data.button
                         self.send({ "ADDLISTENEVENT" : pygame.MOUSEMOTION,
                                     "surface" : self.display},
                                     "displaysignal")
                         self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                                     "surface" : self.display},
                                     "displaysignal")
                     if drag:
                         if data.type == pygame.MOUSEMOTION:
                             data.button = drag_button
                             if 1 <= data.button <=3:
                                 self.draw(data)
                     if data.type == pygame.MOUSEBUTTONUP:
                         drag = False

                 yield 1

            while self.dataReady("inbox"):
                yield 1
                message = self.recv("inbox")
                command, args = message[0], message[1:]
                if command == "size":
                    size = int(args[0])
                    self.brush.setsize(size)
                if command == "colour":
                    colour = ( int(args[0]), int(args[1]), int(args[2]) )
                    try:
                        self.brush.setcolour(colour, button = int(args[3]))
                    except IndexError:
                        self.brush.setcolour(colour)
                if command == "bigger": self.brush.bigger()
                if command == "smaller": self.brush.smaller()
                if command == "red":
                    c = self.brush.redset(int(args[0]))
                    self.send(c, "colour")
                if command == "green": 
                    c = self.brush.greenset(int(args[0]))
                    self.send(c, "colour")
                if command == "blue": 
                    c = self.brush.blueset(int(args[0]))
                    self.send(c, "colour")

            yield 1

class SimpleBrush(object):
    def __init__(self):
        self.colour = [ None, (240,32,32), (32,240,32), (255, 255, 255) ]
        self.size = 5
    def render(self, surface, colour_index, position):
        pygame.draw.circle(surface, self.colour[colour_index], position, self.size)
    def setsize(self, size):
        self.size = size
    def setcolour(self, colour, index=1):
        self.colour[index] = colour
    def redset(self, level):
        colour = self.colour[1]
        self.colour[1] = level, colour[1], colour[2]
        return colour
    def greenset(self, level):
        colour = self.colour[1]
        self.colour[1] = colour[0], level, colour[2]
        return colour
    def blueset(self, level):
        colour = self.colour[1]
        self.colour[1] = colour[0], colour[1], level
        return colour
    def bigger(self):
        self.size += 5
    def smaller(self):
        self.size -= 5
        if self.size <1: self.size =1


def main(*args): 
    Graphline(
        PALETTE = Palette("Palette","Brush"),
        CONSOLE = ConsoleReader(">>> "),
        LINESTOKENS = lines_to_tokenlists(),
        PAINT = Painter(),
        linkages = {
            ("CONSOLE", "outbox"): ("LINESTOKENS","inbox"),
            ("LINESTOKENS", "outbox"): ("PAINT","inbox"),
            ("PALETTE", "outbox"): ("LINESTOKENS","inbox"),
            ("PAINT", "colour") : ("PALETTE", "colourchange"),
        }
    ).run()

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
