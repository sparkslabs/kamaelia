#!/usr/bin/python


import Axon
from Creator.AxonVisualiserServer import AxonVisualiser
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Chassis.Pipeline import Pipeline

import time
#class Source(Axon.ThreadedComponent.threadedcomponent):
class Source(Axon.Component.component):
    "A simple data source"
    def __init__(self, data=None):
        super(Source, self).__init__()
        if data == None: data = []
        self.data = data

    def main(self):
        yield 1
        for item in iter(self.data):
            self.send(item, "outbox")
            yield 1
        self.pause()

from Kamaelia.UI.Pygame.Button import Button


from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo

example = Source(["""\
ADD NODE Source Source randompos component
ADD NODE Source#default default randompos inbox
ADD NODE Source#next Next randompos outbox
ADD LINK Source Source#default
ADD LINK Source Source#next
ADD NODE Sink Sink randompos component
ADD NODE Sink#default default randompos inbox
ADD NODE Sink#next Next randompos outbox
ADD LINK Sink Sink#default
ADD LINK Sink Sink#next
ADD LINK Source#next Sink#default
ADD LINK Sink#next Source#default
"""])

class AssetManager(Axon.Component.component):
    def out(self, message):
        print message
        self.send(message, "outbox")

    def main(self):
        baseid = "asset"
        count = 0
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data == "add":
                    count += 1
                    nid = baseid + str(count)
                    nlabel = nid + ".label"
                    self.out("ADD NODE "+nid+" "+nlabel+" randompos component\n")
                    self.out("ADD NODE "+nid+"#default default randompos inbox\n")
                    self.out('ADD NODE '+nid+'#next Next randompos outbox\n')
                    self.out("ADD LINK "+nid+" "+nid+"#default\n")
                    self.out("ADD LINK "+nid+" "+nid+"#next\n")
            yield 1
             

class Magic(Axon.Component.component):
    Inboxes = {
       "nodeselect" : "expect to get node notifications here",
       "makelink": "Expect to be told to make links here",
       "inbox" : "",
       "control" : "",
    }
    Outboxes = {
       "outbox" : "",
       "signal" : "",
    }
    def main(self):
        selected = None
        mode = None
        source = None
        sink = None
        while 1:
            yield 1
            while self.dataReady("nodeselect"):
                event = self.recv("nodeselect")
                selected = event[2]
                print "CLICKED: ", selected
                if mode == "LINK":
                    print "Make link?", source, sink
                    sink = selected
                    print "Make link?", source, sink
                    try:
                        if "#" not in sink:
                            sink = selected+"#default"
                        self.send("ADD LINK "+source+" "+sink+"\n","outbox")
                    except TypeError:
                        pass
                    source, sink, selected, mode = None, None, None, None
                    selected = None

            while self.dataReady("makelink"):
                print "BONGLE"
                event = self.recv("makelink")
                            
                if event[0] == "MAKELINKTO":
                   mode = "LINK"
                   print "MAKING LINK from", selected
                   source = selected
                   try:
                       if '#' not in source:
                            source = source+"#next"
                   except TypeError,e:
                           mode = None
                           source = None
                           sink = None
                           priorselected = None
                           selected = None

Backplane("VIS").activate()
Backplane("UI_Events").activate()

X = Pipeline(
    SubscribeTo("VIS"),
    chunks_to_lines(),
    lines_to_tokenlists(),
    AxonVisualiser(position=(0,0)),
    ConsoleEchoer(forwarder=True),
    PublishTo("UI_Events"),
).activate()


Graphline(
    EXAMPLE = example,
    ADDASSET =  Button(caption="ADD ASSET", position=(800, 20), msg='add'),
    LINKER = Button(caption="LINK", position=(800, 53), msg=("MAKELINKTO",) ),
    
    EVENTS = SubscribeTo("UI_Events"),
    MAGIC = Magic(),
    ASSETS = AssetManager(),
    CONTROL = PublishTo("VIS"),
    linkages = {
        ("EVENTS","outbox") : ("MAGIC","nodeselect"),
        ("LINKER","outbox") : ("MAGIC","makelink"),
        ("ADDASSET","outbox") : ("ASSETS","inbox"),
        ("MAGIC","outbox")   : ("CONTROL","inbox"),
        ("ASSETS","outbox")  : ("CONTROL","inbox"),
        ("EXAMPLE","outbox") : ("CONTROL","inbox"), # This can be removed at a later date
    }
).activate()

Z = Pipeline(
    ConsoleReader(),
    PublishTo("VIS"),
).run()
