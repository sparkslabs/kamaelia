#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Entuple(component):
    def __init__(self, prefix=[], postfix=[]):
        super(Entuple,self).__init__()
        self.prefix = prefix
        self.postfix = postfix
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                entupled = self.prefix + [data] + self.postfix
                self.send( entupled, "outbox" )
            self.pause()
            yield 1

