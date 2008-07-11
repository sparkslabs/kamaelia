#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: JMB

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class ProxyManager(component):
    Inboxes = {'inbox' : 'receive new box bundles',
               'response' : 'receive incoming responses',
               'control' : 'receive shutdown signals'}
    Outboxes = {'outbox' : 'Send data received from the HTTPServer.',
                'signal' : 'send shutdown signals'}
    DebugMemory=False
    def __init__(self, **argd):
        super(ProxyManager, self).__init__(**argd)
        self.not_done = True
        
        #note that a box bundle should NOT ever get a reference to either of these
        #next two attributes.  That would create a circular reference.
        self.proxies = set()      #The bundles we're currently tracking
        self.ready_proxies = []    #The bundles that currently have messages waiting
        self.finished_proxies = []

    def main(self):
        """
        FIXME:  This will need to be reviewed for possible race conditions when
        dealing with threaded components.
        """                
        while self.not_done:
            for msg in self.Inbox('inbox'):
                self.handleMainInbox(msg)
                
            for msg in self.Inbox('control'):
                self.handleControlInbox(msg)
            
            finished_proxies=[]
            while len(self.ready_proxies) != 0:
                proxy = self.ready_proxies.pop(0)
                self.handleProxyInbox(proxy)
                if self.proxyDone(proxy):
                    finished_proxies.append(proxy)
                
            #Read each proxy's control box and check for any shutdown messages.
            #If any shutdown messages are received, unregister the proxy.
            for proxy in finished_proxies:
                self.unregisterProxy(proxy)
                
            if not self.anyReady() and self.not_done:
                self.pause()
                
            yield 1
            
    def handleMainInbox(self, msg):
        if isinstance(msg, component):
            self.registerProxy(msg)

    def handleControlInbox(self, msg):
        if isinstance(msg, shutdownMicroprocess):
            for bundle in self.box_bundles:
                bundle.unbind()
            self.not_done = False

    def handleProxyInbox(self, proxy):
        for msg in proxy.Inbox('inbox'):
            self.send(msg, )
    
    def proxyDone(self, proxy):
        for msg in proxy.Inbox('control'):
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                self.not_done = False    
                return True
            
        return False
    
    def registerProxy(self, proxy):
        try:
            proxy.bind(self.unpause, self.setReady)
            self.proxies.add(proxy)
        except AttributeError:
            raise AttributeError('The component that was registered does not appear to be a valid box bundle')

    def unregisterProxy(self, proxy):
        proxy.unbind()
        self.proxies.discard(proxy)

    def setReady(self, proxy):
        self.ready_proxies.append(proxy)


class Proxy(component):
    """This component is not meant to be activated.  Use it instead as a bundle of
    boxes."""
    # The ParentUnpause attribute is used to notify the component that uses this
    #bundle that it has a new message.
    ParentUnpause=None
    
    #The ParentSet is used to keep a list of the components that have messages
    #waiting.  This way it doesn't have to check each and every component it
    #manages for messages waiting.
    ParentAddMethod = None
    def __init__(self, **argd):
        super(Proxy, self).__init__(**argd)
        if self.ParentUnpause and self.ParentSet:
            self.bound = True
        else:
            self.bound = False
        
    def unpause(self):
        if self.bound:
            #print 'Calling ParentUnpause: %s' % (self.ParentUnpause)
            self.ParentUnpause()
            self.ParentAddMethod(self)
        else:
            print 'unpause called, but bundle not bound!'
        
    def unbind(self):
        self.bound = False
        self.ParentUnpause=None
        self.ParentAddMethod = None
        
    def bind(self, parent_unpause, parent_add_method):
        self.bound = True
        self.ParentUnpause = parent_unpause
        self.ParentAddMethod = parent_add_method
        
    def activate(self, *argv, **argd):
        pass
    
    def run(self):
        pass
        
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    
    class Producer(component):
        def __init__(self, msg):
            self.msg = msg
            super(Producer, self).__init__()
        def main(self):
            for i in range(50):
                yield 1
                self.send(self.msg)
            import sys
            sys.exit(0)
    
    pm = ProxyManager()
    pro1 = Producer('Hello from Producer 1\n')
    pro2 = Producer('Hello from Producer 2\n')
    cons = ConsoleEchoer()
    
    proxy1 = Proxy()
    proxy2 = Proxy()
    
    pm.registerProxy(proxy1)
    proxy_sender = component()
    proxy_sender.link((proxy_sender, 'outbox'), (pm, 'inbox'))
    proxy_sender.send(proxy2, 'outbox')
    
    pro1.link((pro1, 'outbox'), (proxy1, 'inbox'))
    pro2.link((pro2, 'outbox'), (proxy2, 'inbox'))
    pm.link((pm, 'outbox'), (cons, 'inbox'))
    
    pro1.activate()
    pro2.activate()
    cons.activate()
    pm.run()
