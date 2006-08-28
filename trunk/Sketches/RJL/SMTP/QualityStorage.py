import os
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.Ipc import producerFinished, shutdown

import cPickle # so we can save dictionaries etc. to disk

class QualityStorageQueue(AdaptiveCommsComponent):
    Inboxes = ["addclient", "removeclient", "inbox", "control"]
    def __init__(self, queuename):
        self.queuename = queuename
        if not os.path.isdir("./" + self.queuename):
            os.mkdir("./" + self.queuename)
        self.outboxFor = {}
        super(QualityStorageQueue, self).__init__()
        
    def writeFile(self, msg):
        self.messages += 1
        filehandle = open(self.queuename + "/" + str(self.messages), "w")
        filehandle.write(cPickle.dumps(msg))
        filehandle.close()
   
    def addClient(self, replyService):
        print "Adding client!"

        particularOutbox = self.addOutbox("clientoutbox")
        self.link((self, particularOutbox), replyService)
        self.outboxFor[replyService] = particularOutbox
        
    def removeClient(self, replyService):
        print "Removing client!"
       
        particularOutbox = self.outboxFor[replyService]
        self.unlink((self, particularOutbox), replyService)
        
    def main(self):
        self.messages = 0
        while 1:
            msg = None
            yield 1
            
            while self.dataReady("addclient"):
                msg = self.recv("addclient")
                self.addClient(msg)
                
            while self.dataReady("removeclient"):
                msg = self.recv("removeclient")
                self.removeClient(msg)
                                
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                correctOutbox = self.outboxFor[msg[0]]
                self.writeFile(msg[1])
                self.send(True, correctOutbox)
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return
    
            self.pause()
            
