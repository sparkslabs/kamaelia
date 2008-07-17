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
from Axon.idGen import numId
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import PublishTo

from headstock.api.im import Message, Body, Event, Thread
from headstock.api.jid import JID
from headstock.lib.utils import generate_unique

import base64
from xml.sax.saxutils import escape, unescape

import simplejson

from gate import OutboxBundle, BPLANE_NAME, InitialMessage

class requestToMessageTranslator(component):
    """Note that sending messages via XMPP is considered outbound.  This converts
    an HTTP request object into a headstock message.""" 
    Inboxes = {'inbox' : 'Receive messages from the HTTPServer',
               'control' : 'Receive signals from the HTTPServer'}
    Outboxes = {'outbox' : 'Send messages to the Interface',
                'signal' : 'Send signals',
                'publisher_signal' : 'send signals to the publisher',}
    
    ThisJID = u'amnorvend_gateway@jabber.org'
    ToJID = u'amnorvend@jabber.org'
    bundle = OutboxBundle()
    def __init__(self, request, **argd):
        super(requestToMessageTranslator, self).__init__(**argd)
        self.request = request
        self.signal = None
        self.batch_id = unicode(numId())
        self.Publisher = PublishTo(BPLANE_NAME)
        self.link((self, 'outbox'), (self.Publisher, 'inbox'))
        
        if not isinstance(self.ToJID, unicode):
            self.ToJID = unicode(self.ToJID)
        if not isinstance(self.ThisJID, unicode):
            self.ThisJID = unicode(self.ThisJID)
        
    def main(self):
        self.Publisher.activate()        
        self.sendInitialMessage(self.request)
        
        yield 1
        
        while not self.signal:
            for msg in self.Inbox('control'):
                self.handleControlBox(msg)
            
            for msg in self.Inbox('inbox'):
                self.handleInbox(msg)
                
            if not self.signal and not self.anyReady():
                self.pause()
                
            yield 1
            
        self.send(self.signal, 'signal')
        self.send(self.signal, 'publisher_signal')
        
        signal_msg = {'signal' : type(self.signal).__name__}
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
        request['batch'] = self.batch_id
        
        hMessage = self.makeMessage(request)
        out = InitialMessage(hMessage=hMessage,
                             bundle=self.bundle, batch_id=self.batch_id)
        
        self.send(out, 'outbox')
        
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
        
class messageToResponseTranslator(component):
    ThisJID = 'amnorvend_gateway@jabber.org'
    ToJID = 'amnorvend@jabber.org/gateway'
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
        if isinstance(msg, (producerFinished, shutdownMicroprocess)):
            self.signal = msg
            
            
def appendTID(msg, thread_id):
    tobj = Thread(thread_id)
    msg.thread = tobj
            
def Translator(request, mtr=None, rtm=None):
    if not mtr:
        mtr = messageToResponseTranslator()
    if not rtm:
        rtm = requestToMessageTranslator(request=request)
        
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
            ('rtm', 'signal') : ('self', 'xmpp_signal')
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
