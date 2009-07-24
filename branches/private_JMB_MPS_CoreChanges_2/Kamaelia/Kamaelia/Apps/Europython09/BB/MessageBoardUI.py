#!/usr/bin/python

from Axon.Ipc import WaitComplete
from Kamaelia.Apps.Europython09.BB.Support import Folder
from Kamaelia.Apps.Europython09.BB.Exceptions import GotShutdownMessage
from Kamaelia.Apps.Europython09.BB.RequestResponseComponent import RequestResponseComponent

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
