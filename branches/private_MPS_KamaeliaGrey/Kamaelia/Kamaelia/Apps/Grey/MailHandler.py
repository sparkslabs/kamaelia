
#
# This is primarily used by Kamaelia.Apps.ConcreteMailHandler
# It does form the basis of most things that need to handle basic SMTP type things
#
"""\
=========================
Abstract SMTP Mailer Core
=========================

This component effectively forms the skeleton of an SMTP server. It expects
an SMTP client to connect and send various SMTP requests to it. This basic
SMTP Mailer Core however, does not actually do anything in response to any
of the SMTP commands it expects.

Each SMTP command is actually given a dummy callback which more customised
SMTP protocol handlers are expected to override. Beyond this, this component
is expected to be used as a protocol handler for ServerCore.

Fundamentally, this component handles the command/response structure of SMTP
fairly directly, but expects the brains of the protocol to be implemented by
a more intelligent subclass.

Example Usage
-------------

Whilst this will work to a minimal extent::

    ServerCore(protocol=MailHandler, port=1025)

This will not actually form a very interesting SMTP, nor SMTP compliant,
server since whilst it will tell you commands it doesn't understand, it will
not do anything interesting.

You are as noted expected to subclass MailHandler. For a better example
of how to subclass MailHandler you are suggested to look at
Kamaelia.Apps.ConcreteMailHandler.ConcreteMailHandler

Note
----

This component is not complete - you are expected to subclass it to finish
it off as you need. Specifically it does not implement the following -
 - It does not enforce "this command followed by that command"
 - It does not actually do anything with any DATA a client sends you
 - It neither performs local mail delivery nor proxying - you'd need to implement this yourself.


How does it work?
-----------------

The component is expected to be connected to a client TCP connection by
ServerCore, such that messages from the network arrive on inbox "inbox", and
outgoing messages get sent to outbox "outbox"

The component will terminate if any of these is true:
 - The client breaks the connection
 - One of the methods sets self.breakConnection to True.
 - If a "socketShutdown" message arrives on inbox "control"

The main() method divides the connection into effectively two main states:
 - accepting random commands prior to getting a DATA command
 - accepting the email during a DATA command

SMTP commands are specifically dispatched to a particular handler for that
command. In this component none of the handlers do anything interesting.

Configuration
-------------

The abstract mailer supports some basic config settings:
 - logfile - path/filename where requests should get logged
 - debuglogfile - path/filename to where the debug log file should do.

Methods you are expected to override
------------------------------------

Whilst you are probably better off subclassing ConcreteMailHandler, you will
probably need to override the following methods in a subclass if you
subclass MailHandler directly.

 - handleConnect(self)
 - handleHelo(self,command)
 - handleEhlo(self,command)
 - handleMail(self,command)
 - handleRcpt(self,command)
 - handleData(self,command)
 - handleQuit(self,command)
 - handleRset(self,command)
 - handleNoop(self,command)
 - handleVrfy(self,command)
 - handleHelp(self,command)
 - logResult(self)
 - handleDisconnect(self)

"""

import Axon
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.IPC import socketShutdown

class MailHandler(Axon.Component.component):
    logfile = "greylist.log"
    debuglogfile = "greylist-debug.log"
    def __init__(self,**argd):
        super(MailHandler, self).__init__(**argd)
        self.inbox_log = []
        self.line = None

    def logging_recv_connection(self):
        self.line = self.recv("inbox")
        self.inbox_log.append(self.line)

    def getline(self):
        control_message = ""
        while 1:
            while not self.anyReady():
                self.pause();  # print "PAUSING", repr(self.inbox_log), repr(self.line)
                yield 1
            while self.dataReady("control"):
                control_message = self.recv("control")
                if isinstance(control_message, socketShutdown):
                    self.client_connected = False
            if self.dataReady("inbox"):
                self.logging_recv_connection()
                return
            else:
                if not self.client_connected :
                    self.breakConnection = True
                    return
            yield 1

    def handleCommand(self,command):
        if len(command) < 1:
            self.netPrint("500 Sorry we don't like broken mailers")
            self.breakConnection = True
            return
        if command[0] == "HELO": return self.handleHelo(command) # RFC 2821 4.5.1 required
        if command[0] == "EHLO": return self.handleEhlo(command) # RFC 2821 4.5.1 required
        if command[0] == "MAIL": return self.handleMail(command) # RFC 2821 4.5.1 required
        if command[0] == "RCPT": return self.handleRcpt(command) # RFC 2821 4.5.1 required
        if command[0] == "DATA": return self.handleData(command) # RFC 2821 4.5.1 required
        if command[0] == "QUIT": return self.handleQuit(command) # RFC 2821 4.5.1 required
        if command[0] == "RSET": return self.handleRset(command) # RFC 2821 4.5.1 required
        if command[0] == "NOOP": return self.handleNoop(command) # RFC 2821 4.5.1 required
        if command[0] == "VRFY": return self.handleVrfy(command) # RFC 2821 4.5.1 required
        if command[0] == "HELP": return self.handleHelp(command)
        self.netPrint("500 Sorry we don't like broken mailers")
        self.breakConnection = True

    def noteToLog(self, line):
        try:
            x = open(self.logfile,"a")
        except IOError:
            x = open(self.logfile,"w")
        x.write(line+"\n")
        x.flush()
        x.close()

    def noteToDebugLog(self, line):
        try:
            x = open(self.debuglogfile,"a")
        except IOError:
            x = open(self.debuglogfile,"w")
        x.write(line+"\n")
        x.flush()
        x.close()

    def netPrint(self, *args):
        for i in args:
            self.noteToDebugLog(i)
            self.send(i+"\r\n", "outbox")

    def handleConnect(self): pass
    def handleHelo(self,command): pass
    def handleEhlo(self,command): pass
    def handleMail(self,command): pass
    def handleRcpt(self,command): pass
    def handleData(self,command): pass
    def handleQuit(self,command): pass
    def handleRset(self,command): pass
    def handleNoop(self,command): pass
    def handleVrfy(self,command): pass
    def handleHelp(self,command): pass
    def logResult(self): pass
    def handleDisconnect(self): yield 1

    def lastline(self):
        if self.line == ".\r\n":
            return True
        if len(self.line) >=5:
            if self.line[-5:] == "\r\n.\r\n":
                return True
        if len(self.line) >=5:
            if self.line[-5:] == "\r\n.\r\n":
                return True
        if len(self.line) >=4:
            if self.line[-4:] == "\n.\r\n":
                return True
        return False

    def main(self):
        brokenClient = False
        self.handleConnect()
        self.gettingdata = False
        self.client_connected = True
        self.breakConnection = False

        while (not self.gettingdata) and (not self.breakConnection):
            yield WaitComplete(self.getline(), tag="_getline1")
            try:
                command = self.line.split()
            except AttributeError:
                brokenClient = True
                break
            self.handleCommand(command)
        if not brokenClient:
            if (not self.breakConnection):
                EndOfMessage = False
                self.netPrint('354 Enter message, ending with "." on a line by itself')
                while not EndOfMessage:
                    yield WaitComplete(self.getline(), tag="getline2")
                    if self.lastline():
                        EndOfMessage = True
                self.netPrint("250 OK id-deferred")

        self.send(producerFinished(),"signal")
        if not brokenClient:
            yield WaitComplete(self.handleDisconnect(),tag="_handleDisconnect")
        self.logResult()
