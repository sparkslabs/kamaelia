import ThreadedComponent
import heapq
import time

class SchedulingComponent(ThreadedComponent.threadedcomponent):
    Inboxes = ["inbox", "control", "event"]
    def __init__(self, **argd):
        super(SchedulingComponent, self).__init__(**argd)
        self.eventQueue = []
        
    def scheduleRel(self, message, delay, priority=1):
        return self.scheduleAbs(message, time.time() + delay, priority) 

    def scheduleAbs(self, message, eventTime, priority=1):
        event = eventTime, priority, message
        heapq.heappush(self.eventQueue, event)
        return event 
        
    def cancelEvent(self, event):
        self.eventQueue.remove(event)
        heapq.heapify(self.eventQueue)

    def pause(self):
        #print "Pausing"
        if self.eventQueue:
            eventTime, priority, message = self.eventQueue[0]
            #print "Inspecting event:", message, eventTime, priority
            if time.time() < eventTime:
                #print "Event not ready yet, calling wait with timeout", eventTime - time.time()
                #a = time.time()
                self.threadWakeUp.wait(eventTime - time.time())
                #print "wait over, lasted", time.time()-a
                self.threadWakeUp.clear()
                return
            else:
                #print "Event ready"
                self.signalEvent()
        else:
            self.threadWakeUp.wait()
            self.threadWakeUp.clear()
            
    def signalEvent(self):
        eventTime, priority, message = heapq.heappop(self.eventQueue)
        #print "Signalling, late by:", (time.time() - eventTime)
        if not self.inqueues["event"].full():
            self.inqueues["event"].put(message)
