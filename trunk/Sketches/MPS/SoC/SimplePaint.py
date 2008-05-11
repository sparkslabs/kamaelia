#!/usr/bin/python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Simplified version of the trivial paint program I wrote. This version is
# augmented to simplify seeing whats going on inside the system, taking advantage
# of the fact that data sent to an outbox that isn't connected to anything doesn't
# result in a memory leak :-)
#


import Axon
import pygame
from Kamaelia.UI.PygameDisplay import PygameDisplay

component = Axon.Component.component
WaitComplete = Axon.Ipc.WaitComplete

class PygameApp(Axon.Component.component):
    " This reimplements a variety of ideas already in use in Matt's Pygame App code "
    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def requestDisplay(self, **argd):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displaysignal"), displayservice)
        self.send(argd, "displaysignal")
        for _ in self.waitBox("displaycontrol"): yield 1
        display = self.recv("displaycontrol")
        self.display = display

class SimpleBrush(object):
    def __init__(self):
        self.colour = [ None, (240,32,32), (32,240,32), (255, 255, 255) ]
        self.size = 5
    def describe(self):
        return { "size": self.size, "colours" : self.colour[1:] }
    def render(self, surface, colour_index, position):
        pygame.draw.circle(surface, self.colour[colour_index], position, self.size)

class Painter(PygameApp):
    Inboxes = [ "inbox", "control", "displaycontrol", "events" ]
    Outboxes = ["signal", "outbox", "displaysignal","colour", "logging" ]

    def __init__(self, size=(1024,768), position=(0,0)):
        super(Painter,self).__init__()
        self.brush = SimpleBrush()
        self.size = size[:]
        self.position = position[:]

    def draw(self, data):
        self.brush.render(self.display, data.button, data.pos)
        action = {"action": "render", "position": data.pos }
        action.update(self.brush.describe())
        self.send( action, "logging")
        self.send({"REDRAW":True, "surface":self.display}, "displaysignal")
        
    def main(self):
        yield WaitComplete(
                  self.requestDisplay(DISPLAYREQUEST=True,
                                      callback = (self,"displaycontrol"),
                                      events = (self, "events"),
                                      size = self.size,
                                      position = self.position,
                            )
              )

        self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                    "surface" : self.display},
                    "displaysignal")
        self.display.fill( (255,255,255) )
        self.send({"REDRAW":True, "surface":self.display}, "displaysignal")
        drag = False
        while 1:
            while not self.anyReady():
                self.pause()
                yield 1
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
            yield 1


if __name__ == "__main__":
    print """
This is a very simple paint program, with 2 very simple modes of usage.
If this is being run with run_simply set to True, then it's being run
completely standalone, so you can see that it's just a simple scribber.

If run_simply is set to false, then a console echoer is connected to
the logging outbox of the Painter, so you can see what's happening when
a mouse is clicked and dragged. This is to make it clearer what's going
on inside the Painter for debugging purposes.

The "run_simply" mode also shows the usage as to how to request a
display position and a surface size.
"""
    run_simply = False
    if run_simply:
       Painter().run()
    else:
       from Kamaelia.Util.Graphline import Graphline
       from Kamaelia.Util.Console import ConsoleEchoer
       import Axon

       from pprint import saferepr
       class myfilter(Axon.Component.component):
           def mainBody(self):
                   if not self.anyReady():
                       self.pause()
                       return 1
                   while self.dataReady("inbox"):
                       self.send( saferepr(self.recv())+"\n", "outbox")
                   return 1

       Graphline(
           PAINTER = Painter(size=(800,600), position=(100,75)),
           FORMATTER = myfilter(),
           DEBUG = ConsoleEchoer(),
           linkages = {
              ("PAINTER", "logging") : ("FORMATTER", "inbox"),
              ("FORMATTER", "outbox") : ("DEBUG", "inbox"),
           },
       ).run()

