'''
This file contains some utility classes which are used by both the client and
server components of the port tester application.
'''

import time
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.IPC import serverShutdown

# FIXME: Needs example of usage.

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
        
        # FIXME: This assumes that <component>.Inboxes is always a
        # FIXME: dictionary. It isn't. It's required to be any iterable that
        # FIXME: returns strings - because self.Inbox is iterated over as:
        # FIXME:
        # FIXME:    for boxname in <component>.Inboxes:
        # FIXME: 
        # FIXME: The reason many components use dictionaries these days is
        # FIXME: because of the recognition that doing the above with
        # FIXME: dictionaries gives you keys, the values can then be docs
                
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
    
    # FIXME: Really a fixme for Axon, but it strikes me (MPS) that what a
    # FIXME: huge chunk of this code is crying out for really is a way of
    # FIXME: killing components. Until that happens, this is pretty good,
    # FIXME: but we can go a stage further here and add in sabotaging the
    # FIXME: components methods as well to force it to crash if all else
    # FIXME: fails (!) (akin to using ctypes to force a stack trace in
    # FIXME: python(!))
    
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
