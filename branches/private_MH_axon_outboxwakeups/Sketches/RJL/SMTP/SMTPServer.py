# we don't deal with encoded addresses properly

import string

from Axon.Ipc import shutdown, producerFinished
from Axon.Component import component
from Kamaelia.Chassis.ConnectedServer import SimpleServer

from MailShared import isLocalAddress, listToDict
from SMTPIPC import MIPCNewMessageFrom, MIPCNewRecipient, MIPCMessageBodyChunk, MIPCCancelLastUnfinishedMessage, MIPCMessageComplete

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
    MaximumMessageSize = 10000000 # 10 MB
    """\
    SMTP protocol component for SimpleServer.
    
    Parameters:
    - hostname -- this server's hostname
    - storagequeue -- a shared DeliveryQueueOne component
    - localdict -- dictionary of {hostname: True} for all hostnames considered to be local for this server
    - uniqueidserivce -- UniqueId component
    """
    
    Inboxes = {
        "inbox" : "TCP in",
        "control" : "TCP shutdown",
        "queueconfirm" : "Confirmation of message saving",
    }
    Outboxes = {
        "outbox" : "TCP out",
        "signal" : "cause TCP shutdown",
        "dq1interface-signal" : "Shutdown our dq1 interface",
        "dq1interface" : "Delivery queue one interface component",
    }

    def sendToMailStorage(self, msg):
        self.send(msg, "dq1interface")
        
    def __init__(self, hostname, storagequeue, localdict, uniqueidservice, funccreateinterface):
        super(SMTPServer, self).__init__()
        self.hostname = hostname
        self.storagequeue = storagequeue
        self.localdict = localdict # messages that will be delivered locally rather than relayed
        
        self.readbuffer = ""
        
        self.waitinguponqueueconfirm = False
        
        self.queueinterface = funccreateinterface(uniqueidservice)
        self.queueinterface.activate()
        self.addChildren(self.queueinterface)
        
        self.link((self, "dq1interface"), (self.queueinterface, "inbox"))
        self.link((self.queueinterface, "forwardon"), (self.storagequeue, "inbox"))        
        self.link((self.queueinterface, "confirmsave"), (self, "queueconfirm"))
        self.link((self, "dq1interface-signal"), (self.queueinterface, "control"))
        
    def shouldShutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdown):
                return True
        return False
    
    def killInterface(self):
        self.send(producerFinished(self), "dq1interface-signal")
        
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
    
    def stateGetMailFrom(self, msg):       
        splitmsg = msg.split(" ",1)
        command = splitmsg[0].upper()
        
        if command == "NOOP":
            self.send("250 utterly pointless\r\n", "outbox")

        elif command == "VRFY":
            self.send("252 send some mail, i'll try my best\r\n", "outbox")
            
        elif command == "RSET":
            self.send("250 Ok\r\n", "outbox")
            self.doRSET()
            return
            
        elif command == "QUIT":
            return self.stateQuit
            
        elif command == "MAIL":
            if len(splitmsg) == 2:
                if splitmsg[1][:5].upper() == "FROM:":
                    fromemail = splitmsg[1][5:].strip()
                    # should add proper decoding here
                    
                    if fromemail[:1] == "<" and fromemail[-1:] == ">":
                        fromemail = fromemail[1:-1].strip()
                    
                    self.sendToMailStorage(MIPCNewMessageFrom(fromemail=fromemail))
                    
                    self.send("250 OK\r\n","outbox")
                    return self.stateGetRecipients
                else:
                    self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
            else:
                self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
        elif command == "RCPT":
            self.send("503 need MAIL before RCPT\r\n", "outbox")
        else:
            self.send("500 Unrecognised command\r\n", "outbox")                        

    def doRSET(self):
        self.msgsize = 0
        self.recipientcount = 0
        
    def stateGetRecipients(self, msg):
        splitmsg = msg.split(" ", 1)
        command = splitmsg[0].upper()
        
        if command == "VRFY":
            self.send("252 send some mail, i'll try my best\r\n", "outbox")
            
        elif command == "NOOP":
            self.send("250 utterly pointless\r\n", "outbox")        
            
        elif command == "RSET":
            self.send("250 Ok\r\n", "outbox")
            self.sendToMailStorage(MIPCCancelLastUnfinishedMessage())
            return self.stateGetMailFrom
            
        elif command == "DATA":
            if self.recipientcount == 0:
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
                        
                    if not isLocalAddress(toemail, self.localdict):
                         self.send("553 we don't relay mail to remote addresses\r\n", "outbox")
                    else:
                        self.recipientcount += 1
                        self.sendToMailStorage(MIPCNewRecipient(recipientemail=toemail))
                        self.send("250 OK\r\n", "outbox")
                else:
                    self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
            else:
                self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
        else:
            self.send("500 Unrecognised command\r\n", "outbox")                        

    def stateGetData(self, msg):
        # this is a bit dodgy - probably shouldn't really convert line breaks to \r\n
        # or wait for one before sending on stuff
        print msg
        if msg == ".":
            # end of data
            print "end of data"
            self.sendToMailStorage(MIPCMessageComplete())
            self.waitinguponqueueconfirm = True
            self.doRSET()
            return self.stateGetMailFrom
        else:
            self.sendToMailStorage(MIPCMessageBodyChunk(data=msg + "\r\n"))
            self.msgsize += len(msg) + 2
        
    def stateGetHELO(self, msg):
        splitmsg = msg.split(" ", 1)
        command = splitmsg[0].upper()
        
        if command == "NOOP":
            self.send("250 utterly pointless\r\n", "outbox")
            
        elif command == "HELO":
            if len(splitmsg) == 2:
                self.theirhostname = splitmsg[1]
                self.send("250 Hello " + self.theirhostname + "\r\n", "outbox")
                self.doRSET()
                return self.stateGetMailFrom
            else:
                self.send("501 Syntax error in parameters or arguments\r\n", "outbox")
        
        elif command == "EHLO":
            if len(splitmsg) == 2:
                self.theirhostname = splitmsg[1]
                self.send("250-" + self.hostname + " Hello " + self.theirhostname + "\r\n", "outbox")
                self.send("250-8BITMIME\r\n", "outbox")
                self.send("250-PIPELINING\r\n", "outbox")
                self.send("250 SIZE " + str(self.MaximumMessageSize) + "\r\n", "outbox")    
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
        self.send("220 " + self.hostname + " ESMTP KamaeliaRJL\r\n", "outbox")
        self.doRSET()        

        self.theirhostname = ""

        self.state = self.stateGetHELO

        while 1:
            if self.state == self.stateQuit:
                self.doQuit()
                self.killInterface()
                self.send(producerFinished(self), "signal")                
                return
                
            yield 1
            if self.shouldShutdown():
                self.killInterface()
                self.send(producerFinished(self), "signal")                
                return
            
            while self.dataFetch():
                pass
            
            msg = self.nextLine()
            while msg != None:
                if self.state == self.stateQuit:
                    self.doQuit()
                    self.killInterface()
                    self.send(producerFinished(self), "signal")
                    return
                
                newstate = self.state(msg)
                
                if self.waitinguponqueueconfirm:
                    print "SENDING MESSAGE"                
                    while self.waitinguponqueueconfirm:
                        if self.dataReady("queueconfirm"):
                            msgid = self.recv("queueconfirm")
                            self.waitinguponqueueconfirm = False
                            break
                        
                        self.pause()
                        yield 1
                    print "SENT MESSAGE"
                    self.send("250 Written safely to disk #" + str(msgid) + "\r\n", "outbox")
                    
                if newstate:
                    self.state = newstate

                msg = self.nextLine()
            else:
                self.pause()

    
if __name__ == '__main__':
    from Axon.Component import scheduler
    from DeliveryQueueOneInterface import DeliveryQueueOneInterface 
    from DeliveryQueueOne import DeliveryQueueOne
    from DeliveryQueueTwo import DeliveryQueueTwo
    from MailDelivery import LocalDelivery, RemoteDelivery
    from UniqueId import UniqueId
    from Kamaelia.Chassis.Pipeline import Pipeline
    import socket
    from Kamaelia.Util.Introspector import Introspector
    from Kamaelia.Internet.TCPClient import TCPClient
    
    hostname = "localhost"
    locallist = ["ronline.no-ip.info", "localhost"]
    localdict = listToDict(locallist)
    
    uniqueid = UniqueId().activate()
    deliveryqueueone = DeliveryQueueOne().activate()
    deliveryqueuetwo = DeliveryQueueTwo(localdict=localdict).activate()
    
    localdelivery = LocalDelivery(deliveryqueuedir="received", localmaildir="local").activate()
    remotedelivery = RemoteDelivery().activate()
    deliveryqueueone.link((deliveryqueueone, "outbox"), (deliveryqueuetwo, "inbox"))
    deliveryqueuetwo.link((deliveryqueuetwo, "local"), (localdelivery, "inbox"))
    deliveryqueuetwo.link((deliveryqueuetwo, "remote"), (localdelivery, "inbox"))    

    SMTPServerProtocol = lambda : SMTPServer(hostname="localhost", storagequeue=deliveryqueueone, localdict=localdict, uniqueidservice=uniqueid, funccreateinterface=DeliveryQueueOneInterface)
    SimpleServer(protocol=SMTPServerProtocol, port=8025, socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ).activate()
    scheduler.run.runThreads(slowmo=0)
