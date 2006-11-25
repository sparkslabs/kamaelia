#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class RangeFilter(component):
    """\
    RangeFilter(ranges) -> new RangeFilter component.
    
    Filters out items of the form (value, ...) not within at least one of a
    specified value set of range. Items within range are passed through.
    
    Keyword arguments::
        
    - ranges  -- list of (low,high) pairs representing ranges of value. Ranges are inclusive.
    """
    
    Outboxes = { "outbox" : "items in range",
                 "signal" : "Shutdown signalling"
               }

    def __init__(self, ranges):
        super(RangeFilter,self).__init__()
        self.ranges=ranges

    def inRange(self,index):
        for (start,end) in self.ranges:
            if index>=start and index<=end:
                return (start,end)
        return None

    def main(self):
        self.shutdownMsg = None
        try:
            while 1:
                while self.dataReady("inbox"):
                    item = self.recv("inbox")
                    index = item[0]
                    if self.inRange(index):
                        for _ in self.waitSend(item,"outbox"): yield _
                    
                if self.canStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                    

        except "STOP":
            self.send(self.shutdownMsg,"signal")

    # shutdown handling

    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)

    # data sending

    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise "STOP"



if __name__=="__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    print "Only items in ranges 1-5 and 8-12 should be output...\n\n"
    
    data = [
        (0, "shouldn't pass through"),
        (1, "YES!"),
        (2, "YES!"),
        (5, "YES!"),
        (6, "shouldn't pass through"),
        
        (7, "shouldn't pass through"),
        (8, "YES!"),
        (11, "YES!"),
        (12, "YES!"),
        (13, "shouldn't pass through"),
        
        (29, "shouldn't pass through"),
        (3, "YES!"),
    ]
    
    Pipeline( DataSource( data ),
              RangeFilter( [ (1,5), (8,12) ] ),
              ConsoleEchoer(),
            ).run()

    print