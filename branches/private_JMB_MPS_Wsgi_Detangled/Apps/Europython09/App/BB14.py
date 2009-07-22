#!/usr/bin/python

import os
import cjson
import socket
import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Seq import Seq

class GotShutdownMessage(Exception):
    pass

class Folder(object):
    def __init__(self, folder="messages"):
        super(Folder, self).__init__()
        self.folder = folder
        try:
            f = open(self.folder + "/.meta")
            raw_meta = f.read()
            f.close()
            meta = cjson.decode(raw_meta)
        except IOError:
            meta = {"maxid": 0}
        self.meta = meta

    def getMessage(self, messageid):
        try:
            f = open(self.folder + "/" + str(messageid))
            message = f.read()
            f.close()
            message = cjson.decode(message)
            return message
        except IOError:
            return None

    def getMessages(self):
        messages = []
        for i in os.listdir(self.folder):
            if i[:1] == ".":
                continue
            messages.append(self.getMessage(i))
        return messages

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

class Authenticator(RequestResponseComponent):
    State = {}
    def main(self):
        loggedin = False
        try:
            self.netPrint("")
            while not loggedin:
                self.send("login: ", "outbox")
                yield self.waitMsg()
                username = self.getMsg()[:-2] # strip \r\n

                self.send("password: ", "outbox")
                yield self.waitMsg()
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

class UserRetriever(RequestResponseComponent):
    State = {}
    def main(self):
        self.netPrint("")
        self.netPrint("Retrieving user data...")
        self.netPrint("")
        yield 1

class StateSaverLogout(RequestResponseComponent):
    State = {}
    def main(self):
        self.netPrint("")
        self.netPrint("Saving user data...")
        self.netPrint("")
        self.netPrint("Goodbye!")
        self.netPrint("")
        yield 1

class MessageBoardUI(RequestResponseComponent):
    State = {}
    def doMainHelp(self):
        self.netPrint("<return> - browse messages")
        self.netPrint("h - help")
        self.netPrint("q - quit")

    def getUnreadMessages(self, user):
        X = Folder()
        return X.getMessages()

    def displayMessage(self, message):
        self.netPrint("")
        for key in ["message", "date", "from", "to", "subject",]:
            self.netPrint("%s: %s" % (key, message[key] ) )

        if len(message["reply-to"]) > 0:
            self.netPrint("In-Reply-To: "+(", ".join(message["reply-to"]) ) )
        self.netPrint("")
        self.netPrint(message["__body__"])

    def doMessagesHelp(self):
        self.netPrint("<return> - next message (exit if on last message)")
        self.netPrint("r - Reply (to be implemented)")
        self.netPrint("d - Delete message (to be implemented)")
        self.netPrint("h - Help")
        self.netPrint("x - eXit to main menu")

    def doMessagesMenu(self, user):
        try:
            messages = self.getUnreadMessages(user)
            while len(messages) > 0:
                self.netPrint("")
                self.netPrint("You have "+str(len(messages))+" message(s) waiting")

                self.send("messages> ", "outbox")
                yield self.waitMsg()
                command = self.getMsg()[:-2]

                if command == "":
                    message = messages.pop(0)
                    self.displayMessage(message)

                if command == "x":
                    break

                if command == "h":
                       self.doMessagesHelp()
        except GotShutdownMessage:
            pass # Expect the "caller" to check for control as well

    def main(self):
        user = self.State.get("remoteuser", "anonymous")
        try:
            self.netPrint("")
            self.netPrint("Hello, "+user)
            while 1:
                self.send("main> ", "outbox")
                yield self.waitMsg()
                command = self.getMsg()[:-2]
                if command == "h":
                    self.doMainHelp()
                if command == "q":
                    break
                if command == "":
                    yield WaitComplete(self.doMessagesMenu(user))
                    self.checkControl()
        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")
        yield 1

def CompositeBulletinBoardProtocol(**argd):
    ConnectionInfo = {}
    ConnectionInfo.update(argd)
    return Seq(
                  Authenticator(State = ConnectionInfo),
                  UserRetriever(State = ConnectionInfo),
                  MessageBoardUI(State = ConnectionInfo),
                  StateSaverLogout(State = ConnectionInfo),
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


