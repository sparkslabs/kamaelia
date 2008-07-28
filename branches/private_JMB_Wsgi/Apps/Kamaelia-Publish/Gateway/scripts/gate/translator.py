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
from Axon.Ipc import producerFinished, shutdownMicroprocess, internalNotify
from Axon.idGen import numId
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import PublishTo
from Kamaelia.Protocol.HTTP.ErrorPages import getErrorPage
from Kamaelia.IPC import LookupByText

from headstock.api.im import Message, Body, Event, Thread
from headstock.api.jid import JID
from headstock.lib.utils import generate_unique

import base64
from xml.sax.saxutils import escape, unescape

import simplejson

from gate import OutboxBundle, BPLANE_NAME, InitialMessage
from gate.JIDLookup import ExtractJID

class RequestSerializer(component):
    """Note that sending messages via XMPP is considered outbound.  This converts
    an HTTP request object into a headstock message.""" 
    Inboxes = {'inbox' : 'Receive messages from the HTTPServer',
               'control' : 'Receive signals from the HTTPServer'}
    Outboxes = {'outbox' : 'Send messages to the Interface',
                'signal' : 'Send signals',
                'publisher_signal' : 'send signals to the publisher',
                'response_signal' : 'send internal signals to the response deserializer'}
    
    ThisJID = u'amnorvend_gateway@jabber.org'    
    def __init__(self, request, **argd):
        super(RequestSerializer, self).__init__(**argd)
        self.request = request
        self.signal = None
        self.batch_id = unicode(numId())
        self.Publisher = PublishTo(BPLANE_NAME)
        self.link((self, 'outbox'), (self.Publisher, 'inbox'))
        self.link((self, 'signal'), (self.Publisher, 'control'))
        
        if not isinstance(self.ThisJID, unicode):
            self.ThisJID = unicode(self.ThisJID)
        
        self.bundle = OutboxBundle()
        
        #The following is used to indicate that we should send a signal to the serving
        #client. Sometimes we want to disable this, like if a serving client isn't
        #found or is unavailable.
        self._send_xmpp_signal = True
        
    def main(self):
        self.Publisher.activate()
        self.ToJID = ExtractJID(self.request)
        if self.ToJID:
            self.sendInitialMessage(self.request)
        else:
            self.JIDNotFound()
        
        #Note that self.signal is set in the methods 'JIDNotFound' and 'handleControlBox'
        #if JIDNotFound is run, this loop will not run.
        while not self.signal:
            for msg in self.Inbox('control'):
                self.handleControlBox(msg)
            
            for msg in self.Inbox('inbox'):
                self.handleInbox(msg)
                
            if not self.signal and not self.anyReady():
                self.pause()
                
            yield 1
            
        self.send(self.signal, 'signal')
        
        if self._send_xmpp_signal:
            signal_msg = {'signal' : type(self.signal).__name__,
                          'batch' : self.batch_id}
            self.sendMessage(signal_msg)
    
    def handleInbox(self, msg):
        chunk = {
            'body' : escape(msg),
            'batch' : self.batch_id,
        }
        self.sendMessage(chunk)
    
    def handleControlBox(self, msg):
        if isinstance(msg, (shutdownMicroprocess, producerFinished)):
            self.signal = msg
            
    def sendInitialMessage(self, request):
        print '='*6, 'REQUEST', '='*6, '\n'
        print request
        
        request['batch'] = self.batch_id
        
        hMessage = self.makeMessage(request)
        out = InitialMessage(hMessage=hMessage,
                             bundle=self.bundle, batch_id=self.batch_id)
        
        self.send(out, 'outbox')
        print '='*6, 'REQUEST', '='*6, '\n'
        print request
        
    def JIDNotFound(self):
        resource = getErrorPage(404, 'Could not find %s' % (self.request['REQUEST_URI']))
        out = internalNotify(message=resource)    #Prevents the loop from running.
        self.send(out, 'response_signal')
        self.signal = shutdownMicroprocess()
        self._send_xmpp_signal = False
        
    def makeMessage(self, serializable):
        hMessage = Message(self.ThisJID, self.ToJID,
                           type=u'chat', stanza_id=generate_unique())
            
        body = simplejson.dumps(serializable)
        body = escape(body)
        body = unicode(body)
        hMessage.bodies.append(Body(body))
        
        hMessage.thread = Thread(self.batch_id)
        
        return hMessage
    
    def sendMessage(self, serializable):
        self.send(self.makeMessage(serializable), 'outbox')
        
class ResponseDeserializer(component):
    Inboxes = {'inbox' : 'Receive responses to deserialize',
               'control' : 'Receive shutdown signals',
               'response_control' : 'Receive signals indicating an error of some kind'}
    Outboxes = {'outbox' : 'Send deserialized responses',
                'signal' : 'Forward shutdown signals'}
    
    ThisJID = 'amnorvend_gateway@jabber.org'
    ToJID = 'amnorvend@jabber.org/gateway'
    def __init__(self, **argd):
        super(ResponseDeserializer, self).__init__(**argd)
        self.signal = None
        
    def main(self):
        self.not_done = True
        while not self.signal:
            [self.handleControlBox(msg) for msg in self.Inbox('control')]
            [self.handleResponseControl(msg) for msg in self.Inbox('response_control')]
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
            
            signal = resource.get('signal')
            if signal:
                self.signal = LookupByText(signal)(self)
            
            assert(isinstance(resource, dict))
            self.send(resource, 'outbox')
        
    def handleControlBox(self, msg):
        if isinstance(msg, (producerFinished, shutdownMicroprocess)):
            self.signal = msg
            
    def handleResponseControl(self, msg):
        if isinstance(msg, internalNotify):
            resource = msg.message
            self.send(resource, 'outbox')
            self.signal = producerFinished(self)
            
            
def Translator(request, mtr=None, rtm=None):
    if not mtr:
        mtr = ResponseDeserializer()
    if not rtm:
        rtm = RequestSerializer(request=request)
        
    trans = Graphline(
        mtr=mtr,
        rtm=rtm,
        linkages={
            #These are the boxes that the HTTPServer will use
            ('self', 'inbox') : ('rtm', 'inbox'),
            ('mtr', 'outbox') : ('self', 'outbox'),
                
            #These are the boxes that the XMPP Handler will use.
            ('self', 'xmpp_in') : ('mtr', 'inbox'),
                
            #This is the shutdown handling
            ('self', 'control') : ('rtm', 'control'),
            ('self', 'xmpp_control') : ('mtr', 'control'),
            ('mtr', 'signal') : ('self', 'signal'),
            ('rtm', 'response_signal') : ('mtr', 'response_control'),
        }
    )
    
    #prepare the outbox bundle so that it may be sent to the interface
    rtm.bundle.link((rtm.bundle, 'outbox'), (trans, 'xmpp_in'))
    rtm.bundle.link((rtm.bundle, 'signal'), (trans, 'xmpp_control'))
    
    return trans

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    class Server(component):
        def main(self):
            self.send('foo')
            yield 1
            self.send(producerFinished(self), 'signal')
            yield 1
            signal = None
            while not signal:
                for msg in self.Inbox('control'):
                    if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                        signal = msg
                        print 'Server received:\n', repr(msg)
                        
                for msg in self.Inbox('inbox'):
                    print 'Server received:\n', repr(msg)
                    
                if not (signal or self.anyReady()):
                    self.pause()
                    
                yield 1
            
            
            
    class Client(component):
        def main(self):
            signal = None
            while not signal:
                for msg in self.Inbox('control'):
                    if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                        signal = msg
                        print 'Client received:\n', repr(msg)
                        
                for msg in self.Inbox('inbox'):
                    print 'Client received:\n', repr(msg)
                    self.send(msg, 'outbox')
                    
                if not (signal or self.anyReady()):
                    self.pause()
                    
                yield 1
                
            self.send(signal, 'signal')
            
    request={
        'a' : 'b',
        'c' : 'd',
        'e' : 'f',
    }
    Graphline(
        server=Server(),
        trans=Translator(request),
        client=Client(),
        
        linkages={
            #server
            ('server', 'outbox') : ('trans', 'inbox'),
            ('trans', 'outbox') : ('server', 'inbox'),
                
            #client
            ('client', 'outbox') : ('trans', 'xmpp_in'),
            ('trans', 'xmpp_out') : ('client', 'inbox'),
                
            #shutdown handling
            ('client', 'signal') : ('trans', 'xmpp_control'),
            ('server', 'signal') : ('trans', 'control'),
            ('trans', 'signal') : ('server', 'control'),
            ('trans', 'xmpp_signal') : ('client', 'control')
        }
    ).run()
    print '\n'
