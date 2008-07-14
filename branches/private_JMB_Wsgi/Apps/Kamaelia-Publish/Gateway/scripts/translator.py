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
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline

from headstock.api.im import Message, Body, Event
from headstock.lib.utils import generate_unique

import base64
from xml.sax.saxutils import escape, unescape

import simplejson

class requestToMessageTranslator(component):
    """Note that sending messages via XMPP is considered outbound.  This converts
    an HTTP request object into a headstock message.""" 
    ThisJID = 'amnorvend_gateway@jabber.org'
    ToJID = 'amnorvend@gmail.com'
    def __init__(self, request, **argd):
        super(requestToMessageTranslator, self).__init__(**argd)
        self.request = request
        self.signal = None
        
    def main(self):
        serialize = simplejson.dumps(self.request)
        serialize = escape(serialize)   #make the data suitable for transmission via XML
        
        hMessage = Message(unicode(self.ThisJID), unicode(self.ToJID),
                           type=u'chat', stanza_id=generate_unique())
        
        hMessage.bodies.append(Body(serialize))
        
        self.send(hMessage, 'outbox')
        
        m = Message(unicode(self.ThisJID), unicode(self.ToJID), 
                    type=u'chat', stanza_id=generate_unique())
        
        self.send(m, "outbox")
        
        yield 1
        
        while not self.signal:
            for msg in self.Inbox('control'):
                self.handleControlBox(msg)
            
            for msg in self.Inbox('inbox'):
                self.handleInbox(msg)
                
            if not self.signal and self.anyReady():
                self.pause()
                
            yield 1
            
        self.send(self.signal, 'signal')
    
    def handleInbox(self, msg):
        chunk = {
            'data' : escape(msg)
        }
        serialize = simplejson.dumps(chunk)
        
        #hMessage being a headstock message
        hMessage = Message(unicode(self.ThisJID), unicode(self.ToJID),
                           type=u'chat', stanza_id=generate_unique())
        
        hMessage.event = Event.composing
        hMessage.bodies.append(unicode(Body(serialize)))
        self.send(hMessage, 'outbox')
        
        # Right after we sent the first message
        # we send another one reseting the event status
        m = Message(unicode(self.ThisJID), unicode(self.ToJID), 
                    type=u'chat', stanza_id=generate_unique())
        
        self.send(m, "outbox")
    
    def handleControlBox(self, msg):
        if isinstance(msg, (shutdownMicroprocess, producerFinished)):
            self.signal = msg           
            
class messageToResponseTranslator(component):
    ThisJID = 'amnorvend_gateway@jabber.org'
    ToJID = 'amnorvend@gmail.com'
    def __init__(self, **argd):
        super(messageToResponseTranslator, self).__init__(**argd)
        self.signal = None
        
    def main(self):
        self.not_done = True
        while not self.signal:
            [self.handleControlBox(msg) for msg in self.Inbox('control')]
            [self.handleInbox(msg) for msg in self.Inbox('inbox')]
            
            if not self.anyReady() and not self.signal:
                self.pause()
                
            yield 1
            
        self.send(self.signal, 'signal')
        
    def handleInbox(self, msg):
        deserialize = ''.join([str(body) for body in msg.bodies])
        
        #Sometimes an emty message comes through to reset the event status.  This
        #will cause errors if we process it.
        if deserialize:
            deserialize = unescape(deserialize) #FIXME:  This is a security issue:  Will also escape escaped HTML.
            resource = simplejson.loads(deserialize)
            
            assert(isinstance(resource, dict))
            self.send(resource, 'outbox')
        
    def handleControlBox(self, msg):
        if isinstance(msg, (shutdownMicroprocess, producerFinished)):
            self.signal = msg
            
def Translator(ThisJID='amnorvend_gateway@jabber.org', ToJID='amnorvend@gmail.com'):
    pass

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    class Producer(component):            
        def main(self):
            self.send('foo')
            yield 1
            self.send(producerFinished(self), 'signal')
            
    request={
        'a' : 'b',
        'c' : 'd',
        'e' : 'f',
    }
    Pipeline(Producer(), requestToMessageTranslator(request), messageToResponseTranslator(), ConsoleEchoer()).run()
    print '\n'
