"""\
==================
Concrete Mail Core
==================

This code enforces the basic statemachine that SMTP expects, switching
between the various commands and finally results in forwarding on the SMTP
command to the appropriate SMTP server. By itself, this can be used as a
simple SMTP Proxy server.

This class is a subclass of MailHandler, and as such largely consists of
methods overriding methods from MailHandler which are designed to be
overridden.

Furthermore, it expects to forward any mail it accepts to another SMTP mail
server, as transparently as possible. Thus this concrete mail core
effectively forms the core of an SMTP proxy.

Note
----

As it stands however, by default this mail proxy will *not* forward any mails
to the internal server. In order to change this, you would need to subclass
this server and replace the method "shouldWeAcceptMail" since that defaults
to returning False

Example Usage
-------------

As noted, you are not expected to use this ConcreteMailHandler directly, but
if you did, you would use it like this::
    
    ServerCore(protocol=ConcreteMailHandler, port=1025)

At minimum, you would need to do this::
    class SpamMeHandler(ConcreteMailHandler):
        def shouldWeAcceptMail(self):
            return True
                    
    ServerCore(protocol=SpamMeHandler, port=1025)

You could alternatively do this::
    class SpamMeMailServer(ServerCore):
        class protcol(ConcreteMailHandler):
            def shouldWeAcceptMail(self):
                 return True
                 
    ServerCore(port=1025)

How does it work?
-----------------

As noted this overrides all the methods relating to handling SMTP commands,
and enforces the state machine that SMTP requires. It's particularly strict
about this, in breach of Postel's law for two reasons - 

 - It helps eradicate spam
 - because most spam systems are generally lax these days and most non-spam systems are generally strict

It was also primarily written in the context of a greylisting server.

Some core values it tracks with regard to a mail - 
 - a list of recipients
 - the (claimed) sender
 - the (claimed) remote/client name
 - the actual client & local port/ip addresses

Once the client has finished sending the data for an email, the proxy
forwards the mail to the local real SMTP server. Fundamentally this happens
by making a connection to the real server using the TCPClient component, and
then replaying all the lines the original server sent us to the local
server.

(ie an inbox_log is built up with all data recieved from inbox "inbox" and
then the contents of this are replayed when being sent to the local (real)
SMTP mail server)

Configuration
-------------

This class provides a large number of configuration options. You can either
change this through subclassing or by providing as named arguments to the
__init__ function. The options you have -

 - servername - The name this server will choose to use to identify itself
 - serverid - The string this server will use to identify itself (in terms of software in use)
 - smtp_ip - the ip address of the server you're proxying for/to
 - smtp_port - this is the port the server you're proxying for/to is listening on

The following attributes get set when a client connects -

 - peer - the IP address of the client
 - peerport - the port which the peer is connected from
 - local - the IP address the client has connected to
 - localport - the port which they're connected to

"""

import time
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Apps.Grey.MailHandler import MailHandler

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
        self.remotename = ""
        self.seenHelo = False
        self.seenMail = False
        self.seenRcpt = False
        self.acceptingMail = False
        self.mailStatus = ""

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

    def handleEhlo(self,command):
        self.netPrint('500 Command Not Recognised')

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

    def handleHelp(self,command):
        self.error("500 unrecognised command")

    def handleVrfy(self,command):
        self.netPrint("252 Cannot VRFY user")

    def handleRset(self,command):
        # self.seenHelo = self.seenHelo - leave unchanged (comment is to note we *have* thought about this!)
        self.recipients = []
        self.sender = None
        self.seenMail = False
        self.seenRcpt = False
        self.acceptingMail = False
        self.netPrint("250 OK")
        self.mailStatus = ""

    def handleNoop(self,command):
        self.netPrint("250 OK")

    def handleMail(self,command):
        if len(command) < 2:
            self.error("500 unrecognised command")
            return

        if len(command) == 2:
            if command[1][:5].upper() == "FROM:" and len(command[1])>5 :
                command = [ command[0], "FROM:", command[1][5:] ]
            else:
                self.error("501 MAIL must have an address operand"+repr(command))
                return

        if command[1].upper() != "FROM:":
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
            if command[1][:3].upper() == "TO:" and len(command[1])>3 :
                command = [ command[0], "TO:", command[1][3:] ]
            else:
                self.error("501 RCPT must have an address operand"+repr(command))
                return

        if command[1].upper() != "TO:":  # Protocol syntax error
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

    def handleQuit(self,command):
        self.netPrint("221 %s closing connection" % (self.servername,))
        self.breakConnection = True

    def shouldWeAcceptMail(self):
        return False # Default policy - don't accept any email

    def deferMail(self):
        self.netPrint("451 4.7.1 Please try again later")
        self.breakConnection = True
        self.mailStatus = "DEFERRED"

    def acceptMail(self):
        self.gettingdata = True
        self.acceptingMail = True
        self.mailStatus = "ACCEPTED"

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
                yield WaitComplete(self.getline_fromsmtpserver(),tag="getline_smtp")

            self.send(line, "tcp_outbox")
            yield 1
            if not sentDataLine:
                sentDataLine = (line == "DATA\r\n")
        yield 1
        self.send(producerFinished(), "tcp_signal")
