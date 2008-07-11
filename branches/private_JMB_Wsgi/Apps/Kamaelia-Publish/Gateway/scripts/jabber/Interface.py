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
import gc

class XMPPInterface(component):
    Inboxes = {'inbox' : 'receive new box bundles',
               'response' : 'receive incoming responses',
               'control' : 'receive shutdown signals'}
    Outboxes = {'outbox' : 'Send data received from the HTTPServer.',
                'signal' : 'send shutdown signals'}
    DebugMemory=False
    def __init__(self, **argd):
        super(XMPPInterface, self).__init__(**argd)
        self.not_done = True
        
        #note that a box bundle should NOT ever get a reference to either of these
        #next two attributes.  That would create a circular reference.
        self.box_bundles = set()      #The bundles we're currently tracking
        self.ready_bundles = set()    #The bundles that currently have messages waiting
        self.marked_bundles = set()
                
    def main(self):
        """
        FIXME:  This will need to be reviewed for possible race conditions when
        dealing with threaded components.
        """        
        self.send(producerFinished(self), 'signal')
        
        while self.not_done:
            [self.handleMainInbox(msg) for msg in self.Inbox('inbox')]
            [self.handleControlInbox(msg) for msg in self.Inbox('control')]
            
            buffer = self.ready_bundles
            self.ready_bundles = set()
            for bundle in buffer:
                self.handleBoxBundleInbox(bundle)
                self.handleBoxBundleControl(bundle)
            
            if self.marked_bundles:    
                self.clearMarkedBundles()
                
            if not self.anyReady() and self.not_done:
                self.pause()
                
            yield 1
            
        #print 'dying!'
            
    def handleMainInbox(self, msg):
        if isinstance(msg, component):
            self.registerBundle(msg)
            

            
    def handleControlInbox(self, msg):
        if isinstance(msg, shutdownMicroprocess):
            for bundle in self.box_bundles:
                bundle.unbind()
            self.not_done = False
            
    def handleBoxBundleInbox(self, bundle):
        pass
    
    def handleBoxBundleControl(self, bundle):
        for msg in bundle.Inbox('control'):
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                self.marked_bundles.add(bundle)
                
        #print bundle, ' marked for removal.'
                
    def clearMarkedBundles(self):
        #print 'Purging marked bundles.'
        [self.unregisterBundle(bundle) for bundle in self.marked_bundles]
        self.marked_bundles.clear()
        
        #print 'box_bundles:\n', self.box_bundles
        
        if self.DebugMemory:
            gc.collect()
            if gc.garbage:
                print '='*6, 'GARBAGE FOUND', '='*6
                print gc.garbage
                
    def anyReady(self):
        if super(XMPPInterface, self).anyReady() or self.ready_bundles:
            return True
        else:
            return False
    
    def registerBundle(self, bundle):
        try:
            if bundle.bound:
                bundle.unbind()
                
            bundle.bind(self.unpause, self.setReady)
            self.box_bundles.add(bundle)
            
            #print msg, ' added.'
            #print 'box_bundles:\n', self.box_bundles,
        except AttributeError:
            raise AttributeError('The component that was registered does not appear to be a valid box bundle')
        
    def unregisterBundle(self, bundle):
        bundle.unbind()
        self.box_bundles.discard(bundle)
        
    def setReady(self, bundle):
        self.ready_bundles.add(bundle)
        
class BoxBundle(component):
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
        super(BoxBundle, self).__init__(**argd)
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
        
    def activate(self, scheduler=None, tracker=None, mainmethod='main'):
        pass
    
    def run(self):
        pass
        
if __name__ == '__main__':
    xmpp = XMPPInterface()
    bundle = BoxBundle()
    xmpp.registerBundle(bundle)
    
    xmpp.link((xmpp, 'signal'), (bundle, 'control'))
    
    xmpp.run()
