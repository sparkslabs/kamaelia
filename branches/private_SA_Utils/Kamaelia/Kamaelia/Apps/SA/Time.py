'''
This file contains some utility classes which are used by both the client and
server components of the port tester application.
'''

import time
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.IPC import serverShutdown

class SingleTick(Axon.ThreadedComponent.threadedcomponent):
    '''
    This threaded component will wait "delay" seconds then send True out it's
    outbox and shutdown.  You can specify an optional "check_interval" which
    will cause the component to periodically check it's control inbox for
    early termination signals.
    
    SingleTick(delay, check_interval=delay, tick_mesg=True)
    '''
    Inboxes = {'inbox':'ignored', 
               'control':'Sending a message here will cause the component to shutdown'}
    Outboxes= {'outbox':'Sends "tick_mesg" (def: True) after "delay" seconds unless interrupted first', 
               'signal':'Sends producerFinished if not interrupted else sends interruption message'}
    tick_mesg = True
    check_interval = None
    
    def __init__(self, delay, **kwargs):
        super(SingleTick, self).__init__(**kwargs)
        self.delay = delay
        if self.check_interval is None or self.check_interval > delay:
            self.check_interval = delay

    def main(self):
        delay_until = time.time() + self.delay
        remaining = self.delay
        while remaining > 0 and not self.dataReady('control'):
            if remaining < self.check_interval:
                self.pause(remaining)
            else:
                self.pause(self.check_interval)
            remaining = delay_until - time.time()

        if remaining <= 0:
            self.send(self.tick_mesg, 'outbox')
            self.send(producerFinished(self), 'signal')
        elif self.dataReady('control'):
            self.send(self.recv('control'), 'signal')


class PeriodicTick(Axon.ThreadedComponent.threadedcomponent):
    '''
    This threaded component will periodically (every "delay" seconds) send
    True out it's outbox.  You can specify an optional "check_interval" which
    will cause the component to more frequently check it's control inbox for
    termination signals.
    
    PeriodicTick(delay, check_interval=delay, tick_mesg=True)
    '''
    Inboxes = {'inbox':'ignored', 
               'control':'Sending a message here will cause the component to shutdown'}
    Outboxes= {'outbox':'Sends a "tick_mesg" (def: True) every "delay" seconds', 
               'signal':'Sends terminiation signal received on "control"'}
    tick_mesg = True
    check_interval = None
    
    def __init__(self, delay, **kwargs):
        super(PeriodicTick, self).__init__(**kwargs)
        self.delay = delay
        if self.check_interval is None or self.check_interval > delay:
            self.check_interval = delay

    def main(self):
        start_time = time.time()
        tick_count = 1
        while not self.dataReady('control'):
            delay_until = start_time + self.delay * tick_count
            remaining = delay_until - time.time()
            while remaining > 0 and not self.dataReady('control'):
                if remaining < self.check_interval:
                    self.pause(remaining)
                else:
                    self.pause(self.check_interval)
                remaining = delay_until - time.time()

            if remaining <= 0:
                self.send(self.tick_mesg, 'outbox')
                tick_count += 1
        self.send(self.recv('control'), 'signal')

