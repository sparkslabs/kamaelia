#!/usr/bin/python

import pygame
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay

globalsurface = None

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

   def doRequestDisplay(self,size):
        return WaitComplete(
                 self.requestDisplay(DISPLAYREQUEST=True,
                                     callback = (self,"display_control"),
                                     events = (self, "events"),
                                     size = size,
                                     transparency = self.transparency,
                                     position = (0,0)
                 )
               )
   def clearDisplay(self):
       """Clears the ticker of any existing text."""
       self.display.fill(0xffffff)

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


class MyFoo(PygameComponent):
    configuration = {
       "transparency" : "Colour to be made transparent. None == no colour transparent",
       "boxsize" : "(width,height) representing size of the boxes",
       "width" : "width of the boxes (yes, I know, this *is* in /Sketches right now",
       "height" : "height of the boxes (yes, I know, this *is* in /Sketches right now",
       "hspacing" : "minimum spacing between boxes horizontally",
       "vspacing" : "minimum spacing between boxes vertically",
    }
    transparency = 0xffffff
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
        try:
            self.nodes[box]
        except KeyError:
            return
        colour = 0xaaaaaa
        if box == self.selected :
            colour = 0xff8888
        
        pygame.draw.rect(self.display, colour, (self.boxes[box],self.boxsize), 0)
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

    def reDoTopology(self):
        self.boxes = {}
        self.layout_tree(1, self.topology,0,100)
        self.clearDisplay()
        self.drawBox(1)
        self.flip()

    def clickInBox(self, pos):
        for box in self.boxes:
            if self.boxes[box][0] <= pos[0] <= self.boxes[box][0]+self.boxsize[0]:
                if self.boxes[box][1] <= pos[1] <= self.boxes[box][1]+self.boxsize[1]:
                    return box
        return None # explicit better than implicit

    def select(self, nodeid):
        self.selected = nodeid
        self.send(["SELECT", self.selected ], "outbox")
        self.reDoTopology()

    def deselect(self):
        self.selected = None
        self.send(["DESELECT"], "outbox")
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

    def main(self):
        """Main loop."""
        yield self.doRequestDisplay((1024, 768))
        global globalsurface
        globalsurface =  self.display
        self.addHandler(pygame.MOUSEBUTTONDOWN, self.mousedown_handler)
#        self.addHandler(pygame.KEYDOWN, self.event_handler)
#        self.addHandler(pygame.KEYUP,   self.event_handler)

        self.selected = None
        self.reDoTopology()
        while 1:
            self._dispatch()
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command[0] == "replace":
                    self.topology = command[1]
                if command[0] == "add":
                    nodeid, label, parent = command[1:]
                    self.nodes[nodeid] = label
                    print [nodeid, label, parent]
                    try:
                       self.topology[parent].append(nodeid)
                    except KeyError:
                        self.topology[parent] = [nodeid]
                if command[0] == "relabel":
                    nodeid, newlabel = command[1:]
                    self.nodes[nodeid] = newlabel
                if command[0] == "select":
                    nodeid, = command[1:]
                    self.select(nodeid)
                if command[0] == "deselect":
                    self.deselect()
                if command[0] == "del":
                    if command[1] == "all":
                        self.selected = None
                        self.topology = {}
                        self.boxes = {}
                        self.nodes = {}
                    if command[1] == "node":
                        try:
                            del self.boxes[command[2]]
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
                if command[0] == "get":
                    if command[1] == "all":
                        self.send((self.nodes, self.topology), "outbox")
                    if command[1] == "node":
                        n = {command[2] : self.nodes[command[2]]}
                        t = {command[2] : self.topology.get(command[2],[])}
                        self.send((n, t), "outbox")
                self.reDoTopology()
            yield 1

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
    topology = { }
    boxes = {}

import time
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
if 1:
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
        
    from pgu.gui.container import Container
    from pgu.gui.basic import Label

    class ModalBox(PygameComponent):
        def __init__(self, x = 200, y = 200, height = 250, width = 250):
            super(ModalBox, self).__init__()
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.rect = pygame.Rect(x, y, width, height)
            self.oldsurf = None
            self.widgets = []
            self.c = Container()
            self.c.add(Label('label'), 10, 10)
            self.display = globalsurface
        
        def add(self, thing, atX, atY):
            """
            atX and atY relative to self's coords
            """
            self.widgets.append(thing)
            thing.x = atX + self.x
            thing.y = atY + self.y
        
        def erase(self, surface):
            if surface == None:
                surface = self.display
            surface.blit(self.oldsurf, self.x, self.y)
        
        def draw(self, surface = None):
            if surface == None:
                surface = self.display
            print 'draw'
            self.c.paint(surface)
    #~             self.oldsurf = surface.subsurface(self.rect).copy()
    #~             pygame.draw.rect(surface, pygame.color.THECOLOURS['white'],
    #~                                           self.rect, 0)
    #~             for w in self.widgets:
    #~                 w.draw(surface)
        
        def handleMouseDown(self, e):
            if not self.rect.collidepoint(e.x, e.y):
                return None
            for w in self.widgets:
                if w.contains(e.x, e.y):
                    return w.handleMouseDown(e)
        
        def main(self):
#~             rq = {}
#~             rq['DISPLAYREQUEST']=True,
#~             rq['callback'] = (self,"display_control"),
#~             rq['events'] = (self, "events"),
#~             rq['size'] = (1024, 768)
#~             rq['position'] = (0,0)
#~             
#~             displayservice = PygameDisplay.getDisplayService()
#~             self.link((self,"displaysignal"), displayservice)
#~             self.send(rq, "displaysignal")
#~             for _ in self.waitBox("display_control"):
#~                 print 'waiting...'
#~                 yield 1
#~             display = self.recv("display_control")
            
            if not hasattr(self, 'display'):
                print 'no display'
                return
            self.draw()
            #self.addHandler(pygame.MOUSEBUTTONDOWN, self.handleMouseDown)
            while True: # modal - no yields -> captures all input?
                while self.dataReady("control"):
                    data = self.recv("control")
                    if isinstance(data, Axon.Ipc.producerFinished):
                        self.send(Axon.Ipc.producerFinished(message=display), "signal") # pass on the shutdown
                        return
                while self.dataReady('events'):
                    pass
                return
            # loop over events received:
                # pass all to relevent component

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
                    if command[0] == 'POP':
                        ModalBox().draw()
                yield 1
    
    
    
    Graphline(
        SOURCE = Source(),
        CLEAR = Button(caption="Clear", msg=["del", "all"], position=(0,690),size=(64,32)),
        ADD= Button(caption="Add Child Node", msg=["ADD"], position=(70,690),size=(94,32)),
        DEL= Button(caption="Del Node", msg=["DEL"], position=(170,690),size=(64,32)),
        RELABEL= Button(caption="Relabel Node", msg=["RELABEL"], position=(240,690),size=(94,32)),
        POPUP = Button(caption = "pop", msg = ['POP'], position = (340, 690), size = (50, 32)),
        CORELOGIC = CoreLogic(),
        TOPOLOGY = MyBoxes(),
        linkages = {
            ("SOURCE", "outbox"): ("TOPOLOGY","inbox"),
            ("CLEAR", "outbox"): ("TOPOLOGY","inbox"),
            ("TOPOLOGY","outbox"): ("CORELOGIC", "inbox"),
            ("ADD","outbox"): ("CORELOGIC", "inbox"),
            ("DEL","outbox"): ("CORELOGIC", "inbox"),
            ("RELABEL","outbox"): ("CORELOGIC", "inbox"),
            ("POPUP","outbox"): ("CORELOGIC", "inbox"),
            ("CORELOGIC","outbox"): ("TOPOLOGY", "inbox"),
        }
    ).run()
