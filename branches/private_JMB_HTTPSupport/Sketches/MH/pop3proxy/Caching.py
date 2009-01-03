#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import re

class SimpleCache(component):
    """\
    Persistently caches simple strings, passed as arrays of strings
    
    Only suitable for caching simple strings containing characters of byte value 32 (space character) or greater
    Can't therefore do multiline strings
    
    Send an array of strings to the inbox to save them.
    Send the string "GET" to teh inbox to retrieve them (will be sent out the outbox)
    """
    
    def __init__(self, filename):
        super(SimpleCache,self).__init__()
        self.filename=filename
        
    def main(self):
        while not self.shutdown():
            
            while not self.anyReady():
                self.pause()
                yield 1
                
            while self.dataReady("inbox"):
                msg=self.recv("inbox")
                if msg=="GET":
                    theCache=self.load()
                    self.send(theCache,"outbox")
                else:
                    theCache=msg
                    self.save(theCache)
                
                
    def shutdown(self):
        while self.dataReady("control"):
            msg=self.recv("control")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                self.send(msg,"signal")
                return True
            return False

    def save(self, dataItems):
        f=open(self.filename,"w")
        f.write("# Message UIDL cache\n")
        f.write("# Do not edit, especially whilst running!\n\n")
        for item in dataItems:
            f.write("+"+item+"+\n")
        f.close()    
        
    def load(self):
        linePattern=re.compile("^[+](.*)[+]$")
        try:
            f=open(self.filename,"r")
        except IOError:
            return []
        items=[]
        for line in f:
            line=line.replace("\n","").strip()
            try:
                (item,)=linePattern.match(line).groups()
                items.append(item)
            except AttributeError:
                pass
        f.close()
        return items



if __name__=="__main__":
    C=SimpleCache("testcachefile")
    C.save(["abc","",""," cde "])
    print C.load()
        