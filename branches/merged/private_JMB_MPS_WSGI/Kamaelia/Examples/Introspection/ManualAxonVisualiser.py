#!/usr/bin/python


import Axon
from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiser
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Chassis.Pipeline import Pipeline

class Source(Axon.Component.component):
    "A simple data source"
    def __init__(self, data=None):
        super(Source, self).__init__()
        if data == None: data = []
        self.data = data

    def main(self):
        for item in iter(self.data):
            self.send(item, "outbox")
            yield 1

Pipeline(
        ConsoleReader(),
        Source(["""\
ADD NODE Source Source randompos component
ADD NODE Source#inbox inbox randompos inbox
ADD NODE Source#outbox outbox randompos outbox
ADD LINK Source Source#inbox
ADD LINK Source Source#outbox
ADD NODE Sink Sink randompos component
ADD NODE Sink#inbox inbox randompos inbox
ADD NODE Sink#outbox outbox randompos outbox
ADD LINK Sink Sink#inbox
ADD LINK Sink Sink#outbox
ADD LINK Source#outbox Sink#inbox
ADD LINK Sink#outbox Source#inbox
"""]),
        chunks_to_lines(),
        lines_to_tokenlists(),
        AxonVisualiser(),
        ConsoleEchoer(),
).run()
