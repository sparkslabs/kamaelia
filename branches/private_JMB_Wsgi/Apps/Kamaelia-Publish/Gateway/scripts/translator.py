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
from Kamaelia.Chassis.Graphline import Graphline

from headstock.api.im import Message, Body, Event
from headstock.lib.utils import generate_unique

import pickle as pickle
import base64

class requestToMessageTranslator(component):
    """Note that sending messages via XMPP is considered outbound.  This converts
    an HTTP request object into a headstock message."""
    ThisJID = 'amnorvend_gateway@jabber.org'
    ToJID = 'amnorvend@gmail.com'
    def __init__(self, **argd):
        super(requestToMessageTranslator, self).__init__(**argd)
        self.not_done=True
        
    def main(self):
        while self.not_done:
            [self.handleInbox(msg) for msg in self.Inbox('inbox')]
            [self.handleControlBox(msg) for msg in self.Inbox('control')]
            
            if not self.anyReady() and self.not_done:
                self.pause()
                
            yield 1
    
    def handleInbox(self, msg):
        assert(isinstance(msg, dict))
        serial = pickle.dumps(msg)
        serial = base64.encodestring(serial)
        
        
        #hMessage being a headstock message
        hMessage = Message(unicode(self.ThisJID), unicode(self.ToJID),
                           type=u'chat', stanza_id=generate_unique())
        
        hMessage.event = Event.composing
        hMessage.bodies.append(unicode(Body(serial)))
        self.send(hMessage, 'outbox')
        
        # Right after we sent the first message
        # we send another one reseting the event status
        m = Message(unicode(self.ThisJID), unicode(self.ToJID), 
                    type=u'chat', stanza_id=generate_unique())
        self.send(m, "outbox")
    
    def handleControlBox(self, msg):
        if isinstance(msg, shutdownMicroprocess):
            self.not_done = False
            self.send(msg, 'signal')
            
            
class messageToResponseTranslator(component):
    ThisJID = 'amnorvend_gateway@jabber.org'
    ToJID = 'amnorvend@gmail.com'
    def __init__(self, **argd):
        super(messageToResponseTranslator, self).__init__(**argd)
        
    def main(self):
        self.not_done = True
        while self.not_done:
            [self.handleInbox(msg) for msg in self.Inbox('inbox')]
            [self.handleControlBox(msg) for msg in self.Inbox('control')]
            
            if not self.anyReady() and self.not_done:
                self.pause()
                
            yield 1
    
    def handleInbox(self, msg):
        serial = ''.join([str(body) for body in msg.bodies])
        
        #Sometimes an emty message comes through to reset the event status.  This
        #will cause errors if we process it.
        if serial:
            serial = base64.b64decode(str(serial))
            resource = pickle.loads(serial)
    
            assert(isinstance(resource, dict))
            self.send(resource, 'outbox')
        
    def handleControlBox(self, msg):
        if isinstance(msg, shutdownMicroprocess):
            self.not_done = False
            self.send(msg, 'signal')

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    class Producer(component):
        Request = {'a' : 'b',
                   'c' : 'd',
                   'e' : 'f',}
        def __init__(self, **argd):
            super(Producer, self).__init__(**argd)
            
        def main(self):
            self.send(self.Request, 'outbox')
            yield 1
            self.send(shutdownMicroprocess(self), 'signal')
            
    Pipeline(Producer(), requestToMessageTranslator(), messageToResponseTranslator(), ConsoleEchoer()).run()
