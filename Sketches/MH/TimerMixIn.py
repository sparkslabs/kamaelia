#!/usr/bin/env python

from Axon.Component import component
from threading import Timer

class TimerMixIn(object):
  
    def __init__(self, *argl, **argd):
        super(TimerMixIn,self).__init__(*argl,**argd)
        self.timer = None
        self.timerSuccess = True
          
    def startTimer(self, secs):
        if self.timer is not None:
            self.cancelTimer()
        self.timer = Timer(secs, self.__handleTimerDone)
        self.timerSuccess = False
        self.timer.start()
  
    def cancelTimer(self):
        if self.timer is not None and self.timer:
             self.timer.cancel()
             self.timer = None
             self.timerSuccess = False
  
    def timerRunning(self):
        return self.timer is not None
        
    def timerWasCancelled(self):
        return not self.timerSuccess
  
    def __handleTimerDone(self):
        self.scheduler.wakeThread(self)
        self.timer = None
        self.timerSuccess = True
        

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
        
    class TestComponent(TimerMixIn,component):
        def __init__(self, label, duration):
            super(TestComponent,self).__init__()
            self.duration = duration
            self.label = label
            
        def main(self):
            while True:
            
                self.startTimer(self.duration)
                while self.timerRunning():
                    self.pause()
                    yield 1
                    
                self.send(self.label+"\n", "outbox")
                

    Graphline(
        A = TestComponent("a  ",0.5),
        B = TestComponent(" b ",0.2),
        C = TestComponent("  c",5.0),
        OUT = ConsoleEchoer(),
        linkages = {
            ("A", "outbox") : ("OUT", "inbox"),
            ("B", "outbox") : ("OUT", "inbox"),
            ("C", "outbox") : ("OUT", "inbox"),
        }).run()
    