#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# from math import *
import sys
import Axon
import pygame
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import *

import Actions

class PygameComponent(Axon.Component.component):
   """
   Borrows ideas from Kamaelia.UI.MH.PyGameApp.PyGameApp & mainly from Ticker
   """
   Inboxes = { "inbox"        : "Specify (new) filename",
               "display_control"      : "Shutdown messages & feedback from Pygame Display service",
               "alphacontrol" : "Transparency of the ticker (0=fully transparent, 255=fully opaque)",
               "control" : "...",
               "events" : "...."
             }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "",
                "displaysignal" : "Shutdown signalling & sending requests to Pygame Display service",
              }
   configuration = {
      "transparency" : "Colour to be made transparent. None == no colour transparent",
   }
   transparency = None
   background = 0xffffff
   surfacesize = (1024, 768)
   surfaceposition=(0,0)
   onlymouseinside = False
   def __init__(self, **argd):
       super(PygameComponent,self).__init__(**argd)
       self.eventHandlers = {}

   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      while True:
         if self.dataReady(boxname): return
         else: yield 1

   def flip(self):
       self.send({"REDRAW":True, "surface":self.display}, "displaysignal")

   def requestDisplay(self, **argd):
      """\
      Generator. Gets a display surface from the Pygame Display service.

      Makes the request, then yields 1 until a display surface is returned.
      """
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"displaysignal"), displayservice)
      self.send(argd, "displaysignal")
      for _ in self.waitBox("display_control"): yield 1
      display = self.recv("display_control")
      self.display = display

   def handleAlpha(self):
       if self.dataReady("alphacontrol"):
            alpha = self.recv("alphacontrol")
            self.display.set_alpha(alpha)

   def doRequestDisplay(self):
        return WaitComplete(
                 self.requestDisplay(DISPLAYREQUEST=True,
                                     callback = (self,"display_control"),
                                     events = (self, "events"),
                                     size = self.surfacesize,
                                     transparency = self.transparency,
                                     position = self.surfaceposition,
                                     onlymouseinside = self.onlymouseinside, ### Tempted to do events depth instead
                 )
               )

   def clearDisplay(self):
       """Clears the ticker of any existing text."""
       self.display.fill(self.background)

   def addHandler(self, eventtype, handler):
        """\
        Add an event handler, for a given PyGame event type.

        The handler is passed the pygame event object as its argument when called.
        """
        if not self.eventHandlers.has_key(eventtype):
            self.eventHandlers[eventtype] = []
            self.send({ "ADDLISTENEVENT" : eventtype,
                        "surface" : self.display,
                      }, "displaysignal")
        self.eventHandlers[eventtype] += [handler]
        return handler

   def removeHandler(self, eventtype, handler):
       """Remove the specified pygame event handler from the specified event."""
       if self.eventHandlers.has_key(eventtype):
           try:
               self.eventHandlers[eventtype].remove(handler) # Latent bugs in application will cause an error here
           except ValueError:
               pass
           if len(self.eventHandlers[eventtype]) == 0:
               print "NO HANDLER LEFT"

   def events(self):
       """Generator. Receive events on "events" inbox and yield then one at a time."""
       while self.dataReady("events"):
          event_bundle = self.recv("events")
          for event in event_bundle:
             yield event

   def _dispatch(self):
        """\
        Internal pygame event dispatcher.
        For all events received, it calls all event handlers in sequence
        until one returns True.
        """
        for event in self.events():
            if self.eventHandlers.has_key(event.type):
                for handler in self.eventHandlers[event.type]:
                    if handler(event):
                        break

class GameDisplay(PygameComponent):
    surfacesize = 1024, 768
    background = 0x000000
    ballx = 512
    bally = 384
    ballradius = 10
    def renderBall(self):
        self.clearDisplay()
        pygame.draw.circle(self.display, (255,255,255), (self.ballx, self.bally), self.ballradius)
        self.flip()
    def main(self):
        yield self.doRequestDisplay()
        self.renderBall()
        while 1:
            while not self.anyReady():
                self.pause()
                yield 1
            while self.dataReady("inbox"):
                m = self.recv("inbox")
                if m[0] == "ballpos":
                    self.ballx = m[1]
                    self.bally = m[2]
                    self.renderBall()

import time
class GameModel(Axon.ThreadedComponent.threadedcomponent):
    max_x,max_y = 1024, 768
    dx,dy = 10,10
    x,y = 512,384
    def moveball(self):
        self.x = (self.x+self.dx)
        if (self.x > self.max_x) or self.x < 0:
            self.dx = -self.dx
            self.x = (self.x+self.dx)
        self.y = (self.y+self.dy)
        if (self.y > self.max_y) or self.y < 0:
            self.dy = -self.dy
            self.y = (self.y+self.dy)
    def main(self):
        while 1:
            self.send(("ballpos", self.x,self.y), "outbox")
            self.moveball()
            time.sleep(0.04)

Backplane("GameEvents").activate()
if sys.argv[1] == "server":

    def ClientProtocol():
        return Pipeline(
                    SubscribeTo("GameEvents"),
                    PureTransformer(lambda x : "|".join([str(y) for y in x])+"X")
               )

    SimpleServer(port=1601, protocol=ClientProtocol).activate()

    Pipeline(
        GameModel(),
        PublishTo("GameEvents"),
    ).activate()

else:
    B = ""
    def unmarshall(x):
        global B
        B = B+x
        if B.find("X") != -1:
            L = B[:B.find("X")]
            B = B[B.find("X")+1:]
            L = L.split("|")
            L[1] = int(L[1])
            L[2] = int(L[2])
            return L
        return (1,1,1)
    Pipeline(
        TCPClient(sys.argv[1], 1601),
        PureTransformer(lambda x : unmarshall(x)),
        PublishTo("GameEvents")
    ).activate()

Pipeline(
    SubscribeTo("GameEvents"),
    GameDisplay()
).run()



