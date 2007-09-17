#!/usr/bin/python

import Axon
import socket
import time
import math
import anydbm
# import pprint
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer

from Kamaelia.Internet.TCPClient import TCPClient

class MailHandler(Axon.Component.component):
    def __init__(self,**argd):
        super(MailHandler, self).__init__(**argd)
        self.inbox_log = []

    def logging_recv_connection(self):
        self.line = self.recv("inbox")
#        print repr(self.line)
        self.inbox_log.append(self.line)

    def getline(self):
        while not self.dataReady("inbox"):
#            print "WAITING getline"
            self.pause()
            yield 1
        self.logging_recv_connection()

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

    def netPrint(self, *args):
        for i in args:
            x = open("greylist.log","a")
            x.write(i+"\n")
            x.flush()
            x.close()
            print i
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

    def main(self):
        self.handleConnect()
        self.gettingdata = False
        self.breakConnection = False

        while (not self.gettingdata) and (not self.breakConnection):
            yield WaitComplete(self.getline(), tag="_getline1")
            command = self.line.split()
            self.handleCommand(command)

        if (not self.breakConnection):
            EndOfMessage = False
            self.netPrint('354 Enter message, ending with "." on a line by itself')
            while not EndOfMessage:
                yield WaitComplete(self.getline(), tag="getline2")
                if self.line == ".\r\n": EndOfMessage = True
                if len(self.line) >=5:
                    if self.line[-5:] == "\r\n.\r\n":
                        EndOfMessage = True
                if len(self.line) >=5:
                    if self.line[-5:] == "\r\n.\r\n":
                        EndOfMessage = True
                if len(self.line) >=4:
                    if self.line[-4:] == "\n.\r\n":
                        EndOfMessage = True
            self.netPrint("250 OK id-deferred")

        self.send(producerFinished(),"signal")
        yield WaitComplete(self.handleDisconnect(),tag="_handleDisconnect")
        self.logResult()

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
        # self.seenHelo = self.seenHelo - leave unchanged
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

class GreyListingPolicy(ConcreteMailHandler):
    allowed_senders = [] # List of senders
    allowed_sender_nets = [] # Only class A,B, C network style networks at present (ie IP prefixes)
    allowed_domains = [ ] # list of IPs

    def sentFromAllowedIPAddress(self):
        if self.peer in self.allowed_senders:
            # print "ALLOWED TO SEND, since is an allowed_sender"
            return True
        return False

    def sentFromAllowedNetwork(self):
        for network_prefix in self.allowed_sender_nets:
            if self.peer[:len(network_prefix)] == network_prefix:
                # print "ALLOWED TO SEND, since is in an approved network"
                return True
        return False

    def sentToADomainWeForwardFor(self):
        for recipient in self.recipients:
            recipient = recipient.replace("<", "")
            recipient = recipient.replace(">", "")
            try:
                domain = recipient[recipient.find("@")+1:]
                if not (domain in self.allowed_domains):
                    # print "NOT ALLOWED TO SEND - recipient not in allowed_domains", recipient, domain, self.allowed_domains
                    return False
            except:
                # print "NOT ALLOWED TO SEND - bad recipient", recipient
                raise
                return False # don't care why it fails if it fails
        return True # Only reach here if all domains in allowed_domains

    def isGreylisted(self, recipient):
        max_grey = 3000000
        too_soon = 180
        min_defer_time = 3600
        max_defer_time = 25000

        IP = self.peer
        sender = self.sender
        def _isGreylisted(greylist, seen, IP,sender,recipient):
            print "GREY?", IP, sender, recipient
            # If greylisted, and not been there too long, allow through
            if greylist.get(triplet,None) is not None:
                greytime = float(greylist[triplet])
                if (time.time() - greytime) > max_grey:
                    del greylist[triplet]
                    try:
                        del seen[triplet]
                    except KeyError:
                        # We don't care if it's already gone
                        pass
                    print "REFUSED: grey too long"
                else:
                    print "ACCEPTED: already grey (have reset greytime)" ,
                    greylist[triplet] = str(time.time())
                    return True
            
            # If not seen this triplet before, defer and note triplet    
            if seen.get( triplet, None) is None:
                seen[triplet] = str(time.time())
                print "REFUSED: Not seen before" ,
                return False
        
            # If triplet retrying waaay too soon, reset their timer & defer
            last_tried = float(seen[triplet])
            if (time.time() - last_tried) < too_soon:
                seen[triplet] = str(time.time())
                print "REFUSED: Retrying waaay too soon so resetting you!" ,
                return False
        
            # If triplet retrying too soon generally speaking just defer
            if (time.time() - last_tried) < min_defer_time :
                print "REFUSED: Retrying too soon, deferring" ,
                return False
        
            # If triplet hasn't been seen in aaaages, defer
            if (time.time() - last_tried) > max_defer_time :
                seen[triplet] = str(time.time())
                print "REFUSED: Retrying too late, sorry - reseting you!" ,
                return False
        
            # Otherwise, allow through & greylist then
            print "ACCEPTED: Now added to greylist!" ,
            greylist[triplet] = str(time.time())
            return True

        greylist = anydbm.open("greylisted.dbm","c")
        seen = anydbm.open("attempters.dbm","c")
        triplet = repr((IP,sender,recipient))
        result = _isGreylisted(greylist, seen, IP,sender,recipient)
        seen.close()
        greylist.close()
        return result

    def whiteListed(self, recipient):
        for (IP, sender, r) in self.whitelisted_triples:
            if self.peer == IP:
                if self.sender == sender:
                    if recipient == r:
                        return True
        for (remotename, IP, r) in self.whitelisted_nonstandard_triples:
            if remotename == self.remotename:
                if IP == self.peer:
                    if r == recipient:
                        return True
        return False


    def shouldWeAcceptMail(self):
        if self.sentFromAllowedIPAddress():  return True # Allowed hosts can always send to anywhere through us
        if self.sentFromAllowedNetwork():    return True # People on truste networks can always do the same
        if self.sentToADomainWeForwardFor():
            try:
                for recipient in self.recipients:
                    if self.whiteListed(recipient):
                        return True
                    if not self.isGreylisted(recipient):
                        return False
            except Exception, e:
                print "Whoops", e
            return True # Anyone can always send to hosts we own

        # print "NOT ALLOWED TO SEND, no valid forwarding"
        return False

    def logResult(self):
        def m(x, w=2):
            return "0"*(w-len(str(x)))+str(x)
        now = time.time()
        msec = int((now -math.floor(now))*1000)
        x= time.gmtime(now)
        stamp =  "".join([ str(z) for z in [ m(x.tm_year,4), m(x.tm_mon,2), m(x.tm_mday,2), m(x.tm_hour,2), m(x.tm_min,2), m(x.tm_sec,2), ".", m(msec,3) ] ])

        logline  = str(stamp) + " | "
        logline += str(self.remotename) + " | "
        logline += str(self.peer) + " | "
        logline += str(self.sender) + " | "
        logline += str(", ".join(self.recipients)) + " | "
        logline += str(self.mailStatus) + " | "

        x = open("greylist.log","a")
        x.write(logline+"\n")
        x.flush()
        x.close()
        print logline


class GreylistServer(MoreComplexServer):
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 25
    class protocol(GreyListingPolicy):
        servername = "mail.cerenity.org"
        serverid = "MPS-SMTP 1.0"
        smtp_ip = "192.168.2.9"
        smtp_port = 8025
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
                            "kamaelia.org",
                            "owiki.org",
                            "cerenity.org"]
        whitelisted_triples = [ ]
        whitelisted_nonstandard_triples = [ ]

class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 120
    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send("tick", "outbox")

class WakeableIntrospector(Axon.Component.component):
    def main(self):
        while 1:
            x = open("greylist.log","a")
            x.write("*debug* THREADS"+ str([ q.name for q in self.scheduler.listAllThreads() ])+ "\n")
            x.flush()
            x.close()
            print "*debug* THREADS", [ x.name for x in self.scheduler.listAllThreads() ]
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            while self.dataReady("inbox"): self.recv("inbox")

from Kamaelia.Chassis.Pipeline import Pipeline
Pipeline(
    PeriodicWakeup(),
    WakeableIntrospector(),
).activate()

GreylistServer().run()
