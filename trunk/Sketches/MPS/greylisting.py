#!/usr/bin/python

import Axon
import socket
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer
from Kamaelia.Chassis.Graphline import Graphline
import pprint
import time
#        for line in self.Inbox("inbox"):
class MailHandler(Axon.Component.component):
    def __init__(self,**argd):
        super(MailHandler, self).__init__(**argd)
        self.inbox_log = []

    def logging_recv_connection(self):
        self.line = self.recv("inbox")
        self.inbox_log.append(self.line)

    def getline(self):
        while not self.anyReady():
            self.pause()
            yield 1
        self.logging_recv_connection()

    def handleCommand(self,command):
        print "command", repr(command)
        if command[0] == "AUTH":
            self.handleAuth(command)
        if command[0] == "HELO": self.handleHelo(command)
        if command[0] == "EHLO": self.handleEhlo(command)
        if command[0] == "MAIL": self.handleMail(command)
        if command[0] == "RCPT": self.handleRcpt(command)
        if command[0] == "DATA": self.handleData(command)
        if command[0] == "QUIT": self.handleQuit(command)
        if command[0] == "RSET": self.handleRset(command)
        if command[0] == "HELP": self.handleHelp(command)

    def netPrint(self, *args):
        for i in args:
            self.send(i+"\r\n", "outbox")

    def handleConnect(self): pass
    def handleAuth(self,command): pass
    def handleHelo(self,command): pass
    def handleEhlo(self,command): pass
    def handleMail(self,command): pass
    def handleRcpt(self,command): pass
    def handleData(self,command): pass
    def handleQuit(self,command): pass
    def handleRset(self,command): pass
    def handleHelp(self,command): pass
    def handleDisconnect(self): pass

    def main(self):
        self.handleConnect()
        self.gettingdata = False
        self.breakConnection = False

        while (not self.gettingdata) and (not self.breakConnection):
            yield WaitComplete(self.getline())
            command = self.line.split()
            self.handleCommand(command)

        if (not self.breakConnection):
            EndOfMessage = False
            self.netPrint('354 Enter message, ending with "." on a line by itself')
            while not EndOfMessage:
                yield WaitComplete(self.getline())
                if self.line == ".\r\n": EndOfMessage = True
            self.netPrint("250 OK id-deferred")

        self.send(producerFinished(),"signal")
        self.handleDisconnect()

class ConcreteMailHandler(MailHandler):
    peer = "*** UNDEFINED ***"
    peerport = "*** UNDEFINED ***"
    local = "*** UNDEFINED ***"
    localport = "*** UNDEFINED ***"
    servername = "Testing.server.local"
    serverid = "MPS SMTP 1.0"
    def __init__(self, **argv):
        super(ConcreteMailHandler, self).__init__(**argv)
        self.recipients = []
        self.sender = None
        self.seenHelo = False
        self.seenMail = False
        self.seenRcpt = False

    def error(self, message):  # Yes, we're quite nasty - we break the connection if the person makes a mistake
        self.netPrint(message) # This violate's Postel's law. The idea is to catch out broken spam mailers...
        self.breakConnection = True

    def RelayError(self):
        self.error("550 relay not permitted")

    def handleDisconnect(self):
        pprint.pprint( self.inbox_log )

    def handleConnect(self):
        self.netPrint("220 %s ESMTP %s %s" %
                      (self.servername,
                       self.serverid,
                       time.ctime())
        )

    def handleHelo(self,command):
        self.actual_remote_ip = "192.168.2.5"
        if len(command) != 2:
            self.error("501 Syntactically invalid HELO argument(s)")
            return

        self.remotename = command[1]
        self.netPrint("250 %s Hello %s %s" %
                      (self.servername, self.remotename,self.peer)
                      )
        self.inbox_log = self.inbox_log[-1:] # Remove all previous items
        self.seenHelo = True

    def handleMail(self,command):
        if len(command) < 2:
            self.error("500 unrecognised command")
            return

        if len(command) == 2:
            self.error("501 MAIL must have an address operand")
            return

        if command[1] != "FROM:":
            self.error("500 unrecognised command")
            return

        if not self.seenHelo:
            self.netPrint("503 5.5.2 Send hello first")
            return

        if self.seenMail:
            self.netPrint("503 sender already given")
            return

        self.sender = command[2]
        self.netPrint("250 OK")
        self.seenMail = True

    def handleRcpt(self,command):
        if len(command) < 2:  # Protocol syntax error
            self.error("500 unrecognised command")
            return
        if len(command) == 2:  # Protocol syntax error
            self.error("501 RCPT must have an address operand")
            return

        if command[1] != "TO:":  # Protocol syntax error
            self.error("500 unrecognised command")
            return

        if not self.seenMail:  # Protocol usage error
            self.error("503 sender not yet given")
            return

        recipient = command[2]
        self.netPrint("250 ACCEPTED")
        self.recipients.append(recipient)
        self.seenRcpt = True

    def handleData(self, command):
        if not self.seenRcpt:
            self.error("503 valid RCPT command must precede DATA")
            return

        print "Now we would decide whether to recieve based on"
        print "Claimed remote name", self.remotename
        print "Actual remote IP", self.peer
        print "The claimed sender email", self.sender
        print "The named recipients", ", ".join(self.recipients)
        print "We do one of these:"
        print "    - self.deferMail()"
        self.acceptMail()

    def deferMail(self, command):
        self.netPrint("451 4.7.1 Please try again later")
        self.breakConnection = True

    def acceptMail(self):
        self.gettingdata = True

    def handleQuit(self,command):
        self.netPrint("221 %s closing connection" % (self.servername,))
        self.breakConnection = True

class GreylistServer(MoreComplexServer):
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8026
    protocol = ConcreteMailHandler

GreylistServer().run()
