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
'''
This file contains some utility classes which are used by both the client and
server components of the port tester application.
'''

import time
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.IPC import serverShutdown

from Kamaelia.Apps.SA.Time import SingleTick

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
                
        for inbox in (item for item in self.child.Inboxes if not item.startswith('_')):
            try:
                self.Inboxes[inbox] = self.child.Inboxes.get(inbox, "")
            except AttributeError: # not a dict
                self.Inboxes[inbox] = ""

        for outbox in (item for item in self.child.Outboxes if not item.startswith('_')):
            try:
                self.Outboxes[outbox] = self.child.Outboxes.get(outbox, "")
            except AttributeError: # not a dict
                self.Outboxes[outbox] = ""

        super(TTL, self).__init__()

        self.timebomb = SingleTick(delay=delay, check_interval=1)

        # We can now create the mailbox linkages now that the parent class'
        # init() has been called.
        
        self.link((self.timebomb, 'outbox'), (self, '_trigger'))
        self.link((self, '_disarm'), (self.timebomb, 'control'))
        try:
            self.link((self, '_sigkill'), (self.child, 'control'))
            self.nochildcontrol = False
        except KeyError:
            self.nochildcontrol = True

        for inbox in (item for item in self.child.Inboxes if not item.startswith('_')):
            self.link((self, inbox), (self.child, inbox), passthrough=1)

        for outbox in (item for item in self.child.Outboxes if not item.startswith('_')):
            self.link((self.child, outbox), (self, outbox), passthrough=2)

        
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
        
        shutdown_messages = [ producerFinished(), shutdownMicroprocess(), serverShutdown(), shutdown() ]
        for msg in shutdown_messages:
            if not self.child._isStopped():
                self.send( msg, "_sigkill")
                yield 1
                yield 1
            else:
                break
             
        self.removeChild(self.child)
        yield 1
        if not self.child._isStopped():
            self.child.stop()
            yield 1
            if 'signal' in self.Outboxes:
                self.send(shutdownMicroprocess(), 'signal')
                yield 1


if __name__=="__main__":
    class WellBehaved1(Axon.Component.component):
        def main(self):
            t = time.time()
            while not self.dataReady("control"):
                if time.time() - t>0.3:
                    self.send("hello", "outbox")
                    print (self)
                    t = time.time()
                yield 1
            self.send(self.recv("control"), "signal")
    
    TTL( WellBehaved1(), 1 ).run()

    class WellBehaved2(Axon.Component.component):
        Inboxes = {
            "inbox"   : "Foo Bar",
            "control" : "Foo Bar",
        }
        Outboxes = {
            "outbox" : "Foo Bar",
            "signal" : "Foo Bar",
        }
        def main(self):
            t = time.time()
            while not self.dataReady("control"):
                if time.time() - t>0.3:
                    self.send("hello", "outbox")
                    print (self)
                    t = time.time()
                yield 1
            self.send(self.recv("control"), "signal")
    
    TTL( WellBehaved2(), 1 ).run()

    class WellBehaved3(Axon.Component.component):
        Inboxes = [ "inbox", "control" ]
        Outboxes = [ "outbox", "signal" ]
        def main(self):
            t = time.time()
            while not self.dataReady("control"):
                if time.time() - t>0.3:
                    self.send("hello", "outbox")
                    print (self)
                    t = time.time()
                yield 1
            self.send(self.recv("control"), "signal")
    
    TTL( WellBehaved3(), 1 ).run()

    class WellBehaved4(Axon.Component.component):
        Inboxes = [ "inbox", "control" ]
        Outboxes = {
            "outbox" : "Foo Bar",
            "signal" : "Foo Bar",
        }
        def main(self):
            t = time.time()
            while not self.dataReady("control"):
                if time.time() - t>0.3:
                    self.send("hello", "outbox")
                    print (self)
                    t = time.time()
                yield 1
            self.send(self.recv("control"), "signal")
    
    TTL( WellBehaved4(), 1 ).run()
    
    class BadlyBehaved1(Axon.Component.component):
        Inboxes = [ ]
        Outboxes = [ ]
        def main(self):
            t = time.time()
            while 1:
                if time.time() - t>0.3:
                    print (self)
                    t = time.time()
                yield 1
    
    TTL( BadlyBehaved1(), 1 ).run()
