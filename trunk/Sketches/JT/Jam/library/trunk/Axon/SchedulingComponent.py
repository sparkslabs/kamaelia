# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ThreadedComponent import threadedcomponent, threadedadaptivecommscomponent
import heapq
import time

class SchedulingComponentMixin(object):
    """
    SchedulingComponent() -> new SchedulingComponent

    Base class for a threadedcomponent with an inbuilt scheduler, allowing a
    component to block until a scheduled event is ready or a message is received
    on an inbox.
    """

    Inboxes = {"inbox"   : "Standard inbox for receiving data from other components",
               "control" : "Standard inbox for receiving control messages from other components",
               "event"   : "Scheduled events which are ready to be processed"}

    def __init__(self, **argd):
        super(SchedulingComponentMixin, self).__init__(**argd)
        self.eventQueue = []
        
    def scheduleRel(self, message, delay, priority=1):
        """
        Schedule an event to wake the component and send a message to the
        "event" inbox after a delay.
        """
        return self.scheduleAbs(message, time.time() + delay, priority) 

    def scheduleAbs(self, message, eventTime, priority=1):
        """
        Schedule an event to wake the component and send a message to the
        "event" inbox after at a specified time.
        """
        event = eventTime, priority, message
        heapq.heappush(self.eventQueue, event)
        return event 
        
    def cancelEvent(self, event):
        """ Remove a scheduled event from the scheduler """
        self.eventQueue.remove(event)
        heapq.heapify(self.eventQueue)

    def eventReady(self):
        """ Returns true if there is an event ready to be processed """
        if self.eventQueue:
            eventTime = self.eventQueue[0][0]
            if time.time() >= eventTime:
                return True
        return False

    def pause(self):
        """
        Sleep until there is either an event ready or a message is received on
        an inbox
        """
        if self.eventReady():
            self.signalEvent()
        else:
            if self.eventQueue:
                eventTime = self.eventQueue[0][0]
                super(SchedulingComponentMixin, self).pause(eventTime - time.time())
                if self.eventReady():
                    self.signalEvent()
            else:
                super(SchedulingComponentMixin, self).pause()

    def signalEvent(self):
        """
        Put the event message of the earliest scheduled event onto the
        component's "event" inbox and remove it from the scheduler.
        """
        eventTime, priority, message = heapq.heappop(self.eventQueue)
        #print "Signalling, late by:", (time.time() - eventTime)
        if not self.inqueues["event"].full():
            self.inqueues["event"].put(message)

class SchedulingComponent(SchedulingComponentMixin, threadedcomponent):
    def __init__(self, **argd):
        super(SchedulingComponent, self).__init__(**argd)

class SchedulingAdaptiveCommsComponent(SchedulingComponentMixin,
                                       threadedadaptivecommscomponent):
    def __init__(self, **argd):
        super(SchedulingAdaptiveCommsComponent, self).__init__(**argd)
