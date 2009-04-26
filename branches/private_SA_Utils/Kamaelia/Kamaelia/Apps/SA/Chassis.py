'''
This file contains some utility classes which are used by both the client and
server components of the port tester application.
'''

import time
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.IPC import serverShutdown

class TTL(Axon.Component.component):
    '''
    This "Time To Live" component is designed to wrap another existing component.
    The TTL starts an embedded SingleTick component which waits for "delay"
    seconds and then the TTL progressivly becomes more aggressive in its attempts
    to shutdown the wrapped component.  Ideally this component should not be
    needed, but it is handy for components that do not have their own timeout
    functionality.
    
    TTL(comp, delay)
    '''
    Inboxes = {'_trigger':'Receives True message to cause embedded component to shutdown'}
    Outboxes= {'_sigkill':'Dynamically links to a emedded component control',
               '_disarm':'Stop timebomb early'}
    
    def __init__(self, comp, delay):
        # One of the rare cases where we do not call the parent class' init()
        # right off the bat.  Instead we first replicate the wrapped component's
        # inboxes and outboxes.  Private "_name" boxes are not replicated.
        self.child = comp
        for inbox in (item for item in self.child.Inboxes.iteritems() if not item[0].startswith('_')):
            self.Inboxes[inbox[0]] = inbox[1]
        for outbox in (item for item in self.child.Outboxes.iteritems() if not item[0].startswith('_')):
            self.Outboxes[outbox[0]] = outbox[1]

        super(TTL, self).__init__()

        self.timebomb = SingleTick(delay=delay, check_interval=1)

        # We can now create the mailbox linkages now that the parent class'
        # init() has been called.
        self.link((self.timebomb, 'outbox'), (self, '_trigger'))
        self.link((self, '_disarm'), (self.timebomb, 'control'))
        self.link((self, '_sigkill'), (self.child, 'control'))

        for inbox in (item for item in self.child.Inboxes.iteritems() if not item[0].startswith('_')):
            self.link((self, inbox[0]), (self.child, inbox[0]), passthrough=1)
 
        for outbox in (item for item in self.child.Outboxes.iteritems() if not item[0].startswith('_')):
            self.link((self.child, outbox[0]), (self, outbox[0]), passthrough=2)
        
        self.addChildren(self.child)
    
    def main(self):
        self.timebomb.activate()
        self.child.activate()
        yield 1
        while not (self.child._isStopped() or (self.dataReady('_trigger') and self.recv('_trigger') is True)):
            self.pause()
            yield 1
        if not self.timebomb._isStopped():
            self.send(producerFinished(), '_disarm')
        if not self.child._isStopped():
            self.send(producerFinished(), '_sigkill')
            yield 1
            yield 1
            if not self.child._isStopped():
                self.send(shutdownMicroprocess(), '_sigkill')
                yield 1
                yield 1
                if not self.child._isStopped():
                    self.send(serverShutdown(), '_sigkill')
                    yield 1
                    yield 1
                    if not self.child._isStopped():
                        self.send(shutdown(), '_sigkill')
                        yield 1
                        yield 1
        self.removeChild(self.child)
        yield 1
        if not self.child._isStopped():
            self.child.stop()
            yield 1
            if 'signal' in self.Outboxes:
                self.send(shutdownMicroprocess(), 'signal')
                yield 1
