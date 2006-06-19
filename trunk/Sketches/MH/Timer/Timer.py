#!/usr/bin/env python


# attempt at a timer

from Axon.Component import component
from heapq import heappush,heappop
import time

# events are a single value 'when' - representing the time
# the event should trigger


class Timer(component):
    Inboxes = { "inbox"   : "Requests for timing stuff go here.",
                "control" : "Shutdown signalling.",
              }
    Outboxes = { "outbox" : "Timing events emitted here.",
                 "signal" : "Shutdown signalling.",
               }
               
    def __init__(self):
        super(Timer,self).__init__()
        
        self.events = []         # partially ordered heap to be managed by heapq
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        while not self.shutdown():
            
            # get new event requests
            while self.dataReady("inbox"):
                when = self.recv("inbox")
                heappush(self.events, when)
            
            now=time.time()
            
            # pop off events that have triggered
            while len(self.events):
                if now < self.events[0]:
                    break
                else:
                    when = heappop(self.events)
                    self.send(when,"outbox")
                
            
            if not self.anyReady() and not len(self.events):
                self.pause()
            
            yield 1


if __name__ == "__main__":
    
    class TimerUser(component):
        def main(self):
            # schedule in mixed up order 6 events with the timer - one every
            # second
            
            now = time.time()
            self.send(now+1.0,"outbox")
            yield 1
            self.send(now+5.0,"outbox")
            yield 1
            self.send(now+3.0,"outbox")
            yield 1
            self.send(now+2.0,"outbox")
            yield 1
            
            while time.time() < now+3.0:   # pause for 3 seconds
                yield 1
                
            then = now
            now = time.time()
            # schedule one event before and one after what's left waiting in
            # the timer
            self.send(then+4.0,"outbox")   
            yield 1
            self.send(then+6.0,"outbox")
            yield 1
    
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    pipeline( TimerUser(),
              Timer(),
              ConsoleEchoer(),
            ).run()
            