#!/usr/bin/python

import cjson
import socket
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Seq import Seq

class GotShutdownMessage(Exception):
    pass

class RequestResponseComponent(Axon.Component.component):
    def waitMsg(self):
        while (not self.dataReady("inbox")) and (not self.dataReady("control")):
            self.pause()
            yield 1

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

class Authenticator(RequestResponseComponent):
    State = {}
    def main(self):
        loggedin = False
        try:
            self.netPrint("")
            while not loggedin:
                self.send("login: ", "outbox")
                yield WaitComplete( self.waitMsg() )
                username = self.getMsg()[:-2] # strip \r\n

                self.send("password: ", "outbox")
                yield WaitComplete( self.waitMsg() )
                password= self.getMsg()[:-2] # strip \r\n

                self.netPrint("")
                if users.get(username.lower(), None) == password:
                    self.netPrint("Login Successful")
                    loggedin = True
                else:
                    self.netPrint("Login Failed!")

        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")

        if loggedin:
            self.State["remoteuser"] = username


def CompositeBulletinBoardProtocol(**argd):
    ConnectionInfo = {}
    ConnectionInfo.update(argd)
    return Seq(
                  Authenticator(State = ConnectionInfo),
              )

def readUsers():
    f = open("users.passwd")
    users = f.read()
    f.close()
    users = cjson.decode(users)
    return users


users = readUsers()

ServerCore(protocol=CompositeBulletinBoardProtocol,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=1600).run()

