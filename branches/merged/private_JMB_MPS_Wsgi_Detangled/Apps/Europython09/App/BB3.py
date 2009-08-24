#!/usr/bin/python

import socket
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.Chassis.ConnectedServer import ServerCore

class RequestResponseComponent(Axon.Component.component):
    def waitMsg(self):
        while not self.dataReady("inbox"):
            self.pause()
            yield 1
    def getMsg(self):
        return self.recv("inbox")
    def main(self):
        while not self.dataReady("control"):
            for msg in self.Inbox("inbox"):
                self.send(msg, "outbox")
            self.pause()
            yield 1
        self.send(self.recv("control"), "signal")

ServerCore(protocol=RequestResponseComponent,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=1600).run()
