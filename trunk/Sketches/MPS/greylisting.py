#!/usr/bin/python

import Axon
import socket
import time
import pprint
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer

from Kamaelia.Internet.TCPClient import TCPClient

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
    def handleDisconnect(self): yield 1

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
        yield WaitComplete(self.handleDisconnect())

class ConcreteMailHandler(MailHandler):
    Inboxes = {
        "inbox" : "Data from the client connecting to the server comes in here",
        "control" : "Shutdown & control messages regarding client side socket handling",
        "tcp_inbox" : "This is where we get respones from the real SMTP server",
        "tcp_control" : "This is where we get shutdown information from the real SMTP server",
    }
    Outboxes = {
        "outbox" : "Data sent here goes back the the client connecting to the server",
        "signal" : "Shutdown & control messages regarding client side socket handling",
        "tcp_outbox" : "Data sent here is sent to the real SMTP server",
        "tcp_signal" : "We send messages here to shutdown the connection to the real SMTP connection",
    }
    peer = "*** UNDEFINED ***"
    peerport = "*** UNDEFINED ***"
    local = "*** UNDEFINED ***"
    localport = "*** UNDEFINED ***"
    servername = "Testing.server.local"
    serverid = "MPS SMTP 1.0"
    smtp_ip = "192.168.2.9"
    smtp_port = 25

    def connectToRealSMTPServer(self):
        self.TCPClient = TCPClient(self.smtp_ip, self.smtp_port).activate()
        self.link((self, "tcp_outbox"), (self.TCPClient, "inbox"))
        self.link((self, "tcp_signal"), (self.TCPClient, "control"))
        self.link((self.TCPClient, "outbox"), (self,"tcp_inbox"))
        self.link((self.TCPClient, "signal"), (self,"tcp_control"))

    def __init__(self, **argv):
        super(ConcreteMailHandler, self).__init__(**argv)
        self.recipients = []
        self.sender = None
        self.seenHelo = False
        self.seenMail = False
        self.seenRcpt = False
        self.acceptingMail = False

    def error(self, message):  # Yes, we're quite nasty - we break the connection if the person makes a mistake
        self.netPrint(message) # This violate's Postel's law. The idea is to catch out broken spam mailers...
        self.breakConnection = True

    def RelayError(self):
        self.error("550 relay not permitted")

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

        self.netPrint("250 ACCEPTED")
        self.recipients.append(command[2])
        self.seenRcpt = True

    def handleData(self, command):
        if not self.seenRcpt:
            self.error("503 valid RCPT command must precede DATA")
            return

        if self.shouldWeAcceptMail():
            self.acceptMail()
        else:
            self.deferMail()

    def shouldWeAcceptMail(self):
        return False # Default policy - don't accept any email

    def deferMail(self):
        self.netPrint("451 4.7.1 Please try again later")
        self.breakConnection = True

    def acceptMail(self):
        self.gettingdata = True
        self.acceptingMail = True

    def handleQuit(self,command):
        self.netPrint("221 %s closing connection" % (self.servername,))
        self.breakConnection = True

    def getline_fromsmtpserver(self):
        while not self.dataReady("tcp_inbox"):
            self.pause()
            yield 1
        self.smtp_line = self.recv("tcp_inbox")

    def handleDisconnect(self):
        if not self.acceptingMail: return
        self.connectToRealSMTPServer()
        yield 1
        sentDataLine = False
        for line in self.inbox_log:
            if not sentDataLine: # wait for a response from the server before sending next line
                yield WaitComplete(self.getline_fromsmtpserver())

            self.send(line, "tcp_outbox")
            if not sentDataLine:
                sentDataLine = (line == "DATA\r\n")

class GreyListingPolicy(ConcreteMailHandler):
    allowed_senders = [] # List of senders
    allowed_sender_nets = [] # Only class A,B, C network style networks at present (ie IP prefixes)
    allowed_domains = [ ] # list of IPs

    def sentFromAllowedIPAddress(self):
        if self.peer in self.allowed_senders:
            print "ALLOWED TO SEND, since is an allowed_sender"
            return True
        return False

    def sentFromAllowedNetwork(self):
        for network_prefix in self.allowed_sender_nets:
            if self.peer[:len(network_prefix)] == network_prefix:
                print "ALLOWED TO SEND, since is in an approved network"
                return True
        return False

    def sentToADomainWeForwardFor(self):
        for recipient in self.recipients:
            recipient = recipient.replace("<", "")
            recipient = recipient.replace(">", "")
            try:
                domain = recipient[recipient.find("@")+1:]
                if not (domain in self.allowed_domains):
                    print "NOT ALLOWED TO SEND - recipient not in allowed_domains", recipient, domain, self.allowed_domains
                    return False
            except:
                print "NOT ALLOWED TO SEND - bad recipient", recipient
                raise
                return False # don't care why it fails if it fails
        return True # Only reach here if all domains in allowed_domains

    def shouldWeAcceptMail(self):
        print "Now we would decide whether to recieve based on"
        print "Claimed remote name", self.remotename
        print "Actual remote IP", self.peer
        print "The claimed sender email", self.sender
        print "The named recipients", ", ".join(self.recipients)
        print "We do one of these:"
        print "    - self.deferMail()"
        print "    - self.acceptMail()"
        pprint.pprint(self.inbox_log)

        if self.sentFromAllowedIPAddress():  return True # Allowed hosts can always send to anywhere through us
        if self.sentFromAllowedNetwork():    return True # People on truste networks can always do the same
        if self.sentToADomainWeForwardFor(): return True # Anyone can always send to hosts we own

        print "NOT ALLOWED TO SEND, no valid forwarding"
        return False

class GreylistServer(MoreComplexServer):
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8026
    class protocol(GreyListingPolicy):
        allowed_senders = ["127.0.0.1"]
        allowed_sender_nets = ["192.168.2"] # Yes, only class C network style
        allowed_domains = [ "private.thwackety.com",
                            "thwackety.com",
                            "thwackety.net",
                            "yeoldeclue.com",
                            "michaelsparks.info",
                            "lansdowneresidents.org",
                            "polinasparks.com",
                            "pixienest.com",
                            "owiki.org",
                            "cerenity.org"]

GreylistServer().run()

