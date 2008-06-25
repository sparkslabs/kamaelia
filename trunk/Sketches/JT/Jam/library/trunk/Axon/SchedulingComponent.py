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

    def eventReady(self):
        if self.eventQueue:
            eventTime = self.eventQueue[0][0]
            if time.time() >= eventTime:
                return True
        return False

    def pause(self):
        if self.eventReady():
            self.signalEvent()
        else:
            if self.eventQueue:
                eventTime = self.eventQueue[0][0]
                super(SchedulingComponent, self).pause(eventTime - time.time())
                if self.eventReady():
                    self.signalEvent()
            else:
                super(SchedulingComponent, self).pause()

    def signalEvent(self):
        eventTime, priority, message = heapq.heappop(self.eventQueue)
        #print "Signalling, late by:", (time.time() - eventTime)
        if not self.inqueues["event"].full():
            self.inqueues["event"].put(message)
