#!/usr/bin/python

import time
import pygame
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay

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

class mixin(object):
    pass

class MyDrawer(mixin):
    offset = 0,0
    scale = 0.5
    def pygame_font_Font(self, Foo, Size):
        return pygame.font.Font(Foo, self.scale*(Size))

    def makeLabel(self, text):
        font = self.pygame_font_Font(None, 14)
        textimage = font.render(text,True, (0,0,0),)
        (w,h) = [ x/self.scale for x in textimage.get_size() ]
        return textimage, w,h

    def pygame_draw_line(self,
                         surface,
                         colour,
                         startpos,
                         endpos,
                         width=1):
        pygame.draw.line(surface,
                         colour,
                        (self.scale*(startpos[0]+self.offset[0]),self.scale*(startpos[1]+self.offset[1])),
                        (self.scale*(endpos[0]+self.offset[0]),self.scale*(endpos[1]+self.offset[1])),
                         width)

    def pygame_draw_rect(self,
                         surface,
                         colour,
                         rect,
                         width=0):
        pygame.draw.rect(surface, colour, 
                         (self.scale*(rect[0][0]+self.offset[0]),
                          self.scale*(rect[0][1]+self.offset[1]),
                          self.scale*(rect[1][0]),
                          self.scale*(rect[1][1])),
                         width)
        return rect

    def display_blit( self, image, position ):
        self.display.blit( image, (self.scale*(position[0]+ self.offset[0]),self.scale*(position[1]+ self.offset[1])) )

    def drawLine(self, line):
        self.pygame_draw_line(self.display, 0, line[0], line[1], 2)

    def drawPath(self, path):
        for line in path:
            self.drawLine(line)

    def drawBox(self, box):
        try:
            self.nodes[box]
        except KeyError:
            return
        colour = 0xaaaaaa
        if box == self.selected :
            colour = 0xff8888
        self.pygame_draw_rect(self.display, colour, (self.boxes[box],(self.width,self.height)), 0)
        cx = (self.boxes[box][0]+self.width/2)
        cy = (self.boxes[box][1]+self.height/2)
        image, w,h = self.makeLabel( self.nodes[box] )
        self.display_blit( image, (cx-w/2,cy-h/2) )
        if box in self.topology:
           self.drawTree(box)

    def drawTree(self, tree):
        box = tree
        w = self.width
        h = self.height
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

    def clickInBox(self, pos):
        for box in self.boxes:
            if self.scale*(self.boxes[box][0]+self.offset[0]) <= pos[0] <= self.scale*(self.boxes[box][0]+self.width+self.offset[0]):
                if self.scale*(self.boxes[box][1]+self.offset[1]) <= pos[1] <= self.scale*(self.boxes[box][1]+self.height+self.offset[1]):
                    return box
        return None # explicit better than implicit

class MyFoo(MyDrawer,PygameComponent):
    configuration = {
       "transparency" : "Colour to be made transparent. None == no colour transparent",
       "boxsize" : "(width,height) representing size of the boxes",
       "width" : "width of the boxes (yes, I know, this *is* in /Sketches right now",
       "height" : "height of the boxes (yes, I know, this *is* in /Sketches right now",
       "hspacing" : "minimum spacing between boxes horizontally",
       "vspacing" : "minimum spacing between boxes vertically",
       "nodes" : "initial mapping of node ids to node labels. Dict of int to string",
       "topology" : "mapping of int -> [list of int] (nodes & child nodes)",
       "boxes" : "mapping of int -> (int,int) initial positions of boxes on surface",
    }
    nodes = { }
    topology = { }
    boxes = {}
    transparency = 0xffffff
    boxsize = (100,50)
    width = 100
    hspacing = 10
    height = 50
    vspacing = 50
    onlymouseinside = True

    def redraw(self):
        self.clearDisplay()
        self.drawBox(1)
        self.flip()

    def reDoTopology(self):
        self.boxes = {}
        self.layout_tree(1, self.topology,0,100)
        self.redraw()

    def select(self, nodeid):
        self.selected = nodeid
        self.send(["SELECT", self.selected ], "outbox")
        \
self.redraw()
#        self.reDoTopology()

    def deselect(self):
        print "DESELECTED", self.selected 
        self.selected = None
        self.send(["DESELECT"], "outbox")
#        \
#self.redraw()
        self.reDoTopology()

    def mousedown_handler(self,*events, **eventd):
        selected = self.selected
        for event in events:
            if event.button == 1:
                nodeid= self.clickInBox(event.pos)
                if nodeid:
                    self.select(nodeid)
                else:
                    self.deselect()

    def layout_tree(self, box, topology, wx, wy):
        "yes, this took a considerable amount of faffing about"
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

    def mousedown_handler(self,*events, **eventd):
        selected = self.selected
        for event in events:
            if event.button == 1:
                nodeid= self.clickInBox(event.pos)
                if nodeid:
                    self.select(nodeid)
                    self.holding = nodeid
                    print "grabbing", self.holding
                    self.addHandler(pygame.MOUSEMOTION, self.mousemove_handler)
                else:
                    self.deselect()

    def mouseup_handler(self, *events, **eventd):
        self.removeHandler(pygame.MOUSEMOTION, self.mousemove_handler)
        print "releasing", self.holding,
        self.holding = None
        for event in events:
            if event.button == 1:
                print "here", event.pos

    def mousemove_handler(self,*events, **eventd):
        pass

    def keydown_handler(self,*events, **eventd):
        for event in events:
            print event, event.key, dir(event)
            if event.key in [273,274,275,276,61,45]:
                if event.key == 273: # UP
                    self.dy = -3
                if event.key == 274: # DOWN
                    self.dy = 3
                if event.key == 275: # RIGHT
                    self.dx = 3
                if event.key == 276: # LEFT
                    self.dx = -3
                if event.key == 61: # PLUS
                    self.ds = 1.05
                if event.key == 45: # MINUS
                    self.ds = 1/1.05

    def keyup_handler(self,*events, **eventd):
        for event in events:
            print event, event.key, dir(event)
            if event.key in [273,274,275,276,61,45]:
                if event.key == 273: # UP
                    self.dy = 0
                if event.key == 274: # DOWN
                    self.dy = 0
                if event.key == 275: # RIGHT
                    self.dx = 0
                if event.key == 276: # LEFT
                    self.dx = 0
                if event.key == 61: # PLUS
                    self.ds = 0
                if event.key == 45: # MINUS
                    self.ds = 0

    def update_offset(self):
        pass

    def main(self):
        """Main loop."""
        yield self.doRequestDisplay()
        self.holding = None
        self.dx = 0
        self.dy = 0
        self.ds = 0

        self.addHandler(pygame.MOUSEBUTTONDOWN, self.mousedown_handler)
        self.addHandler(pygame.MOUSEBUTTONUP, self.mouseup_handler)
        self.addHandler(pygame.KEYDOWN, self.keydown_handler)
        self.addHandler(pygame.KEYUP,   self.keyup_handler)

        self.selected = None
        self.offset = [x for x in self.offset]
        self.scale = self.scale
        self.reDoTopology()
        while 1:
            self._dispatch()
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command[0] == "replace":
                    self.topology = command[1]
                    self.deselect()
                    self.reDoTopology()
                if command[0] == "add":
                    nodeid, label, parent = command[1:]
                    self.nodes[nodeid] = label
                    try:
                       self.topology[parent].append(nodeid)
                    except KeyError:
                        self.topology[parent] = [nodeid]
                    self.reDoTopology()
                if command[0] == "relabel":
                    nodeid, newlabel = command[1:]
                    self.nodes[nodeid] = newlabel
                    self.redraw()
                if command[0] == "select":
                    nodeid, = command[1:]
                    self.select(nodeid)
                    self.redraw()
                if command[0] == "deselect":
                    self.deselect()
                    self.redraw()
                if command[0] == "del":
                    if command[1] == "all":
                        self.selected = None
                        self.topology = {}
                        self.boxes = {}
                        self.nodes = {}
                        self.deselect()
                    if command[1] == "node":
                        try:
                            del self.boxes[command[2]]
                            if command[2] == self.selected:
                                self.deselect()
                        except KeyError:
                            pass
                        try:
                            del self.nodes[command[2]]
                        except KeyError:
                            pass
                        try:
                            del self.topology[command[2]]
                        except KeyError:
                            pass
                        for node in self.topology:
                            if command[2] in self.topology[node]:
                                self.topology[node] = [x for x in self.topology[node] if x != command[2] ]
                    self.reDoTopology()
                if command[0] == "get":
                    if command[1] == "all":
                        self.send((self.nodes, self.topology), "outbox")
                    if command[1] == "node":
                        n = {command[2] : self.nodes[command[2]]}
                        t = {command[2] : self.topology.get(command[2],[])}
                        self.send((n, t), "outbox")
            if self.dx != 0 or self.dy != 0 or self.ds !=0:
                if self.dx != 0 or self.dy:
                   self.offset[0] += self.dx
                   self.offset[1] += self.dy
                if self.dx >0: self.dx += 2
                if self.dx <0: self.dx -= 2
                if self.dy >0: self.dy += 2
                if self.dy <0: self.dy -= 2

                if self.ds !=0: self.scale = self.scale*self.ds
                self.redraw()
            yield 1

class MyBoxes(MyFoo):
    configuration = {
       "transparency" : "Colour to be made transparent. None == no colour transparent",
       "boxsize" : "(width,height) representing size of the boxes",
       "width" : "width of the boxes (yes, I know, this *is* in /Sketches right now",
       "height" : "height of the boxes (yes, I know, this *is* in /Sketches right now",
       "hspacing" : "minimum spacing between boxes horizontally",
       "vspacing" : "minimum spacing between boxes vertically",
       "nodes" : "initial mapping of node ids to node labels. Dict of int to string",
       "topology" : "mapping of int -> [list of int] (nodes & child nodes)",
       "boxes" : "mapping of int -> (int,int) initial positions of boxes on surface",
    }
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

class Source(Axon.Component.component):
    configuration = {
       "iterable": "Something that can be iterated through as in 'for x in iterable', "
                   "list, dict, generator etc",
       "delay" : "Delay between sending messages",
    }
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
]

relabel_commands = [
    ["del", "all"],
    ["add", 1, "1", None ],
    ["add", 2, "2", 1 ],
    ["add", 3, "3", 1 ],
    ["add", 4, "4", 1 ],
    ["add", 5, "5", 1 ],
    ["add", 6, "6", 3 ],
    ["add", 7, "7", 3 ],
    ["add", 8, "8", 4 ],
    ["add", 9, "9", 4 ],
    ["add", 10, "10", 9 ],
    ["add", 11, "11", 10 ],
    ["add", 12, "12", 10 ],
    ["add", 13, "13", 10 ],

    ["del", "node", 6],
    ["del", "node", 7],
    ["del", "node", 3],
    ["del", "node", 8],
    ["select", 1 ],
    ["select", 2 ],
    ["select", 3 ],
    ["select", 6 ],
    ["select", 7 ],
    ["select", 4 ],
    ["select", 8 ],
    ["select", 9 ],
    ["select", 10 ],
    ["select", 11 ],
    ["select", 12 ],
    ["select", 13 ],
    ["select", 5 ],
    ["deselect"],
    
    ["relabel", 2, "init" ],
    ["relabel", 3, "setupdisplay" ],
    ["relabel", 4, "mainloop" ],
    ["relabel", 5, "exit" ],
    ["relabel", 6, "Get Display Surface" ],
    ["relabel", 7, "Set Event Options" ],
    ["relabel", 8, "Handle Shutdown" ],
    ["relabel", 9, "Loop pygame events" ],
    ["relabel", 10, "handle event" ],
    ["relabel", 11, "mouse dn 1" ],
    ["relabel", 12, "mouse dn 2" ],
    ["relabel", 13, "mouse dn 3" ],
    ["get", "all"],
    ["get", "node", 10],
    ["get", "node", 11],
    ["get", "node", 9],
]

from Kamaelia.Util.Console import ConsoleEchoer
if 0:
    Pipeline(
        Source(iterable=topologies),
        PureTransformer(lambda x : ["replace", x ]),
        MyBoxes()
    ).run()

if 0:
    Pipeline(
        Source(iterable=grow_commands),
        MyBoxes()
    ).run()

if 0:
    Pipeline(
        Source(iterable=relabel_commands, delay=0.3),
        MyBoxes(),
        PureTransformer(lambda x : str(x)+"\n"),
        ConsoleEchoer(),
    ).run()

if 0:
    import random
    from Kamaelia.UI.Pygame.Button import Button
    from Kamaelia.Chassis.Graphline import Graphline
    f = open("/usr/share/dict/words")
    l = f.readlines()
    f.close()

    def newNodeId():
        i = 1
        while 1:
            yield i
            i = i + 1

    class CoreLogic(Axon.Component.component):
        def main(self):
            nodeId = 1000
            selected = None
            while 1:
                while self.dataReady("inbox"):
                    command = self.recv("inbox")
                    if command[0] == "SELECT":
                        selected = command[1]
#                    if command[0] == "DESELECT":
#                        selected = None
                    if command[0] == "ADD":
                        if selected:
                            nodeId = nodeId + 1
                            self.send(["add", nodeId, str(nodeId), selected ],"outbox")
                            self.send(["select", nodeId ],"outbox")
                    if command[0] == "DEL":
                        if selected:
                            nodeId = nodeId + 1
                            self.send(["del", "node", selected ],"outbox")
                    if command[0] == "RELABEL":
                        if selected:
                            randomword = l[random.randint(0,len(l)-1)].strip()
                            self.send(["relabel", selected, randomword ],"outbox")
                            self.send(["select", selected ],"outbox")
                yield 1
    Graphline(
        SOURCE = Source(iterable=relabel_commands, delay=0.3),
        CLEAR = Button(caption="Clear", msg=["del", "all"], position=(0,690),size=(64,32)),
        ADD= Button(caption="Add Child Node", msg=["ADD"], position=(70,690),size=(94,32)),
        DEL= Button(caption="Del Node", msg=["DEL"], position=(170,690),size=(64,32)),
        RELABEL= Button(caption="Relabel Node", msg=["RELABEL"], position=(240,690),size=(94,32)),
        CORELOGIC = CoreLogic(),
        TOPOLOGY = MyFoo(),
        linkages = {
            ("SOURCE", "outbox"): ("TOPOLOGY","inbox"),
            ("CLEAR", "outbox"): ("TOPOLOGY","inbox"),
            ("TOPOLOGY","outbox"): ("CORELOGIC", "inbox"),
            ("ADD","outbox"): ("CORELOGIC", "inbox"),
            ("DEL","outbox"): ("CORELOGIC", "inbox"),
            ("RELABEL","outbox"): ("CORELOGIC", "inbox"),
            ("CORELOGIC","outbox"): ("TOPOLOGY", "inbox"),
        }
    ).run()


if 1:
    import random
    from Kamaelia.UI.Pygame.Button import Button
    from Kamaelia.Chassis.Graphline import Graphline
    f = open("/usr/share/dict/words")
    l = f.readlines()
    f.close()

    commands = [ ["replace", { 1: [ 2, 3, 4, 5], 3: [ 6, 7], 4: [ 8, 9], 9: [ 10], 10: [ 11, 12, 13] } ] ]
    def newNodeId():
        i = 1
        while 1:
            yield i
            i = i + 1

    class CoreLogic(Axon.Component.component):
        def main(self):
            nodeId = 1000
            selected = None
            while 1:
                while self.dataReady("inbox"):
                    command = self.recv("inbox")
                    if command[0] == "SELECT":
                        selected = command[1]
                    if command[0] == "DESELECT":
                        selected = None
                    if command[0] == "ADD":
                        if selected:
                            nodeId = nodeId + 1
                            self.send(["add", nodeId, str(nodeId), selected ],"outbox")
                    if command[0] == "DEL":
                        if selected:
                            nodeId = nodeId + 1
                            self.send(["del", "node", selected ],"outbox")
                    if command[0] == "RELABEL":
                        if selected:
                            randomword = l[random.randint(0,len(l)-1)].strip()
                            self.send(["relabel", selected, randomword ],"outbox")
                yield 1

    Graphline(
        SOURCE = Source(iterable=commands),
        CLEAR = Button(caption="Clear", msg=["del", "all"], position=(0,690),size=(64,32)),
        ADD= Button(caption="Add Child Node", msg=["ADD"], position=(70,690),size=(94,32)),
        DEL= Button(caption="Del Node", msg=["DEL"], position=(170,690),size=(64,32)),
        RELABEL= Button(caption="Relabel Node", msg=["RELABEL"], position=(240,690),size=(94,32)),
        CORELOGIC = CoreLogic(),
        TOPOLOGY = MyBoxes(background=0xffffaa,
                           surfacesize=(964,600),
                           surfaceposition=(30,30)),
        linkages = {
            ("SOURCE", "outbox"): ("TOPOLOGY","inbox"),
            ("CLEAR", "outbox"): ("TOPOLOGY","inbox"),
            ("TOPOLOGY","outbox"): ("CORELOGIC", "inbox"),
            ("ADD","outbox"): ("CORELOGIC", "inbox"),
            ("DEL","outbox"): ("CORELOGIC", "inbox"),
            ("RELABEL","outbox"): ("CORELOGIC", "inbox"),
            ("CORELOGIC","outbox"): ("TOPOLOGY", "inbox"),
        }
    ).run()
