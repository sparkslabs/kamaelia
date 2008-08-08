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
"""
Translators are designed to take a request from the HTTP server (using the
WSGILikeTranslator) and turn it into a message that can be sent out via headstock.
It also takes a message from headstock and turns it into a response that can be
sent out by the HTTPServer.

There are two components to a translator:  a RequestSerializer and a
ResponseDeserializer.  The RequestSerializer takes the incoming HTTP request and
turns it into a form that can be sent to the peer.  The ResponseDeserializer takes
a message from the Peer and turns it into a form that can be sent to the page
requester by the HTTPServer.

The system is also made to connect to a pair of backplanes (via a PublishTo component
of course).  The first backplane that it connects to will connect to the interface's
inbox.  This is used for a translator to register itself with the interface (so
it can receive notifications when the peer has sent a message back) as well as to
send the interface messages to be sent out to the peer.  The second backplane is
used to connect to the interface's control inbox.  This is used to notify the interface
that the translator is no longer active.

You probably don't need to instantiate either the RequestSerializer or
ResponseDeserializer directly.  However, you may also swap them out for other
components with the same interface if you so desire.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, internalNotify
from Axon.idGen import numId
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import PublishTo
from Kamaelia.Protocol.HTTP.ErrorPages import getErrorPage
from Kamaelia.IPC import LookupByText, userLoggedOut, batchDone, newBatch
from Kamaelia.Apps.Wsgi.Console import info, debug, warning

from headstock.api.im import Message, Body, Event, Thread
from headstock.api.jid import JID
from headstock.lib.utils import generate_unique

import base64, weakref
from xml.sax.saxutils import escape, unescape
import zlib
from pprint import pformat

import simplejson

from gate import BPLANE_NAME, BPLANE_SIGNAL
from gate.JIDLookup import ExtractJID

_logger_suffix='.publish.gateway.translator'

class RequestSerializer(component):
    """Note that sending messages via XMPP is considered outbound.  This converts
    an HTTP request object into a headstock message.""" 
    Inboxes = {'inbox' : 'Receive messages from the HTTPServer',
               'control' : 'Receive signals from the HTTPServer'}
    Outboxes = {'outbox' : 'Send messages to the Interface',
                'signal' : 'Send signals',}
    
    ThisJID = u'amnorvend_gateway@jabber.org'    
    def __init__(self, request, batch_id, **argd):
        super(RequestSerializer, self).__init__(**argd)
        self.request = request
        self.signal = None
        self.batch_id = batch_id
        self.request['batch'] = self.batch_id
        
        if not isinstance(self.ThisJID, unicode):
            self.ThisJID = unicode(self.ThisJID)
        
        self.bundle = None
        
    def main(self):
        self.ToJID = ExtractJID(self.request)
        info('request for [%s], batch %s', _logger_suffix, self.request['REQUEST_URI'], self.batch_id)
        
        if self.ToJID:
            self.sendRegisterSignal()
            yield 1 # give the register signal time to get to the interface
            self.sendMessage(self.request)
            debug('User found.  Initial message sent for batch %s.', _logger_suffix, self.batch_id)
        else:
            #FIXME:  Note that sometimes the gateway won't receive a message when
            #it first logs in that a user is available.  It's really better to double
            #check with the server to get the user's status before assuming that
            #they are offline.
            self.JIDNotFound()
            debug('User not found for batch %s.', _logger_suffix, self.batch_id)
            return
        
        #Note that self.signal is set in handleControlBox
        while not self.signal:
            for msg in self.Inbox('control'):
                self.handleControlBox(msg)

            for msg in self.Inbox('inbox'):
                self.handleInbox(msg)
                
            if not self.signal and not self.anyReady():
                self.pause()
                
            yield 1
    
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
        
    def sendRegisterSignal(self):
        signal = newBatch(self.batch_id,
                          self.bundle(), #dereference the weakref
                          self.ToJID)
        self.send(signal, 'signal')
        
    def JIDNotFound(self):
        resource = getErrorPage(404, 'Could not find %s' % (self.request['REQUEST_URI']))
        out = internalNotify(message=resource)    #Prevents the loop from running.
        self.send(out, 'signal')
        
    def makeMessage(self, serializable):
        hMessage = Message(self.ThisJID, self.ToJID,
                           type=u'chat', stanza_id=generate_unique())
            
        body = simplejson.dumps(serializable)
        body = zlib.compress(body)
        body = base64.encodestring(body)
        body = unicode(body)
        hMessage.bodies.append(Body(body))
        
        hMessage.thread = Thread(self.batch_id)
        
        return hMessage
    
    def sendMessage(self, serializable):
        self.send(self.makeMessage(serializable), 'outbox')
        
class ResponseDeserializer(component):
    Inboxes = {'inbox' : 'Receive responses to deserialize',
               'control' : 'Receive shutdown signals',}
    Outboxes = {'outbox' : 'Send deserialized responses',
                'signal' : 'Forward shutdown signals to the HTTPServer',}
    def __init__(self, batch_id, **argd):
        super(ResponseDeserializer, self).__init__(**argd)
        self.signal = None
        self.batch_id = batch_id
        
    def main(self):
        self.not_done = True
        while not self.signal:
            [self.handleControlBox(msg) for msg in self.Inbox('control')]
            [self.handleInbox(msg) for msg in self.Inbox('inbox')]
            
            if not self.anyReady() and not self.signal:
                self.pause()
                
            yield 1
        if not isinstance(self.signal, internalNotify):
            self.send(self.signal, 'signal')
            self.send(batchDone(self.batch_id), 'signal')
        
    def handleInbox(self, msg):
        deserialize = ''.join([str(body) for body in msg.bodies])
        #Sometimes an emty message comes through to reset the event status.  This
        #will cause errors if we process it.
        if deserialize:
            deserialize = base64.decodestring(deserialize)
            deserialize = zlib.decompress(deserialize)
            resource = simplejson.loads(deserialize)
            
            debug('Translator %s received:\n%s' % (self.batch_id, resource),
                  _logger_suffix)
            
            signal = resource.get('signal')
            if signal:
                debug('Signal %s caught in batch %s.' % (signal, self.batch_id))
                self.signal = LookupByText(signal)(self)
                del resource['signal']
            if resource:
                self.send(resource, 'outbox')
        else:
            warning('deserialize empty', _logger_suffix)
    def handleControlBox(self, msg):
        if isinstance(msg, (producerFinished, shutdownMicroprocess)):
            self.signal = msg
        elif isinstance(msg, internalNotify):
            #The user was not found.
            resource = msg.message
            self.send(resource, 'outbox')
            self.send(producerFinished(self), 'signal')
            self.signal = msg
        elif isinstance(msg, userLoggedOut):
            #The user logged out mid-batch
            resource = getErrorPage(502, 'Batch %s terminated unexpectedly.' % (msg.thread))
            self.send(resource, 'outbox')
            self.signal = producerFinished(self)
            
class TranslatorController(component):
    Inboxes = {'inbox' : 'NOT USED',
               'control' : 'Receive signals from internal components',
               'interface_control' : 'Receive signals from the interface',}
    Outboxes = {'outbox' : 'NOT USED',
                'signal' : 'NOT USED',
                'interface_signal' : 'Send messages to the interface',
                'signal_publisher_in' : """Send shutdown messages to the
                                           in publisher""",
                'signal_publisher_signal' : """Send shutdown messages to
                                               the signal publisher""",
                'signal_serializer' : 'Send signals to the serializer',
                'signal_deserializer' : 'Send signals to the deserializer',
                'http_signal' : 'Send shutdown signals to the HTTPServer',}
    def main(self):
        self.signal = None
        while not self.signal:
            for msg in self.Inbox('control'):
                if isinstance(msg, internalNotify):
                    #Notify internal components that we're done.
                    #Note that no signal is sent out to the HTTP server or interface
                    #by this component.  The signal to the HTTP server will be sent
                    #by the deserializer and no message is necessary to the interface
                    #since it won't have started tracking the component yet.
                    self.sendSignals(msg)
                    self.signal = msg
                elif isinstance(msg, batchDone):
                    #This signals normal shutdown when everything is fine.  The
                    #interface and HTTP Server will both be notified.
                    self.sendSignals(signal=msg,
                                     interface_signal=msg,
                                     http_signal=producerFinished())
                    self.signal = msg
                elif isinstance(msg, shutdownMicroprocess):
                    #Not currently sent to this component by anything in Kamaelia
                    #Publish, but we do want to shut down when we receive this
                    #message.
                    self.sendSignals(msg, msg, msg)
                    self.signal = msg
                elif isinstance(msg, newBatch):
                    #This will go to the interface signaling that it should track
                    #a new batch.
                    self.send(msg, 'interface_signal')
                else:
                    warning('Unknown message %s received.  Ignoring' % (msg),
                            _logger_suffix)
            for msg in self.Inbox('interface_control'):
                if isinstance(msg, userLoggedOut):
                    #This message is from the interface notifying us that the user
                    #has logged out mid-batch.  No notification is necessary for
                    #the interface, since there the one that notified us.  The
                    #deserializer will send the message to the HTTP Server.
                    self.sendSignals(msg)
                    self.signal=msg
                else:
                    warning('Unknown message %s received.  Ignoring.' % (msg),
                            _logger_signal)
            for msg in self.Inbox('inbox'):
                pass #pop the messages so they won't keep unpausing this component
            
            if not self.signal and not self.anyReady():
                self.pause()
                
            yield 1
            
                
    def sendSignals(self, signal, interface_signal=None, http_signal=None):
        """This will send the specified signal to the signal serializer and deserializer
        and a producerFinished to the publishers."""
        self.send(signal, 'signal_serializer')
        self.send(signal, 'signal_deserializer')
        self.send(producerFinished(), 'signal_publisher_in')
        self.send(producerFinished(), 'signal_publisher_signal')
        if interface_signal:
            self.send(interface_signal, 'interface_signal')
        if http_signal:
            self.send(http_signal, 'http_signal')
            
def Translator(request, mtr=None, rtm=None):
    batch = unicode(numId())
    if not mtr:
        mtr = ResponseDeserializer(batch)
    if not rtm:
        rtm = RequestSerializer(request, batch)
        
    trans = Graphline(
        mtr=mtr,
        rtm=rtm,
        interface_in=PublishTo(BPLANE_NAME),
        interface_signal=PublishTo(BPLANE_SIGNAL),
        controller=TranslatorController(),
        linkages={
            #These are the boxes that the HTTPServer will use
            ('self', 'inbox') : ('rtm', 'inbox'),
            ('mtr', 'outbox') : ('self', 'outbox'),
                
            #These are the boxes that the XMPP Handler will use.
            ('self', 'xmpp_in') : ('mtr', 'inbox'),
            ('rtm', 'outbox') : ('interface_in', 'inbox'),
                
            #This is the shutdown handling
            #('self', 'control') : ('rtm', 'control'),
            #('self', 'xmpp_control') : ('mtr', 'response_control'),
            #('mtr', 'signal') : ('self', 'signal'),
            #('rtm', 'response_signal') : ('mtr', 'response_control'),
            ('rtm', 'signal') : ('controller', 'control'),
            ('mtr', 'signal') : ('self', 'signal'), #Will go to the HTTPServer
            ('controller', 'signal_serializer') : ('rtm', 'control'),
            ('controller', 'signal_deserializer') : ('mtr', 'control'),
            ('controller', 'http_signal') : ('self', 'signal'),
            ('controller', 'interface_signal') : ('interface_signal', 'inbox'),
            ('controller', 'signal_publisher_in') : ('interface_in', 'control'),
            ('controller', 'signal_publisher_signal') : ('interface_signal', 'control'),
            ('self', 'xmpp_control') : ('controller', 'interface_control')
        }
    )
    
    rtm.bundle = weakref.ref(trans) #use a weakref to prevent circular references
    
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
