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
ADD NODE Source#clicknext "Click Next" randompos outbox
ADD LINK Source Source#default
ADD LINK Source Source#clicknext
ADD NODE Sink Sink randompos component
ADD NODE Sink#default default randompos inbox
ADD NODE Sink#clicknext ClickNext randompos outbox
ADD LINK Sink Sink#default
ADD LINK Sink Sink#clicknext
ADD LINK Source#clicknext Sink#default
ADD LINK Sink#clicknext Source#default
"""])

Backplane("VIS").activate()
Backplane("UI_Events").activate()

X = Pipeline(
    SubscribeTo("VIS"),
#    ConsoleEchoer(forwarder=True),
    chunks_to_lines(),
    lines_to_tokenlists(),
    AxonVisualiser(position=(0,0)),
    ConsoleEchoer(forwarder=True),
    PublishTo("UI_Events"),
).activate()

Y = Pipeline(
    example,
#    ConsoleEchoer(forwarder=True),
    PublishTo("VIS"),
).activate()


class AssetManager(Axon.Component.component):
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
                    self.send("ADD NODE "+nid+" "+nlabel+" randompos component\n","outbox")
                    self.send("ADD NODE "+nid+"#default default randompos inbox\n","outbox")
                    self.send('ADD NODE '+nid+'#clicknext "Click Next" randompos outbox\n',"outbox")
                    self.send("ADD LINK "+nid+" "+nid+"#default\n","outbox")
                    self.send("ADD LINK "+nid+" "+nid+"#clicknext\n","outbox")
            yield 1
             
F = Pipeline(
             Button(caption="ADD ASSET",
                    size=(63,32),
                    position=(800, 20),
                    msg='add').activate(),
             AssetManager(),
             ConsoleEchoer(forwarder=True),
             PublishTo("VIS"),
).activate()

class Magic(Axon.Component.component):
    def main(self):
        selected = None
        mode = None
        source = None
        sink = None
        while 1:
            yield 1
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                if event[0] == "SELECT":
                    if event[1] == "NODE":
                        selected = event[2]
                        print "CLICKED: ", selected
                        if mode == "LINK":  
                            sink = selected
                            try:
                                if "#" not in sink:
                                    sink = selected+"#default"
                                self.send("ADD LINK "+source+" "+sink+"\n","outbox")
                            except TypeError:
                                pass
                            source = None
                            priorselected = None
                            selected = None
                            
                if event[0] == "MAKELINKTO":
                   mode = "LINK"
                   print "MAKING LINK from", selected
                   source = selected
                   try:
                       if '#' not in source:
                            print "Hmm, we don't allow you to make links from nodes without going grrrrr"
                            mode = None
                   except TypeError,e:
                           mode = None
                           source = None
                           sink = None
                           priorselected = None
                           selected = None
#                       else:
#                           print "Gingle?",e

F_ = Pipeline(
             Button(caption="LINK",
                    size=(64,32),
                    position=(800, 53),
                    msg=("MAKELINKTO",) ).activate(),
             ConsoleEchoer(forwarder=True),
             PublishTo("UI_Events"),
).activate()

Pipeline( 
    SubscribeTo("UI_Events"),
#    ConsoleEchoer(forwarder=True),
    Magic(),
    ConsoleEchoer(forwarder=True),
    PublishTo("VIS"),
).activate()

Z = Pipeline(
    ConsoleReader(),
    PublishTo("VIS"),
).run()
