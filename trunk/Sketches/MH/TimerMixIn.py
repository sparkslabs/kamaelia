#!/usr/bin/env python

from Axon.Component import component
from threading import Timer

class TimerMixIn(object):
  
    def __init__(self, *argl, **argd):
        super(TimerMixIn,self).__init__(*argl,**argd)
        self.timer = None
        self.timerSuccess = True
          
    def startTimer(self, secs):
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
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
        
    class TestComponent(TimerMixIn,component):
        def __init__(self):
            super(TestComponent,self).__init__()
            
        def main(self):
            count = 0
            
            while True:
            
                self.startTimer(0.5)
                while self.timerRunning():
                    self.pause()
                    yield 1
                    
                self.send(count, "outbox")
                count=count+1
                
    Pipeline(TestComponent(),ConsoleEchoer()).run()
    