#!/usr/bin/python

import pygame
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class PygameComponent(Axon.Component.component):
   Inboxes = { "inbox"        : "Specify (new) filename",
               "display_control"      : "Shutdown messages & feedback from Pygame Display service",
               "alphacontrol" : "Transparency of the ticker (0=fully transparent, 255=fully opaque)",
               "control" : "...",
             }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "",
                "pygamesignal" : "Shutdown signalling & sending requests to Pygame Display service",
              }
   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      while True:
         if self.dataReady(boxname): return
         else: yield 1

   def flip(self):
       self.send({"REDRAW":True, "surface":self.display}, "pygamesignal")

   def requestDisplay(self, **argd):
      """\
      Generator. Gets a display surface from the Pygame Display service.

      Makes the request, then yields 1 until a display surface is returned.
      """
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"pygamesignal"), displayservice)
      self.send(argd, "pygamesignal")
      for _ in self.waitBox("display_control"): yield 1
      display = self.recv("display_control")
      self.display = display

   def handleAlpha(self):
       if self.dataReady("alphacontrol"):
            alpha = self.recv("alphacontrol")
            self.display.set_alpha(alpha)

   def doRequestDisplay(self,size):
        return WaitComplete(
                 self.requestDisplay(DISPLAYREQUEST=True,
                                     callback = (self,"display_control"),
                                     size = size,
                                     position = (0,0)
                 )
               )
   def clearDisplay(self):
       """Clears the ticker of any existing text."""
       self.display.fill(0xffffff)

class MyFoo(PygameComponent):
    boxsize = (100,50)
    width = 100
    hspacing = 10
    height = 50
    vspacing = 50
    def makeLabel(self, text):
        font = pygame.font.Font(None, 14)
        textimage = font.render(text,True, (0,0,0),)
        (w,h) = textimage.get_size()
        return textimage, w,h

    def drawBox(self, box):
        pygame.draw.rect(self.display, 0xaaaaaa, (self.boxes[box],self.boxsize), 0)
        cx = self.boxes[box][0]+self.boxsize[0]/2
        cy = self.boxes[box][1]+self.boxsize[1]/2
        image, w,h = self.makeLabel(self.nodes[box])
        self.display.blit( image, (cx-w/2,cy-h/2) )
        if box in self.topology:
           self.drawTree(box)

    def drawLine(self, line):
        pygame.draw.line(self.display, 0,line[0],line[1],2)

    def drawTree(self, tree):
        box = tree
        w = self.boxsize[0]
        h = self.boxsize[1]
        x,y = self.boxes[box]
        paths = []
        for subbox in self.topology[box]:
            self.drawBox(subbox)
            ax,ay = self.boxes[subbox]
            paths.append(
                    [
                        (((x+w/2), y+h) , ((x+w/2), y+h+((ay-(y+h))/2) )),  # DOWN
                        (((x+w/2), y+h+((ay-(y+h))/2) ), ((ax+w/2), ay-(ay-(y+h))/2 )), # ACROSS
                        (((ax+w/2), ay-(ay-(y+h))/2 ), ((ax+w/2), ay)),  # DOWN
                    ],
            )

        for path in paths:
            self.drawPath(path)

    def drawPath(self, path):
        for line in path:
            self.drawLine(line)

    def main(self):
        """Main loop."""
        self.layout_tree(1, self.topology,0,100)
        yield self.doRequestDisplay((1024, 768))
        self.clearDisplay()
        self.drawBox(1)
        self.flip()
        while 1:
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command[0] == "replace":
                    self.topology = command[1]
                    self.boxes = {}
                    self.layout_tree(1, self.topology,0,100)
                    self.clearDisplay()
                    self.drawBox(1)
                    self.flip()
                if command[0] == "add":
                    nodeid, label, parent = command[1:]
                    self.nodes[nodeid] = label
                    try:
                       self.topology[parent].append(nodeid)
                    except KeyError:
                        self.topology[parent] = [nodeid]
                    self.boxes = {}
                    self.layout_tree(1, self.topology,0,100)
                    self.clearDisplay()
                    self.drawBox(1)
                    self.flip()
            yield 1

    def layout_tree(self, box, topology, wx, wy):
        left = wx
        nw = self.width
        row_below = wy+self.height+self.vspacing
        for subbox in topology.get(box,[]):
            nw = self.layout_tree(subbox, topology, left, row_below)
            left = left + nw+self.hspacing
        if left != wx:
            nw = left-wx-self.hspacing
        self.boxes[box] = wx+(nw/2), wy
        return nw

class MyBoxes(MyFoo):
    nodes = {
       1: "MagnaDoodle",
       2: "init",
       3: "setupdisplay",
       4: "mainloop",
       5: "exit",
       6: "Get Display Surface",
       7: "Set Event Options",
       8: "Handle Shutdown",
       9: "Loop pygame events",
      10: "handle event",
      11: "mouse dn 1",
      12: "mouse dn 2",
      13: "mouse dn 3",
    }
    topology = { }
    boxes = {}

import time
class Source(Axon.Component.component):
    iterable = []
    delay = 1
    def main(self):
        tl = time.time() 
        for item in self.iterable:
            while (time.time()-tl) < self.delay:
                yield 1
            tl = time.time() 
            yield 1
            self.send(item,"outbox")
        yield 1

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

# Sample topologies to show how the hierarchy can grow/be constructed...
topologies = [
    { 1: [ 2], },
    { 1: [ 2, 3], },
    { 1: [ 2, 3, 4], },
    { 1: [ 2, 3, 4, 5], },
    { 1: [ 2, 3, 4, 5], 3: [ 6], },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8], },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8, 9], },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8, 9], 9: [ 10], },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8, 9], 9: [ 10], 10: [ 11] },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8, 9], 9: [ 10], 10: [ 11, 12] },
    { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8, 9], 9: [ 10], 10: [ 11, 12, 13] },
]
grow_commands = [
    ["add", 2, "init", 1 ],
    ["add", 3, "setupdisplay", 1 ],
    ["add", 4, "mainloop", 1 ],
    ["add", 5, "exit", 1 ],
    ["add", 6, "Get Display Surface", 3 ],
    ["add", 7, "Set Event Options", 3 ],
    ["add", 8, "Handle Shutdown", 4 ],
    ["add", 9, "Loop pygame events", 4 ],
    ["add", 10, "handle event", 9 ],
    ["add", 11, "mouse dn 1", 10 ],
    ["add", 12, "mouse dn 2", 10 ],
    ["add", 13, "mouse dn 3", 10 ],
    ["add", 14, "mouse dn 3", 10 ],
    ["add", 15, "mouse dn 3", 10 ],
]

if 0:
    Pipeline(
        Source(iterable=topologies),
        PureTransformer(lambda x : ["replace", x ]),
        MyBoxes()
    ).run()

if 1:
    Pipeline(
        Source(iterable=grow_commands),
        MyBoxes()
    ).run()

