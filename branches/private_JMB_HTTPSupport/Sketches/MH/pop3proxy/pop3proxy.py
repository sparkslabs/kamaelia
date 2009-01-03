#!/usr/bin/env python
#
# Simple POP3 relaying proxy with message filtering
#
# The idea is for this to act as much as possible as a transparent proxy,
# but for it also to be able to hide messages from the client if they have
# certain properties - eg. are MS Exchange Calendar requests

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

from Caching import SimpleCache

import time
import re
import sys

PROXYSERVER_PORT=20110
POP3SERVER_NAME="localhost"
POP3SERVER_PORT=10110

PERSISTENCE_STORE_FILENAME="/tmp/pop3proxy.uidls.cache"

CRLF="\x0d\x0a"
    
OK = re.compile("^[+]OK([ ]+.*|)$")    # match an OK msg
ERR = re.compile("^[-]ERR([ ]+.*|)$")  # match an ERR msg


class Pop3CommandRelay(component):
    Inboxes = {
      "inbox"   : "Commands from client",
      "control" : "Shutdown signalling from client",
    
      "fromServer"       : "",
      "fromServerSignal" : "",
      
      "fromStore" : "",
    }
  
    Outboxes = {
        "outbox"  : "To client",
        "signal"  : "Shutdown signalling to client",
    
        "toServer"         : "",
        "toServerControl"  : "",
        
        "toStore"          : "",
        "toStoreControl"   : "",
    }
  
    def main(self):
        self.invalidateMailState()
        
        self.log("CONNECTED : "+time.asctime())

        while not self.shutdown():
        
            while not self.anyReady():
                self.pause()
                yield 1

            while self.dataReady("fromServer"):
                msg=self.recv("fromServer")
                self.log("Server: "+str(msg))
                self.send(msg+CRLF, "outbox")

            while self.dataReady("inbox"):
                msg=self.recv("inbox")
                handler = self.findClientMsgHandler(msg)
                
                try:
                    for _ in handler:
                        yield _
                        while not self.anyReady():
                            self.pause()
                            yield 1
                        if self.shutdown():
                            return
                except:
                    print str(sys.exc_info())
                    self.send("-ERR Proxy problem"+CRLF, "outbox")
                    self.log("|----")
              
        self.log("CLOSED")
        
    def log(self,msg):
        print "%10d : %s" % (self.id, msg)

    def shutdown(self):
        for inbox in ("control","fromServerSignal"):
            while self.dataReady(inbox):
                msg=self.recv(inbox)
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    self.send(msg,"toServerControl")
                    self.send(msg,"toStoreControl")
                    self.send(msg,"signal")
                    return True
        return False


    def findClientMsgHandler(self, msg):
        # core, rfc 1939
        
        if re.compile("^QUIT([ ]+.*|)$").match(msg):
            return self.handle_QUIT(msg)
        
        if re.compile("^STAT([ ]+.*|)$").match(msg):
            return self.handle_STAT(msg)
        
        if re.compile("^LIST *$").match(msg):
            return self.handle_LIST(msg)
        
        if re.compile("^LIST +[0-9]+").match(msg):
            return self.handle_LIST_N(msg)
        
        if re.compile("^RETR +[0-9]+").match(msg):
            return self.handle_RETR(msg)
        
        if re.compile("^DELE +[0-9]+").match(msg):
            return self.handle_DELE(msg)
        
        if re.compile("^NOOP([ ]+.*|)$").match(msg):
            return self.handle_NOOP(msg)
        
        if re.compile("^RSET([ ]+.*|)$").match(msg):
            return self.handle_RSET(msg)
        
        # optional, rfc 1939
        
        if re.compile("^TOP ").match(msg):
            return self.handle_TOP(msg)
          
        if re.compile("^UIDL *$").match(msg):
            return self.handle_UIDL(msg)
        
        if re.compile("^UIDL +[0-9]+").match(msg):
            return self.handle_UIDL_N(msg)
        
        if re.compile("^USER([ ]+.*|)$").match(msg):
            return self.handle_USER(msg)
        
        if re.compile("^PASS([ ]+.*|)$").match(msg):
            return self.handle_PASS(msg)
        
        if re.compile("^APOP([ ]+.*|)$").match(msg):
            return self.handle_APOP(msg)
        
        # rfc 1734 / 5034
        
        if re.compile("^AUTH([ ]+.*|)$").match(msg):
            return self.handle_AUTH(msg)
        
        # rfc 2449
        
        if re.compile("^CAPA([ ]+.*|)$").match(msg):
            return self.handle_CAPA(msg)
            
        # ELSE
        return self.handle_unsupported(msg)
    
    def sendToClient(self, msg, logAlternative=None):
        if logAlternative is None:
            logAlternative=msg
        self.log("| s  : "+str(logAlternative))
        self.send(msg+CRLF, "outbox")
        
        
    def sendToServer(self, msg, logAlternative=None):
        if logAlternative is None:
            logAlternative=msg
        self.log("|  c : "+str(logAlternative))
        self.send(msg+CRLF, "toServer")
        
    
    def recvFromClient(self):
        msg=self.recv("outbox")
        self.log("|C   : "+str(msg))
        return msg
    
    def recvFromServer(self):
        msg=self.recv("fromServer")
        self.log("|   S: "+str(msg))
        return msg
    
    def dataReadyFromServer(self):
        return self.dataReady("fromServer")
    
    def dataReadyFromClient(self):
        return self.dataReady("inbox")
    
    def handle_unsupported(self, req):
        self.log("***UNSUPPORTED : "+str(req))
        self.sendToClient("-ERR sorry - this proxy doesn't support this command. Can't handle it :-(")
        yield 1
        self.log("|---")
        
        
    def handle_QUIT(self, req):
        self.log("QUIT : "+str(req))
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")
        
        # persistently store our pretend deletions so they're remembered next time
        pretendDeletedUidls=[]
        for msgId in self.pretendDeleted:
            print msgId
            uidl=self.msgsOnServer[msgId]["uidl"]
            print uidl
            pretendDeletedUidls.append(uidl)
        self.send(pretendDeletedUidls, "toStore")
        
        
    def handle_STAT(self, req):
        self.log("STAT : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        try:
            numMsgs,totalSize,tail = re.compile("^[+]OK +([0-9]+?) +([0-9]+)( +.*| *)$").match(msg).groups()
            numMsgs=int(numMsgs)
            totalSize=int(totalSize)
            for msgId in self.pretendDeleted:
                numMsgs=numMsgs-1
                totalSize=totalSize-self.msgsOnServer[msgId]["size"]
            self.sendToClient("+OK %d %d%s" % (numMsgs,totalSize,tail))
        except AttributeError:
            self.sendToClient("-ERR Proxy had problems understanding response from the server")
        self.log("|---")
        
        
    def handle_LIST(self, req):
        self.log("LIST : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        self.sendToServer(req)
        
        msg=""
        while msg != "." and not ERR.match(msg):
            while not self.dataReadyFromServer():
                yield 1
                
            msg=self.recvFromServer()
            if OK.match(msg) or msg=="." or ERR.match(msg):
                self.sendToClient(msg)
            else:
                # hide any scan listing for any messages we're PRETENDING to have deleted
                try:
                    msgId,tail = re.compile("^ *([0-9]+) +(.*)$").match(msg).groups()
                    if msgId not in self.pretendDeleted:
                        self.sendToClient(msg)
                except AttributeError:
                    self.sendToClient("-ERR Proxy had problems understanding response from server")
                    self.log("|---")
                    return
        self.log("|---")
    
    
    def handle_LIST_N(self, req):
        self.log("LIST N : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        if False==self.canProceedForMsgId("^LIST +([0-9]+) *$",req):
            self.log("|---")
            return
        
        # ok, no pretending to do, so pass on the request as normal
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")


    def canProceedForMsgId(self, extractMsgIdRegex, req):
        """\
        Uses supplied regex to extract msgId from supplied request/command string.
        Returns False if msgId is in the list of message id's we're pretending have been deleted
        Otherwise returns teh msgId as a string.
        Note this might be an empty string, so you must explicity test for equality to False.
        """
        try:
            (msgId,)=re.compile(extractMsgIdRegex).match(req).groups()
        except AttributeError:
            self.sendToClient("-ERR Proxy didn't understand this command")
            return False

        if msgId in self.pretendDeleted:
            self.sendToClient("-ERR Message doesn't exist (or that's what I'm pretending!)")
            return False
        else:
            return msgId

    def handle_RETR(self, req):
        self.log("RETR : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        if False==self.canProceedForMsgId("^RETR +([0-9]+) *$",req):
            self.log("|---")
            return
        
        self.sendToServer(req)
        
        msg=""
        while msg != "." and not ERR.match(msg):
            while not self.dataReadyFromServer():
                yield 1
                
            msg=self.recvFromServer()
            self.sendToClient(msg)

        self.log("|---")

    
    def handle_DELE(self, req):
        self.log("DELE : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        msgId=self.canProceedForMsgId("^DELE +([0-9]+) *$",req)
        if msgId==False:
            self.log("|---")
            return
        elif msgId in self.preventDeletions:
            self.sendToClient("+OK We'll pretend to have deleted that!")
            self.log("|---")
            self.pretendDeleted.append(msgId)
            return
        
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")
    
    
    def handle_NOOP(self, req):
        self.log("NOOP : "+str(req))
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")


    def handle_RSET(self, req):
        self.log("RSET : "+str(req))
        
        self.invalidateMailState()
        
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")
        

    
    def handle_USER(self, req):
        self.log("USER : "+str(req))
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")
        
        
    def handle_PASS(self, req):
        reqMasked="PASS "+("*"*len(req[5:]))  # mask out password for logging output
        self.log("PASS : "+str(reqMasked))
        self.sendToServer(req, logAlternative=reqMasked)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")


    def handle_TOP(self, req):
        self.log("TOP : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        if False==self.canProceedForMsgId("^TOP +([0-9]+) +.*$",req):
            self.log("|---")
            return
        
        self.sendToServer(req)
        
        msg=""
        while msg != "." and not ERR.match(msg):
            while not self.dataReadyFromServer():
                yield 1
                
            msg=self.recvFromServer()
            self.sendToClient(msg)

        self.log("|---")
    
    
    def handle_UIDL(self, req):
        self.log("UIDL : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        self.sendToServer(req)

        msg=""
        while msg != "." and not ERR.match(msg):
            while not self.dataReadyFromServer():
                yield 1
                
            msg=self.recvFromServer()
            if OK.match(msg) or msg=="." or ERR.match(msg):
                self.sendToClient(msg)
            else:
                # hide any scan listing for any messages we're PRETENDING to have deleted
                try:
                    msgId,tail = re.compile("^ *([0-9]+) +(.*)$").match(msg).groups()
                    if msgId not in self.pretendDeleted:
                        self.sendToClient(msg)
                except AttributeError:
                    self.sendToClient("-ERR Proxy had problems understanding response from server")
                    self.log("|---")
                    return
        self.log("|---")


    def handle_UIDL_N(self, req):
        self.log("UIDL N : "+str(req))
        
        if not self.gotMailState:
            for _ in self.getMailState():
                yield _
        
        if False==self.canProceedForMsgId("^UIDL +([0-9]+) *$",req):
            self.log("|---")
            return
        
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")


    def handle_APOP(self, req):
        self.log("APOP : "+str(req))
        self.sendToServer(req)
        
        while not self.dataReadyFromServer():
            yield 1
            
        msg=self.recvFromServer()
        self.sendToClient(msg)
        self.log("|---")


    def handle_AUTH(self, req):
        self.log("AUTH : "+str(req))
        self.sendToServer(req)
        
        msg=""
        while not ERR.match(msg) and not OK.match(msg):
            while not self.dataReadyFromServer() and not self.dataReadyFromClient():
                yield 1
                
            if self.dataReadyFromClient():
                msg=self.recvFromClient()
                self.sendToServer(msg)

            if self.dataReadyFromServer():
                msg=self.recvFromServer()
                self.sendToClient(msg)

        self.log("|---")
    
    
    def handle_CAPA(self, req):
        self.log("CAPA : "+str(req))
        self.sendToServer(req)
        
        msg=""
        while msg != "." and not ERR.match(msg):
            while not self.dataReadyFromServer():
                yield 1
                
            msg=self.recvFromServer()
            self.sendToClient(msg)

        self.log("|---")


    def invalidateMailState(self):
        self.msgsOnServer={}
        self.pretendDeleted=[]
        self.preventDeletions=[]
        self.gotMailState=False
    

    def getMailState(self):
        """\
        Query the server to find out what mail is on it, and get headers for all those messages
        
        Uses LIST, UIDL and TOP
        """
        self.invalidateMailState()
        
        uidls={}
        for _ in self.getUIDLs(uidls):
            yield _
            
        sizes={}
        for _ in self.getLIST(sizes):
            yield _
            
        for msgId in uidls:
            self.msgsOnServer[msgId] = { "uidl": uidls[msgId], "size": sizes[msgId] }
            top=[]
            for _ in self.getTOP(msgId, top):
                yield _
            isCalendarRequest = self.checkIfCalendarRequest(top)
            if isCalendarRequest and not msgId in self.preventDeletions:
                self.log("| >>  : Detected calendar request, msgId "+str(msgId))
                self.preventDeletions.append(msgId)
                
        self.send("GET", "toStore")
        while not self.dataReady("fromStore"):
            yield 1
        alreadyDeletedUidls=self.recv("fromStore")
        
        # ignore cached uidl if not present on the server any more...
        for msgId in uidls:
            uidl=uidls[msgId]
            if uidl in alreadyDeletedUidls:
                self.pretendDeleted.append(msgId)
            
        self.gotMailState=True
            
            
    def getUIDLs(self, uidls):
        self.sendToServer("UIDL")
        while not self.dataReadyFromServer():
            yield 1
        rsp=self.recvFromServer()
        
        if ERR.match(rsp):
            raise "FAILURE"
            
        if OK.match(rsp):
            line=""
            while line != ".":
                while not self.dataReadyFromServer():
                    yield 1
                line=self.recvFromServer()
                if line != ".":
                    try:
                        msgId,uidl = self.parse_UIDL_line(line)
                        uidls[msgId]=uidl
                    except:
                        self.log("| ERR : not a recognised UIDL response line")
            
            for (msgId,uidl) in uidls.items():
                self.log("| >>  : msgId, uidl = "+str(msgId)+" , "+str(uidl))
        
        else:
            raise "FAULT"


    def parse_UIDL_line(self, line):
        match = re.compile("^ *([0-9]+) +(.+) *$").match(line)
        if not match:
            raise "Not a UIDL line"
        msgId=match.group(1)
        uidl=match.group(2)
        return (msgId, uidl)
    
    
    def getLIST(self, sizes):
        self.sendToServer("LIST")
        while not self.dataReadyFromServer():
            yield 1
        rsp=self.recvFromServer()
        
        if ERR.match(rsp):
            raise "FAILURE"
            
        if OK.match(rsp):
            line=""
            while line != ".":
                while not self.dataReadyFromServer():
                    yield 1
                line=self.recvFromServer()
                if line != ".":
                    try:
                        msgId,size = self.parse_LIST_line(line)
                        sizes[msgId]=size
                    except:
                        self.log("| ERR : not a recognised LIST response line")
            
            for (msgId,size) in sizes.items():
                self.log("| >>  : msgId, size = "+str(msgId)+" , "+str(size))
        
        else:
            raise "FAULT"
                

    def parse_LIST_line(self, line):
        match = re.compile("^ *([0-9]+) +([0-9]+)(?: +.*| *)$").match(line)
        if not match:
            raise "Not a UIDL line"
        msgId=match.group(1)
        size=int(match.group(2))
        return (msgId, size)
    
    
    def getTOP(self, msgId, top):
        self.sendToServer("TOP "+str(msgId)+" 0")
        while not self.dataReadyFromServer():
            yield 1
        rsp=self.recvFromServer()
        
        if ERR.match(rsp):
            raise "FAILURE"
            
        if OK.match(rsp):
            line=""
            while line != ".":
                while not self.dataReadyFromServer():
                    yield 1
                line=self.recvFromServer()
                if line != ".":
                    top.append(line)
        
        else:
            raise "FAULT"
    
    
    def checkIfCalendarRequest(self, headers):
        for line in headers:
            if line.strip() == "Content-class: urn:content-classes:calendarmessage":
                return True
        return False
    
    
class LineSplit(component):
    """\
    De-chunks incoming stream and splits into separate messages at delimiters.
    ("CRLF"s by default)
    
    Does not include the delimiter in the passed on message.
    """
    def __init__(self, delim="\x0d\x0a"):
        super(LineSplit,self).__init__()
        self.delim = delim
        
    def main(self):
        buffer=""
        
        while 1:

            while not self.anyReady():
                self.pause()
                yield 1

            while self.dataReady("inbox"):
                buffer+=self.recv("inbox")
                
                offset=buffer.find(self.delim)
                while offset>=0:
                    msg=buffer[:offset]
                    self.send(msg,"outbox")
                    buffer=buffer[offset+len(self.delim):]
                    offset=buffer.find(self.delim)
        
            # do this last (after returning from pause state)
            # so that we've processed any data first
            if self.shutdown():
                return
                
    def shutdown(self):
        while self.dataReady("control"):
            msg=self.recv("control")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                self.send(msg,"signal")
                return True
            return False



def Pop3Proxy():
    return Graphline(
        SERVER = TCPClient(POP3SERVER_NAME, POP3SERVER_PORT),
        RELAY = Pop3CommandRelay(),
        LINESPLIT_CMDS = LineSplit(),
        LINESPLIT_RESP = LineSplit(),
        DELETION_STORE = SimpleCache(PERSISTENCE_STORE_FILENAME),
        linkages = {
            ("", "inbox")   : ("LINESPLIT_CMDS", "inbox"),
            ("", "control") : ("LINESPLIT_CMDS", "control"),
            
            ("LINESPLIT_CMDS", "outbox") : ("RELAY", "inbox"),
            ("LINESPLIT_CMDS", "signal") : ("RELAY", "control"),
            
            ("RELAY", "toServer")        : ("SERVER", "inbox"),
            ("RELAY", "toServerControl") : ("SERVER", "control"),
            
            ("SERVER", "outbox") : ("LINESPLIT_RESP", "inbox"),
            ("SERVER", "signal") : ("LINESPLIT_RESP", "control"),
            
            ("LINESPLIT_RESP", "outbox") : ("RELAY", "fromServer"),
            ("LINESPLIT_RESP", "signal") : ("RELAY", "fromServerSignal"),
            
            ("RELAY", "outbox") : ("", "outbox"),
            ("RELAY", "signal") : ("", "signal"),
            
            ("RELAY", "toStore") : ("DELETION_STORE", "inbox"),
            ("RELAY", "toStoreControl")  : ("DELETION_STORE", "control"),
            ("DELETION_STORE", "outbox") : ("RELAY", "fromStore"),
            
        }
    )
    
SimpleServer(protocol=Pop3Proxy, port=PROXYSERVER_PORT).run()
