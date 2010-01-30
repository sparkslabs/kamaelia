#!/usr/bin/python

import socket
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.Chassis.ConnectedServer import ServerCore

class GotShutdownMessage(Exception):
    pass

class RequestResponseComponent(Axon.Component.component):
    def waitMsg(self):
        while (not self.dataReady("inbox")) and (not self.dataReady("control")):
            self.pause()
            yield 1

    def getMsg(self):
        if self.dataReady("control"):
            raise GotShutdownMessage()
        return self.recv("inbox")

    def main(self):
        try:
            while 1:
                self.send("login: ", "outbox")
                yield WaitComplete( self.waitMsg() )
                username = self.getMsg()

                self.send("password: ", "outbox")
                yield WaitComplete( self.waitMsg() )
                password= self.getMsg()

                print
                print repr(username), repr(password)
                self.pause()
                yield 1
        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")
        self.send( Axon.Ipc.producerFinished(), "signal")

ServerCore(protocol=RequestResponseComponent,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=1600).run()
