#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
import Axon
import pygame
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import *
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists
from Kamaelia.UI.Pygame.Image import Image

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

from math import *
class Turtle(PygameComponent):
    transparency = 0xffffff
    background = 0xffffff
    surfacesize = (570, 650)
    surfaceposition=(430,90)
    colour = (0,0,0)
    width = 10
    pos = [285,325]
    logical_pos = (0,0)
    turtle = (
            ((-50, -50), (50, -50)),
            (( 50, -50), (50,  50)),
            (( 50,  50),(-50,  50)),
            ((-50,  50),(-50, -50)),
    )
    turtle = (
            ((0, -50), (50, 50)),
            ((50, 50), (-50, 50)),
            ((-50, 50),( 0, -50)),
    )
    orientation = 0

    def rotate(self,pos):
        return (pos[0] * cos( (-pi*self.orientation)/180))+(pos[1] * sin( (-pi*self.orientation)/180)) , \
               (-pos[0] * sin( (-pi*self.orientation)/180))+(pos[1] * cos( (-pi*self.orientation)/180))

    def translate(self, pos):
        return (self.pos[0]+pos[0], self.pos[1]+pos[1])

    def render_turtle(self):
        for S,E in self.turtle:
            pygame.draw.line(self.display, self.colour,
                            self.translate(self.rotate(S)),
                            self.translate(self.rotate(E)),
                            self.width)
        self.send(self.pos, "outbox")

    def main(self):
        yield self.doRequestDisplay()
        self.clearDisplay()
        self.render_turtle()
        self.flip()
        yield 1
        tlast = self.scheduler.time
        while 1:
            yield 1
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command[0] == "forward":
                    distance = int(command[1])
                    delta = [-x for x in self.rotate( (0,distance)) ]
                    self.send("DELTA:"+repr(delta), "outbox")
                if command[0] == "back":
                    distance = -int(command[1])
                    delta = [-x for x in self.rotate( (0,distance)) ]
                    self.send("DELTA:"+repr(delta), "outbox")
                if command[0] == "left":
                    angle = int(command[1])
                    self.orientation = self.orientation - angle
                if command[0] == "right":
                    angle = int(command[1])
                    self.orientation = self.orientation + angle

class DrawingCanvas(PygameComponent):
    background = 0x820046
    surfacesize = (400, 610)
    surfaceposition=(550,20)
    x = 200
    y = 200
    orientation = 0
    width = 1
    colour = (0,0,0)
    def redraw(self):
        self.clearDisplay()
        self.flip()
    def main(self):
        """Main loop."""
        yield self.doRequestDisplay()
        self.redraw()
#        pygame.display.toggle_fullscreen() # ICK ICK ICK, but looks pwetty
        yield 1
        while 1:
            while not self.anyReady():
                self.pause()
                yield 1
            while self.dataReady("inbox"):
                self.dirty = False
                d = self.recv("inbox")
                reload(Actions)
                if (not isinstance(d, list)) and (not len(d)>0):
                    continue
                for command,handler in Actions.actions:
                    if d[0] == command:
                        handler(self, *d[1:])
                if self.dirty:
                    self.flip()
                yield 1

class Memory(Axon.Component.component):
    Outboxes = [
        "outbox",
        "signal",
        "toconsole",
    ]
    recording = False
    def __init__(self, **argd):
        super(Memory, self).__init__(**argd)
        self.noting = None
        self.notes = {}
        self.contextactions = [self.doCommand]
        self.commands = {
            "to": self.start_recording,
            "end": self.stop_recording,
        }

    def sleep(self):
        while not self.anyReady():
            self.pause()
            yield 1

    def main(self):
        while 1:
            yield WaitComplete(self.sleep())
            for d in self.Inbox("inbox"):
                try:
                    command = self.commands.get(d[0])
                except KeyError:
                    pass
                if command:
                    command(d[1:])
                else:
                    (self.contextactions[-1])(d)

    def doCommand(self,d):
        if d[0] in self.notes:
            for command in self.notes[d[0]]:
                self.send(command, "outbox")
        else:
            self.send(d, "outbox")

    def start_recording(self, d):
        if len(d) != 1:
            return
        print "recording", d[0]
        self.noting = d[0]
        self.notes[self.noting] = []
        self.contextactions.append(self.note)
        self.recording = True

    def note(self, d):
        print "Noting ", self.noting, repr(d)
        self.notes[self.noting].append(d)
        print self.notes

    def stop_recording(self, d):
        print "stopping recording", self.noting
        self.noting = None
        self.recording = False
        self.contextactions.pop()
        print self.notes

    def note(self, d):
        print "Noting ", self.noting, repr(d)
        self.notes[self.noting].append(d)
        print self.notes

if __name__ == '__main__':
    Backplane("RAWINPUT").activate()
    Backplane("PARSEDINPUT").activate()
    Backplane("DISPLAYCONSOLE").activate()


    Image(image="kamaelia_logo.png",
          bgcolour=(255,255,255),
          position=(20, 20),
          size = (64,64),
          maxpect = (64,64),
          ).activate()

    Graphline(
        RAW = SubscribeTo("RAWINPUT"),
        PARSER = text_to_tokenlists(),
        MEM = Memory(),
        PARSED = PublishTo("PARSEDINPUT"),
        linkages = {
            ("RAW","outbox"): ("PARSER","inbox"),
            ("PARSER","outbox"): ("MEM","inbox"),
            ("MEM","outbox"): ("PARSED","inbox"),

            ("RAW","signal"): ("PARSER","control"),
            ("PARSER","signal"): ("MEM","control"),
            ("MEM","signal"): ("PARSED","control"),
        }
    ).activate()

    Pipeline(
        SubscribeTo("RAWINPUT"),
        PublishTo("DISPLAYCONSOLE"),
    ).activate()

    Pipeline(
        SubscribeTo("PARSEDINPUT"),
        DrawingCanvas(background = 0xD0D0D0, # Grey!
                      surfacesize = (570, 650),
                      surfaceposition=(430,90)),
        ).activate()

    Pipeline(
        SubscribeTo("PARSEDINPUT"),
        Turtle(),
        PublishTo("DISPLAYCONSOLE"),
    ).activate()

    Pipeline(Textbox(position=(20, 640),
                     text_height=36,
                     screen_width=400,
                     screen_height=100,
                     background_color=(130,0,70),
                     text_color=(255,255,255)),
             PublishTo("RAWINPUT"),
    ).activate()

    Pipeline(SubscribeTo("DISPLAYCONSOLE"),
             TextDisplayer(position=(20, 90),
                           text_height=36,
                           screen_width=400,
                           screen_height=540,
                           background_color=(130,0,70),
                           text_color=(255,255,255))
    ).run()
