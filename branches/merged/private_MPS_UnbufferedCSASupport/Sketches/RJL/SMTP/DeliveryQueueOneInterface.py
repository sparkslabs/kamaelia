import os
import time
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
from SMTPIPC import MIPCNewMessageFrom, MIPCNewRecipient, MIPCMessageBodyChunk, MIPCCancelLastUnfinishedMessage, MIPCMessageComplete


class DeliveryQueueOneInterface(component):
    Inboxes = {
        "msgid" : "Reply from unique id service",
        "inbox" : "Stuff from SMTPServer",
        "control" : "Shut me down"
    }
    Outboxes = {
        "requestmsgid" : "Ask unique id service for a number",
        "confirmsave" : "Tell SMTPServer the id we gave its message",
        "forwardon" : "Tell DQ1 about the message",
    }
    
    def __init__(self, uniqueidservice):
        super(DeliveryQueueOneInterface, self).__init__()    
        self.link((self, "requestmsgid"), (uniqueidservice, "inbox"))
        self.requestUniqueId()
                
    def requestUniqueId(self):
        self.send(self, "requestmsgid")
        
    def newFile(self):
        self.messagecount += 1
        self.filename = self.uniqueid + "." + str(self.messagecount)
        self.currentfile = open(os.path.join("received" , self.filename), "w")
        
    def cancelFile(self):
        if self.currentfile:
            self.currentfile.close()
            os.unlink("received/" + self.filename)
        self.filename = ""
        self.currentfile = None
        self.recipients = []
        
    def completeFile(self):
        print "completeFile()"
        self.writeString("C", "")
        self.currentfile.close()
        self.send(self.filename, "confirmsave") # tell the SMTPServer (incoming TCP connection handler) the id we gave the message        
        self.send((self.filename, self.recipients), "forwardon")
        
    def writeString(self, fieldletter, text):
        encodedform = fieldletter + str(len(text)) + "=" + text
        self.currentfile.write(encodedform) # should use a service of some kind to prevent blocking
        
    def main(self):
        self.uniqueid = ""
        self.messagecount = 0
        self.currentfile = None
        self.cancelFile()
        
        while not self.uniqueid:
            yield 1
            if self.dataReady("msgid"):
                self.uniqueid = self.recv("msgid")
            else:
                self.pause()
        
        print "DQ1I: My unique id is " + self.uniqueid
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                
                if isinstance(msg, MIPCNewMessageFrom):
                    self.newFile()
                    self.writeString("T", str(time.time())) # timestamp message - secs since epoch
                    self.writeString("F", msg.fromemail)

                elif isinstance(msg, MIPCNewRecipient):
                    self.recipients.append(msg.recipientemail)
                    self.writeString("R", msg.recipientemail)
                    
                elif isinstance(msg, MIPCMessageBodyChunk):
                    self.writeString("B", msg.data)
                
                elif isinstance(msg, MIPCMessageComplete):
                    self.completeFile()
                    
                elif isinstance(msg, MIPCCancelLastUnfinishedMessage):
                    self.cancelFile()
           
                else:
                    raise ValueError
                    
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdown):
                    return
                elif isinstance(msg, producerFinished):
                    return
            self.pause()
