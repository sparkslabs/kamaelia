#!/usr/bin/python

import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.Apps.Europython09.BB.Exceptions import GotShutdownMessage

class RequestResponseComponent(Axon.Component.component):
    def waitMsg(self):
        def _waitMsg(self):
            while (not self.dataReady("inbox")) and (not self.dataReady("control")):
                self.pause()
                yield 1
        return WaitComplete( _waitMsg(self) ) 

    def checkControl(self):
        if self.dataReady("control"):
            raise GotShutdownMessage()

    def getMsg(self):
        if self.dataReady("control"):
            raise GotShutdownMessage()
        return self.recv("inbox")

    def netPrint(self, arg):
        self.send(arg + "\r\n", "outbox")

    def main(self):
        self.send("no protocol attached\r\n\r\n")
        self.send( Axon.Ipc.producerFinished(), "signal")
        yield 1

