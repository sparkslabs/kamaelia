#!/usr/bin/python

import Axon
from Kamaelia.Chassis.ConnectedServer import ServerCore

class RequestResponseComponent(Axon.Component.component):
    def main(self):
        while not self.dataReady("control"):
            for msg in self.Inbox("inbox"):
                self.send(msg, "outbox")
            self.pause()
            yield 1
        self.send(self.recv("control"), "signal")

ServerCore(protocol=RequestResponseComponent,
           port=1599).run()

