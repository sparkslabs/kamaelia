import string

from Axon.Ipc import shutdown, producerFinished
from Axon.Component import component
from Kamaelia.Chassis.ConnectedServer import SimpleServer

"""
Minimum implementation for SMTP is:
COMMANDS -- HELO
            MAIL
            RCPT
            DATA
            RSET
            NOOP
            QUIT
"""

def removeTrailingCr(line):
    if len(line) == 0:
        return line
    elif line[-1] == "\r":
        return line[0:-1]
    else:
        return line
    
class SMTPServer(component):
    Inboxes = {
        "inbox" : "TCP in",
        "control" : "TCP shutdown",
        "queueconfirm" : "Confirmation of message saving",
    }
    Outboxes = {
        "outbox" : "TCP out",
        "signal" : "cause TCP shutdown",
        
        "savequeue" : "send messages to the storagequeue",
        "registerqueue" : "register with the storagequeue",
        "deregisterqueue" : "deregister with the storagequeue"
    }

    def deregisterStorageQueue(self):
        self.send((self, "queueconfirm"), "deregisterqueue")
        
    def __init__(self, hostname, storagequeue):
        super(SMTPServer, self).__init__()
        self.hostname = hostname
        self.readbuffer = ""
        self.storagequeue = storagequeue
        self.waitinguponqueueconfirm = False
        
        self.link((self, "registerqueue"), (self.storagequeue, "addclient"))
        self.link((self, "deregisterqueue"), (self.storagequeue, "removeclient"))        
        self.link((self, "savequeue"), (self.storagequeue, "inbox"))                
        self.send((self, "queueconfirm"), "registerqueue")

    
    def isLocalAddress(self, address):    
        if address[-(1+len(self.hostname)):-len(self.hostname)] == "@" and address[-len(self.hostname):] == self.hostname:
            return True
        else:
            return False

    def shouldShutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdown):
                return True
        return False
        
        
    def dataFetch(self):
        if self.dataReady("inbox"):
            msg = self.recv("inbox")
            self.readbuffer += msg
            return True
        else:
            return False
    
    def nextLine(self):
        lineendpos = self.readbuffer.find("\n")
        if lineendpos == -1:
            return None
        else:
            line = removeTrailingCr(self.readbuffer[:lineendpos])
            self.readbuffer = self.readbuffer[lineendpos + 1:] #the remainder after the \n
            return line

    def sendGreeting(self):
        """Send initial server greeting to client"""
        self.send("220 " + self.hostname + " SMTP KamaeliaRJL\r\n", "outbox")

    def sendDownMessage(self):
        """Message if the server is (or is going) down - seldom used"""
        self.send("421 " + hostname + " Service not available, closing transmission channel\r\n", "outbox")
    
    def acceptMessage(self, message):
        self.send(message, "deliver")
        return True
    
    def stateGetMailFrom(self, msg):       
        splitmsg = msg.split(" ",1)
        command = splitmsg[0].upper()
        
        if command == "RSET":
            self.send("250 Ok\r\n", "outbox")
            self.doRSET()
            return
        elif command == "QUIT":
            return self.stateQuit
        elif command == "MAIL":
            if len(splitmsg) == 2:
                if splitmsg[1][:5].upper() == "FROM:":
                    fromemail = splitmsg[1][5:].strip()
                    if fromemail[:1] == "<" and fromemail[-1:] == ">":
                        fromemail = fromemail[1:-1].strip()
                    
                    self.envelope["fromemail"] = fromemail
                    self.send("250 OK\r\n","outbox")
                    return self.stateGetRecipients
                else:
                    self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
            else:
                self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
        else:
                self.send("500 Unrecognised command\r\n", "outbox")                        

    def doRSET(self):
        self.envelope = { "fromemail" : "", "recipients" : [], "msgdata" : "" }
        self.msgdata = []
        
    def stateGetRecipients(self, msg):
        splitmsg = msg.split(" ", 1)
        command = splitmsg[0].upper()
        
        if command == "RSET":
            self.send("250 Ok\r\n", "outbox")
            return self.stateGetMailFrom
        elif command == "DATA":
            if len(self.envelope["recipients"]) == 0:
                self.send("503 need RCPT before DATA\r\n", "outbox")
            else:
                self.send("354 End data with <CR><LF>.<CR><LF>\r\n", "outbox")
                return self.stateGetData
        elif command == "RCPT":
            if len(splitmsg) == 2:
                if splitmsg[1][:3].upper() == "TO:":
                    toemail = splitmsg[1][3:].strip()
                    if toemail[:1] == "<" and toemail[-1:] == ">":
                        toemail = toemail[1:-1].strip()
                        
                    if not self.isLocalAddress(toemail):
                         self.send("553 we don't relay mail to remote addresses\r\n", "outbox")
                    else:
                        self.envelope["recipients"].append(toemail)                    
                        self.send("250 OK\r\n", "outbox")
                else:
                    self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
            else:
                self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
        else:
            self.send("500 Unrecognised command\r\n", "outbox")                        

    def stateGetData(self, msg):
        # might be better to store data to file as we go along to save memory
        if msg == ".":
            # end of data
            self.envelope["msgdata"] = "".join(self.msgdata)
            self.send([(self, "queueconfirm"), self.envelope], "savequeue")
            self.waitinguponqueueconfirm = True
            return self.stateGetMailFrom
        else:
            self.msgdata.append(msg)
            self.msgdata.append("\r\n")

        
    def stateGetHELO(self, msg):
        splitmsg = msg.split(" ", 1)
        command = splitmsg[0].upper()
        
        if command == "HELO":
            if len(splitmsg) == 2:
                self.theirhostname = splitmsg[1]
                self.send("250 Hello " + self.theirhostname + "\r\n", "outbox")
                self.doRSET()
                return self.stateGetMailFrom
            else:
                self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
        else:
                self.send("500 Nice people say HELO\r\n", "outbox")

    def stateQuit(self):
        pass
        
    def doQuit(self):
        self.send("221 " + self.hostname + " Closing Connection\r\n", "outbox")
        
        
    def main(self):
        # possible enhancements - support ESMTP and associated extensions
        self.sendGreeting()
        self.doRSET()        

        self.theirhostname = ""

        self.state = self.stateGetHELO

        while 1:
            if self.state == self.stateQuit:
                self.doQuit()
                self.deregisterStorageQueue()
                self.send(producerFinished(self), "signal")                
                return
                
            yield 1
            if self.shouldShutdown():
                self.deregisterStorageQueue()
                self.send(producerFinished(self), "signal")                
                return
            
            while self.dataFetch():
                pass
            
            msg = self.nextLine()
            while msg:
                if self.state == self.stateQuit:
                    self.doQuit()
                    self.deregisterStorageQueue()
                    self.send(producerFinished(self), "signal")
                    return
                
                newstate = self.state(msg)
                
                if self.waitinguponqueueconfirm:
                    print "SENDING MESSAGE"                
                    while self.waitinguponqueueconfirm:
                        if self.dataReady("queueconfirm"):
                            confirmation = self.recv("queueconfirm")
                            self.waitinguponqueueconfirm = False
                            break
                        
                        self.pause()
                        yield 1
                    print "SENT MESSAGE"
                    self.send("250 Ok\r\n", "outbox")
                    
                if newstate:
                    self.state = newstate

                msg = self.nextLine()
            else:
                self.pause()



if __name__ == '__main__':
    from Axon.Component import scheduler
    from QualityStorage import QualityStorageQueue 
    import socket
    
    hostname = "localhost"
    deliverycomponent = QualityStorageQueue("received").activate()
    
    SimpleServer(protocol=lambda : SMTPServer("localhost", deliverycomponent), port=8025, socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).activate()
    scheduler.run.runThreads(slowmo=0)
