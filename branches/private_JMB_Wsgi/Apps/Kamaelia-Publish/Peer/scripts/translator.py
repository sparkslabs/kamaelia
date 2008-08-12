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
"""
========================
Translator (Peer)
========================

Translators are designed to take a request from the HTTP server (using the
WSGILikeTranslator) and turn it into a message that can be sent out via headstock.
It also takes a message from headstock and turns it into a response that can be
sent out by the HTTPServer.

There are three subcomponents in a Translator: A RequestDeserializer, a
ResponseSerializer, and a TranslatorChassis.  The RequestDeserializer takes the incoming
HTTP request and turns it into a form that can be used by the handler.  The
ResponseSerializer takes a response by the Handler and turns it into a form that
can be sent to the Gateway.  The TranslatorChassis managesthe components and forwards
their messages to the TransactionManager.

These components will also create a handler, which will be responsible for generating
a Webpage that will be viewed by the person that sent the HTTP request to the Gateway.

How does it work?
------------------
The TransactionManager will create a new TranslatorChassis when it receives a new
incoming request.  The TranslatorChassis will create a new RequestDeserializer and
a ResponseSerializer, passing the initial request along to the RequestDeserializer.
Once the request has been translated, the TranslatorChassis will create the handler.
The RequestDeserializer will continue to forward body chunks on to the handler until
the Gateway signals that the body is done (using a producerFinished signal).  The
handler will forward its response to the ResponseSerializer, which will translate
the request to a form that may be sent over a network and then send the request out
to headstock.

You probably don't need to instantiate either the RequestDeserializer or
ResponseSerializer directly.  You should instead call the factory function
Translator, which will automatically create the components and link them.

What is crosstalk?
--------------------

Cross talk is a way of passing data back and forth between the gateway and the peer
It is basically a dictionary that roughly maps to a CGI environment-like dictionary
that has been serialized into JSON (using simplejson).  There are a few other fields
that may be in a crosstalk message.

- 'batch' is the "series" of messages a message is a part of.  Each HTTP request
and its associated response (together referred to as a "transaction") are assigned
a batch id.  This ID will be used to determine which "conversation" a message belongs
to.  This is the id that the interface will use to determine which translator to
send a message to.  The batch id also corresponds to the XMPP thread ID.

- 'signal' will be present to signal certain things.  Presently, it is used to
notify the peer when the gateway has transmitted the entire HTTP request (formatted
into crosstalk) and by the Peer to signal when the entire HTTP response has been
transmitted.

- 'body' will contain a chunk of the body or the body in its entirety.

The batch ID must be in all crosstalk messages while the signal and body fields may
be in the initial message, a separate message, or may not even be in the same message
(the Translator will currently send signal in a message by itself.)

For more info on CGI environment variables that may be present, see the following
webpage:  http://hoohoo.ncsa.uiuc.edu/cgi/env.html

In additon to the standard CGI variables, the following variable may also be present:

- 'NON_QUERY_URI' represents the URI without the query string.  For example, the
URI /a/b/c?d=e would give a NON_QUERY_URI of /a/b/c

What is JSON?
--------------
JSON may sound like an intimidating thing, but it's not.  It's a data serialization format
sort of like XML, only less verbose and simpler.  In fact, if you're reading this,
you're probably already familiar with a significant amount of its syntax.  For example,
you can do this at the python command line (assuming you have simplejson installed):

>>> import simplejson
>>> x = {'a' : 'b', 'c' : 'd', 'e' : 'f'}
>>> simplejson.dumps(x)
'{"a": "b", "c": "d", "e": "f"}'
>>> simplejson.dumps(y)
'["a", "b", "c", "d", "e", "f"]'
>>> z = {'a' : ['b', 'c', 'd', 'e'], 'f' : ['g', 'h', 'i', 'j']}
>>> simplejson.dumps(z)
'{"a": ["b", "c", "d", "e"], "f": ["g", "h", "i", "j"]}'


You'll notice that the formatting is almost identical to the way that Python prints
out string representation of basic objects.

What else will be done to the message?
--------------------------------------

The message will be gzipped to be smaller, and will then be base64 encoded to
prevent any text in the message from invalidating the XML that will be used by
XMPP.
"""
from Axon.Component import component
from Kamaelia.IPC import LookupByText, ToText
from Kamaelia.Apps.Web_common.Console import info

from xml.sax.saxutils import unescape, escape

from headstock.api.im import Message, Body, Thread
from headstock.lib.utils import generate_unique

import simplejson
import zlib, base64

class RequestDeserializer(component):
    Inboxes = {'inbox' : '',
               'control' : '',}
    Outboxes = {'outbox' : '',
                'initial' : 'send the initial output',
                'batch' : 'Output the batch id',
                'signal' : '',
                'chassis_signal' : '',}
    def __init__(self, message, **argd):
        super(RequestDeserializer, self).__init__(**argd)
        self.batch_id = None
        self.message = message
    
    def main(self):
        self.processInitialMessage()
        
        self.signal = None
        while not self.signal:
            for msg in self.Inbox('inbox'):
                msg = self.decodeMessage(msg)
                
                #signals may be included in the message by the gateway, so we
                #check for a shutdown signal here.
                sig = msg.get('signal')
                if sig:
                    #If there's a signal in the message, we send it to the chassis
                    #to be sent right back to here after the request handler is
                    #created.  This is done to prevent things from shutting down
                    #too quickly.
                    signal_type = LookupByText(sig)
                    signal_instance = signal_type(self)
                    self.send(signal_instance, 'chassis_signal')

                self.send(msg, 'outbox')
            
            for msg in self.Inbox('control'):
                self.signal = msg
            
            if not (self.anyReady() or self.signal):
                self.pause()
                
            yield 1

        self.send(self.signal, 'signal')
    
    def processInitialMessage(self):
        
        request = self.decodeMessage(self.message)
        self.batch_id = request['batch']
        self.send(self.batch_id, 'batch')
        sig = request.get('signal')
        if sig:
            signal_type = LookupByText(sig)
            signal_instance = signal_type(self)
            self.send(signal_instance, 'chassis_signal')
        
        assert(isinstance(request, dict))
        self.send(request, 'initial')
        
    def decodeMessage(self, msg):
        temp = [str(x) for x in msg.bodies]
        body = ''.join(temp)
        body = base64.decodestring(body)
        body = zlib.decompress(body)
        #print body
        return simplejson.loads(body)
    
class ResponseSerializer(component):
    Inboxes = {
        'inbox' : '',
        'control' : '',
        'batch' : 'receive the batch ID'
    }
    Outboxes = {
        'outbox' : '',
        'signal' : '',
    }
    ThisJID = u'amnorvend@jabber.org'
    ToJID = u'amnorvend_gateway@jabber.org'
    def main(self):
        #wait for the batch ID from the Request Translator
        while not self.dataReady('batch'):
            self.pause()
            yield 1
            
        self.batch_id = self.recv('batch')
        #print '> BATCH ID: ', self.batch_id
        
        self.signal = None
        while not self.signal:
            for response in self.Inbox('inbox'):
                if response.get('signal'):
                    del response['signal']
                    
                if response:
                    self.send(self.makeMessage(response), 'outbox')
                
            for msg in self.Inbox('control'):
                self.signal = msg
                self.send(self.makeMessage({'signal' : type(self.signal).__name__}))
                
            if not self.anyReady() and not self.signal:
                self.pause()
                
            yield 1
            
        yield 1
        self.send(self.signal, 'signal')
        #print 'serializer dying!'
        
    def makeMessage(self, serializable):
        #print serializable
        text = simplejson.dumps(serializable)
        text = zlib.compress(text)
        text = base64.encodestring(text)
        text = unicode(text)
        
        msg = Message(self.ThisJID, self.ToJID,
                      type=u'chat', stanza_id=generate_unique())
        msg.bodies.append(Body(text))
        msg.thread = Thread(self.batch_id)
        
        return msg
        
        
class TranslatorChassis(component):
    """
    This is a chassis that will create a pair of translators and a resource handler
    (aka Minimal or the WSGI Handler).  It will die only when all these components
    die.
    
    Note that this component will also be responsible for forwarding messages from
    the request translator to the resource handler.  It does this to prevent messages
    that are sent before the resource handler is created from being lost.
    """
    Inboxes = {'inbox' : 'Receive body messages.  Forwarded to message translator',
               'control' : '',
               '_msg_translator' : 'Receive messages from the message translator',
               '_body_chunks_in' : 'Receive body chunks',
               '_request_control' : 'Receive signals from the request handler',}
    Outboxes = {'outbox' : '',
                'signal' : '',
                '_body_chunks_out' : 'Send body chunks to the resource handler.',
                '_request_signal' : 'Send signals to message translator',}
    
    requestTranslator = RequestDeserializer
    responseTranslator = ResponseSerializer
    
    ThisJID = None
    ToJID = u'amnorvend_gateway@jabber.org'
    def __init__(self, message, handler_factory, **argd):
        super(TranslatorChassis, self).__init__(**argd)
        self.message = message
        self.handler_factory = handler_factory
        self.initializeComponents()
        self.done = False
        
    def initializeComponents(self):
        """Set up the response and request translators.
        
        FIXME:  This is a disorganized mess."""
        self._requestTranslator = self.requestTranslator(self.message)
        self.link((self, 'inbox'), (self._requestTranslator, 'inbox'), passthrough=1)
        self.link((self, '_request_signal'), (self._requestTranslator, 'control'))
        self.link((self._requestTranslator, 'outbox'), (self, '_body_chunks_in'))
        self.link((self._requestTranslator, 'initial'), (self, '_msg_translator'))
        self.link((self._requestTranslator, 'chassis_signal'), (self, '_request_control'))
        
        self._responseTranslator = self.responseTranslator(ThisJID=self.ThisJID, ToJID=self.ToJID)
        self.link((self._requestTranslator, 'batch'), (self._responseTranslator, 'batch'))
        self.link((self._responseTranslator, 'signal'), (self, 'signal'), passthrough=2)
        
        self.addChildren(self._requestTranslator, self._responseTranslator)
        
    def main(self):
        self._requestTranslator.activate()
        self._responseTranslator.activate()
        
        self.signal = None
        initial_message_handled = False
        
        #Wait for the message translator to send its initial output
        while not self.dataReady('_msg_translator'):
            self.pause()
            yield 1
            
        request = self.recv('_msg_translator')
        #print 'chassis received:\n', request
        
        #FIXME: The below section is a disorganized mess
        self.handler = self.handler_factory(request)
        self._requestTranslator.link((self._requestTranslator, 'signal'), (self.handler, 'control'))
        self.link((self, '_body_chunks_out'), (self.handler, 'inbox'))
        self.link((self.handler, 'outbox'), (self._responseTranslator, 'inbox'))
        self.link((self.handler, 'signal'), (self._responseTranslator, 'control'))
        self.link((self._responseTranslator, 'outbox'), (self, 'outbox'), passthrough=2)
        self.addChildren(self.handler)
        self.handler.activate()
        
        while not self.childrenDone():                            
            #This just forwards body chunks from the request translator to the
            #resource handler.  This is done to prevent any messages that were
            #sent out by the request translator before the resource handler is
            #created from being lost.
            for msg in self.Inbox('_body_chunks_in'):
                self.send(msg, '_body_chunks_out')
                
            #essentially all the following code does is send a signal that was sent
            #to us by the request translator.  It does this so that we can ensure
            #that things don't get shut down too quickly.
            for msg in self.Inbox('_request_control'):
                self.send(msg, '_request_signal')
                
            if not self.anyReady() and not self.childrenDone():
                self.pause()
            
            yield 1
            
    def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us

       return 0==len(self.childComponents())
    
class SimpleHandler(component):
    def __init__(self, request, **argd):
        super(SimpleHandler, self).__init__(**argd)
        self.request = request
    def main(self):
        self.signal = None
        
        resource = {
            'statuscode' : '200 OK',
            'headers' : [('content-type', 'text/plain')],
            'data' : 'Hello, world!',
        }
        self.send(resource, 'outbox')
        
        while not self.signal:
            for msg in self.Inbox('control'):
                self.signal = msg

            for msg in self.Inbox('inbox'):
                print 'SimpleHandler received:\n', msg
                self.send(msg, 'outbox')
                
            if not (self.anyReady() or self.signal):
                self.pause()
                
            yield 1
            
        for msg in self.Inbox('inbox'):
            self.send(msg, 'outbox')
            
        yield 1
        
        self.send(self.signal, 'signal')
        
_log_suffix='.publish.translator'

if __name__ == '__main__':
    from headstock.api.im import Message, Body
    from Kamaelia.Chassis.Pipeline import Pipeline
    

    
    class FakeHTTPServer(component):
        body={u'body' : u'This is the body'}
        def main(self):

            for i in xrange(5):
                self.body['count'] = i
                msg = self.makeMessage(self.body)
                self.send(msg, 'outbox')
                yield 1
                
            signal = {'signal' : 'producerFinished'}
            msg = self.makeMessage(signal)
            self.send(msg, 'outbox')
            
            print 'FakeHTTPServer dying!'
            
        def makeMessage(self, serializable):
            msg = Message(u'foo@foo.com', u'foo2@foo.com',
                          type=u'chat')
            
            text = simplejson.dumps(serializable)
            text = unescape(text)
            text = unicode(text)
            msg.bodies.append(Body(text))
            
            return msg
    
    request ={
        'a' : 'b',
        'c' : 'd',
        'e' : 'f',
        'batch' : '1234'
    }
    serial = simplejson.dumps(request)
    serial = unicode(unescape(serial))
    msg = Message(u'foo@foo.com', u'foo2@foo.com',
                  type=u'chat')
    msg.bodies.append(Body(serial))
    
    https = FakeHTTPServer()
    tc = TranslatorChassis(msg, SimpleHandler)
    print repr(tc)
    
    Pipeline(https, tc).run()
