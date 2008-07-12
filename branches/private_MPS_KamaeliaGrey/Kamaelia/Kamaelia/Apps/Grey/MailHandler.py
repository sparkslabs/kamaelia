
#
# This is primarily used by Kamaelia.Apps.ConcreteMailHandler
# It does form the basis of most things that need to handle basic SMTP type things
#

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
