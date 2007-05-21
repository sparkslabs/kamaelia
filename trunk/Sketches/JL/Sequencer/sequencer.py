#! /usr/bin/env python
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

class sequencer(component):
#Inboxes: inbox, control
#Outboxes: outbox, signal
    n = 5
    def __init__(self):
        super(sequencer, self).__init__()
        self.running = True
        
    def findNext(self):
        self.n += 1
        return self.n
    
    def printNext(self):
        print self.findNext()
        
    def main(self):
        while self.running:
##            self.send('message', 'outbox')
            if self.dataReady("control"):
                msg = self.recv("control")
                print "received control message: ", msg
                if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                    self.shutdown()
                    break
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                print "received inbox message: ", msg
                if msg == "NEXT":
                    self.send(self.findNext(), 'outbox')
            yield 1

    def shutdown(self):
        self.running = False
        self.send(producerFinished(), "signal")

                
class fibonacciSequencer(sequencer):
    def __init__(self):
        super(fibonacciSequencer, self).__init__()
        self.n = 0
        self.n_1 = 1
        
    def findNext(self):
        val = self.n
        self.n = self.n_1
        self.n_1 = val + self.n_1
        return val
    
    def main(self):
        i = 0
        while i < 20:
            yield 1
            self.printNext()
            i = i+1
        self._closeDownMicroprocess()
            
                
        
class naturals(sequencer):
    def __init__(self):
        super(naturals, self).__init__()
        self.n = 0
        
    def findNext(self):
        self.n = self.n + 1
        return self.n

