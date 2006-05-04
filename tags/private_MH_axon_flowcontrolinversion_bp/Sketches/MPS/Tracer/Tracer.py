#!/usr/bin/python

import Axon

from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.PipelineComponent import pipeline
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Util.ConsoleEcho import consoleEchoer


class dataRecorder(Axon.Component.component):

    def __init__(self):
        super(dataRecorder, self).__init__()
        self.messages = []
        self.current = -1

    def do(self):
        self.current += 1
        value = self.messages[self.current]
        return value

    def undo(self):
        if self.current == -1: raise IndexError
        value = self.messages[self.current]
        value = self.revert(value)
        self.current -= 1
        return value
        
    def revert(self, value):
        return value

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                self.messages.append(self.recv("inbox"))
            if self.dataReady("control"):
                message = self.recv("control")
                if message[0] == "NEXT":
                    try:
                        messagesend = self.do()
                        self.send(messagesend, "outbox")
                    except IndexError:
                        "Fell off the end", self.current
                        self.current = len(self.messages) -1
                elif message[0] == "PREV":
                    try:
                        messagesend = self.undo()
                        self.send(messagesend, "outbox")
                    except IndexError:
                        "Fell off the beginning", self.current
                        self.current = -1
            yield 1

class topologyRecorder(dataRecorder):
    """Worth noting that reverting a topology is not a trivial matter 
    
       Kamaelia Present works with slides at a time, which clear the
       display before drawing a topology, generally speaking. This is
       much more tractable for a data recorder
       
       It should be clear from this that this subclass provides a policy
       mechanism
    """

    def revert(self, value):
        value = [x for x in value]
        if value[0] == "ADD" and value[1] == "LINK":
           value[0] = "DEL"
           return value
        if value[0] == "ADD" and value[1] == "NODE":
           value = [ "DEL", "NODE", value[2] ]
           return value
        print "WARNING, I HAVE NO IDEA HOW TO REVERT", value
        return value
        
################################################
#
# Test Harness code
#
################################################

class LineSplit(Axon.Component.component):
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                lines = data.split("\n")
                for line in lines:
                    self.send(line, "outbox")
                    yield 1

class source(Axon.Component.component):
    def __init__(self,data):
        super(source, self).__init__()
        self.data = data
    def main(self):
        self.send(self.data, "outbox")
        yield 1


class muxTwo(Axon.Component.component):
    Inboxes={ "inbox" : "default",
              "control": "default",
              "primary" : "Main data control",
              "secondary" : "Secondart data control",
    }
    def main(self):
        while 1:
            ready = False
            source1 = None
            source2 = None

            #These next two force a synchronisation
            while not self.dataReady("primary"):
                 yield 1
            source1 = self.recv("primary")
            while not self.dataReady("secondary"): 
                 yield 1
            source2 = self.recv("secondary")

            # This forces a time delay
            self.send((source1,source2), "outbox")
            yield 1

class Comparator(Axon.Component.component):
     def main(self):
         while 1:
             while self.dataReady("inbox"):
                data = self.recv("inbox")
                item1, item2 = data
                if item1 == item2:
                   self.send("SUCCESS\n", "outbox")
                else:
                   self.send("FAIL"+str(data)+"\n", "outbox")
                yield 1
             self.pause()
             yield 1

topology = """ADD NODE 1 one auto -
ADD NODE 2 two auto -
ADD NODE 3 three auto -
ADD LINK 1 2
ADD LINK 2 3
ADD LINK 1 3
"""

commands = """NEXT
NEXT
NEXT
NEXT
NEXT
NEXT
NEXT
PREV
PREV
PREV
PREV
PREV
PREV
NEXT
NEXT
PREV
NEXT
PREV
"""

dataRecorderExpected = """ADD NODE 1 one auto -
ADD NODE 2 two auto -
ADD NODE 3 three auto -
ADD LINK 1 2
ADD LINK 2 3
ADD LINK 1 3
ADD LINK 1 3
ADD LINK 2 3
ADD LINK 1 2
ADD NODE 3 three auto -
ADD NODE 2 two auto -
ADD NODE 1 one auto -
ADD NODE 1 one auto -
ADD NODE 2 two auto -
ADD NODE 2 two auto -
ADD NODE 2 two auto -
ADD NODE 2 two auto -
"""

topologyRecorderExpected = """ADD NODE 1 one auto -
ADD NODE 2 two auto -
ADD NODE 3 three auto -
ADD LINK 1 2
ADD LINK 2 3
ADD LINK 1 3
DEL LINK 1 3
DEL LINK 2 3
DEL LINK 1 2
DEL NODE 3
DEL NODE 2
DEL NODE 1
ADD NODE 1 one auto -
ADD NODE 2 two auto -
DEL NODE 2
ADD NODE 2 two auto -
DEL NODE 2
"""


NonInteractiveDataTester = Graphline(
    SOURCE = pipeline(source(topology),
                       LineSplit(),
                       lines_to_tokenlists(),
              ),
    CONTROLLER = pipeline(source(commands),
                       LineSplit(),
                       lines_to_tokenlists(),
              ),
    EXPECTED = pipeline(source(dataRecorderExpected),
                        LineSplit(),
                        lines_to_tokenlists(),
              ),
    MUXER = muxTwo(),
    DR = dataRecorder(),
    DISPLAY = consoleEchoer(),
    TRACE = consoleEchoer(forwarder=True),
    RESULT = Comparator(),
    linkages = {
        ("SOURCE", "outbox") : ("DR", "inbox"),
        ("CONTROLLER", "outbox") : ("DR", "control"),
        ("DR", "outbox") : ("MUXER", "primary"),
        ("EXPECTED", "outbox") : ("MUXER", "secondary"),
        ("MUXER", "outbox") : ("RESULT", "inbox"),
        ("RESULT", "outbox") : ("DISPLAY", "inbox"),
    }
)

NonInteractiveTopologyTester = Graphline(
    SOURCE = pipeline(source(topology),
                       LineSplit(),
                       lines_to_tokenlists(),
              ),
    CONTROLLER = pipeline(source(commands),
                       LineSplit(),
                       lines_to_tokenlists(),
              ),
    EXPECTED = pipeline(source(topologyRecorderExpected),
                        LineSplit(),
                        lines_to_tokenlists(),
              ),
    MUXER = muxTwo(),
    DR = topologyRecorder(),
    DISPLAY = consoleEchoer(),
    TRACE = consoleEchoer(forwarder=True),
    RESULT = Comparator(),
    linkages = {
        ("SOURCE", "outbox") : ("DR", "inbox"),
        ("CONTROLLER", "outbox") : ("DR", "control"),
        ("DR", "outbox") : ("MUXER", "primary"),
        ("EXPECTED", "outbox") : ("MUXER", "secondary"),
        ("MUXER", "outbox") : ("RESULT", "inbox"),
        ("RESULT", "outbox") : ("DISPLAY", "inbox"),
    }
)

InteractiveTester = Graphline(
    SOURCE = pipeline( source(topology),
                   LineSplit(),
                   lines_to_tokenlists(),
             ),
    NEXT = Button(caption="Next", msg=["NEXT"], position=(72,8)),
    PREVIOUS = Button(caption="Previous", msg=["PREV"],position=(8,8)),
    DR = topologyRecorder(),
    TVC = TopologyViewerComponent(transparency = (255,255,255), showGrid = False, position=(0,0)),
    linkages = {
        ("SOURCE", "outbox") : ("DR", "inbox"),
        ("DR", "outbox") : ("TVC", "inbox"),
        ("NEXT", "outbox") : ("DR", "control"),
        ("PREVIOUS", "outbox") : ("DR", "control"),
    }
)

# NonInteractiveDataTester.run()
# NonInteractiveTopologyTester.run()
InteractiveTester.run()

