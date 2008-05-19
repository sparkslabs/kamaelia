#!/usr/bin/env python


# attempt at a timer
#
# desireable usage model for the timer as a service:
# 
# class MyComponent(component):
#     def main(self):
#         Make timer plug
#         wire to its input and output
#         make timing requests to the plug

from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Axon.Ipc import shutdownMicroprocess,producerFinished
from Axon.Ipc import WaitComplete
from heapq import heappush,heappop
import time

from ThreadedComponent import threadedadaptivecommscomponent

# events are a single value 'when' - representing the time
# the event should trigger


class _TimerCore(threadedadaptivecommscomponent): # (AdaptiveCommsComponent):
    Inboxes = { "inbox"   : "Requests for timing stuff go here.",
                "register": "Registration/deregistration messages",
                "control" : "Shutdown signalling.",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling.",
               }
               
    def __init__(self):
        super(_TimerCore,self).__init__()
        
        self.events = []         # partially ordered heap to be managed by heapq
        self.mappings = {}       # (key,value) pairs: (handle, (outboxname,linkage))
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        while not self.shutdown():
            
            # handle new registration/deregistration requests
            while self.dataReady("register"):
                msg = self.recv("register")
                cmd = msg[0]
                if cmd == "REGISTER":
                    handle, target = msg[1], msg[2]
                    boxname = self.addOutbox("outbox")
                    linkage = self.link( (self,boxname), target[0], passthrough=target[1])
                    self.mappings[handle] = (boxname,linkage)
                    
                elif cmd == "DEREGISTER":
                    handle = msg[1]
                    boxname,linkage = self.mappings[handle]
                    self.unlink(thelinkage=linkage)
                    self.deleteOutbox(boxname)
            
            # get new event requests
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                heappush(self.events, event)
            
            now=time.time()
            
            # pop off events that have triggered
            timeout = None
            while len(self.events):
                if now < self.events[0][0]:
                    timeout = self.events[0][0] - now
                    break
                else:
                    (when,handle) = heappop(self.events)
                    try:
                        boxname = self.mappings[handle][0]
                        self.send(when,boxname)
                    except KeyError:
                        # in case the box has been deleted, just sink the event
                        pass
                
            
            if not self.anyReady():
                self.pause(timeout)
            
#            yield 1

    def setTimerServices(timer, tracker = None):
        """\
        Sets the given timer as the service for the selected tracker or the
        default one.

        (static method)
        """
        if not tracker:
            tracker = CAT.getcat()
        tracker.registerService("TimerRegister", timer, "register")
        tracker.registerService("TimerRequest", timer, "inbox")
    setTimerServices = staticmethod(setTimerServices)

    def getTimerServices(tracker=None): # STATIC METHOD
      """\
      Returns any live timer registered with the specified (or default) tracker,
      or creates one for the system to use.

      (static method)
      """
      if tracker is None:
         tracker = CAT.getcat()
      try:
         registerservice = tracker.retrieveService("TimerRegister")
         requestservice  = tracker.retrieveService("TimerRequest")
         return registerservice, requestservice, None
      except KeyError:
         timer = _TimerCore()
         _TimerCore.setTimerServices(timer, tracker)
         registerservice=(timer,"register")
         requestservice=(timer,"inbox")
         return registerservice, requestservice, timer
    getTimerServices = staticmethod(getTimerServices)

class Timer(component):
    Inboxes = { "inbox" : "Timer event requests go here",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Timing events emit from here",
                 "signal" : "Shutdown signalling",
                 "_eventsToTimer" : "Events to timer",
                 "_ctrlToTimer" : "Control requests to timer",
               }
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        # get access to the timer
        services = _TimerCore.getTimerServices()
        ctrllinkage = self.link((self,"_ctrlToTimer"),    services[0])
        eventlinkage = self.link((self,"_eventsToTimer"), services[1])
        if services[2]:
            services[2].activate()
        
        # request an outbox from the timer
        dest = ((self,"outbox"),2)
        self.send( ("REGISTER", self.id, dest), "_ctrlToTimer")
        
        while not self.shutdown():
            
            # receive timing requests, and add our handle to them and send on to the timer
            while self.dataReady("inbox"):
                when = self.recv("inbox")
                self.send( (when,self.id), "_eventsToTimer")

            self.pause()
            yield 1
        
        # detach from the timer
        self.send( ("DEREGISTER", self.id), "_ctrlToTimer")
        self.unlink(thelinkage = ctrllinkage)
        self.unlink(thelinkage = eventlinkage)
        


if __name__ == "__main__":
    
    class TimerUser(component):
        def __init__(self, offset=0.0, multiplier=1.0):
            self.offset=offset
            self.multiplier=multiplier
            super(TimerUser,self).__init__()
            
        def main(self):
            # schedule in mixed up order 6 events with the timer - one every
            # second
            m,o = self.multiplier, self.offset
            
            now = time.time()
            self.send(now+1.0*m+o,"outbox")
            yield 1
            self.send(now+5.0*m+o,"outbox")
            yield 1
            self.send(now+3.0*m+o,"outbox")
            yield 1
            self.send(now+2.0*m+o,"outbox")
            yield 1
            
            while time.time() < now+3.0*m+o:   # pause for 3 seconds
                yield 1
                
            then = now
            now = time.time()
            # schedule one event before and one after what's left waiting in
            # the timer
            self.send(then+4.0*m+o,"outbox")   
            yield 1
            self.send(then+6.0*m+o,"outbox")
            yield 1
    
#            self.send(producerFinished(), "signal")
    
    class Tag(component):
        def __init__(self,text):
            super(Tag,self).__init__()
            self.text = text
        def main(self):
            while 1:
                while self.dataReady("inbox"):
                    msg=self.recv("inbox")
                    self.send((self.text, msg),"outbox")
                self.pause()
                yield 1
    
    class InternalTimerUser(component):
        Inboxes = { "inbox" : "NOT USED",
                    "control" : "NOT USED",
                    "_fromTimer" : "Receive timer events",
                  }
        Outboxes = { "outbox" : "output",
                     "signal" : "shutdown signalling",
                     "_toTimer" : "Request timer notifications",
                     "_timerSignal" : "Shutdown timer",
                   }
                   
        def waitUntil(self, t):
            self.send( t, "_toTimer")
            while not self.dataReady("_fromTimer"):
                self.pause()
                yield 1
            self.recv("_fromTimer")
                   
        def main(self):
            timer = Timer().activate()
            self.addChildren(timer)
            self.link((self,"_toTimer"),(timer,"inbox"))
            self.link((timer,"outbox"),(self,"_fromTimer"))
            self.link((self,"_timerSignal"),(timer,"control"))
            
            for i in range(0,10):
                for _ in self.waitUntil( self.scheduler.time + 1.0): yield _
                self.send( "Waited, then output "+str(i),"outbox")
                
            yield 1
            self.send(producerFinished(), "_timerSignal")
            self.send(producerFinished(), "signal")
                
    
    class InternalTimerUser2(component):
        Inboxes = { "inbox" : "NOT USED",
                    "control" : "NOT USED",
                    "_fromTimer" : "Receive timer events",
                  }
        Outboxes = { "outbox" : "output",
                     "signal" : "shutdown signalling",
                     "_toTimer" : "Request timer notifications",
                     "_timerRegister" : "Register with the timer",
                   }
    
        def waitUntil(self, t):
            self.send( (t, self.id), "_toTimer")
            while not self.dataReady("_fromTimer"):
                self.pause()
                yield 1
            self.recv("_fromTimer")
    
        def main(self):
            registerService, requestService, timer = _TimerCore.getTimerServices()
            if timer:
                timer.activate()
            self.link((self,"_toTimer"), requestService)
            self.link((self,"_timerRegister"), registerService)
            dest = ((self,"_fromTimer"), 0)
            self.send( ("REGISTER", self.id, dest ), "_timerRegister")
            
            for i in range(0,10):
                for _ in self.waitUntil( self.scheduler.time + 1.0): yield _
                self.send( "Manual Waited, then output "+str(i),"outbox")
                
            yield 1
            self.send(producerFinished(), "signal")
    
    
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    pipeline( TimerUser(offset=0.5),
              Timer(),
              Tag("B"),
              ConsoleEchoer(),
            ).activate()
            
    pipeline( InternalTimerUser(),
              ConsoleEchoer(),
            ).activate()
            
    pipeline( InternalTimerUser2(),
              ConsoleEchoer(),
            ).activate()
            
    pipeline( TimerUser(),
              Timer(),
              Tag("A"),
              ConsoleEchoer(),
            ).run()
            