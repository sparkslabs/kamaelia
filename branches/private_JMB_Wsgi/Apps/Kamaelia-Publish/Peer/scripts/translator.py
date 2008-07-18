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
from Axon.Ipc import LookupByText, ToText

from xml.sax.saxutils import unescape, escape

from headstock.api.im import Message, Body, Thread

import simplejson

class RequestTranslator(component):
    Inboxes = {'inbox' : '',
               'control' : '',}
    Outboxes = {'outbox' : '',
                'initial' : 'send the initial output',
                'batch' : 'Output the batch id',
                'signal' : '',
                'chassis_signal' : '',}
    def __init__(self, message, **argd):
        super(RequestTranslator, self).__init__(**argd)
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
                    signal_instance = LookupByText(sig)(self)  #FIXME:  This is just plain ugly.
                    self.send(signal_instance, 'chassis_signal')

                self.send(msg, 'outbox')
            
            for msg in self.Inbox('control'):
                self.signal = msg
            
            if not (self.anyReady() or self.signal):
                self.pause()
                
            yield 1
            
        #print self.signal
        self.send(self.signal, 'signal')
    
    def processInitialMessage(self):
        request = self.decodeMessage(self.message)
        self.batch_id = request['batch']
        self.send(self.batch_id, 'batch')
        
        assert(isinstance(request, dict))
        self.send(request, 'initial')
        
    def decodeMessage(self, msg):
        temp = [str(x) for x in msg.bodies]
        body = ''.join(temp)
        
        body = unescape(body)
        return simplejson.loads(body)
    
class ResponseTranslator(component):
    Inboxes = {
        'inbox' : '',
        'control' : '',
        'batch' : 'receive the batch ID'
    }
    Outboxes = {
        'outbox' : '',
        'signal' : '',
    }
    def main(self):
        #wait for the batch ID from the Request Translator
        while not self.dataReady('batch'):
            self.pause()
            yield 1
            
        self.batch_id = self.recv('batch')
        print '> BATCH ID: ', self.batch_id
        
        self.signal = None
        while not self.signal:
            for response in self.Inbox('inbox'):
                print Message.to_element(self.makeMessage(response)).xml()
                
            for msg in self.Inbox('control'):
                self.signal = msg
                
            if not self.anyReady() and not self.signal:
                self.pause()
                
            yield 1
            
        self.send(self.signal, 'signal')
        
    def makeMessage(self, serializable):            
        text = simplejson.dumps(serializable)
        text = escape(text) #FIXME:  Security issue.  Will unescape escaped HTML when deserialized
        text = unicode(text)
        
        msg = Message(u'foo@foo.com', u'foo2@foo.com',
                      type=u'chat')
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
    
    requestTranslator = RequestTranslator
    responseTranslator = ResponseTranslator
    def __init__(self, message, handler_factory, **argd):
        super(TranslatorChassis, self).__init__(**argd)
        self.message = message
        self.handler_factory = handler_factory
        self.initializeComponents()
        
    def initializeComponents(self):
        """Set up the response and request translators.
        
        FIXME:  This is a disorganized mess."""
        self._requestTranslator = self.requestTranslator(self.message)
        self.link((self, 'inbox'), (self._requestTranslator, 'inbox'), passthrough=1)
        self.link((self, '_request_signal'), (self._requestTranslator, 'control'))
        self.link((self._requestTranslator, 'outbox'), (self, '_body_chunks_in'))
        self.link((self._requestTranslator, 'initial'), (self, '_msg_translator'))
        self.link((self._requestTranslator, 'chassis_signal'), (self, '_request_control'))
        
        self._responseTranslator = self.responseTranslator()
        self.link((self._requestTranslator, 'batch'), (self._responseTranslator, 'batch'))
        self.link((self._requestTranslator, 'signal'), (self, 'signal'), passthrough=2)
        self._responseTranslator.activate()
        
        self.addChildren(self._requestTranslator, self._responseTranslator)
        
    def main(self):
        self._requestTranslator.activate()
        
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
        
if __name__ == '__main__':
    from headstock.api.im import Message, Body
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    class SimpleHandler(component):
        def __init__(self, request, **argd):
            super(SimpleHandler, self).__init__(**argd)
            self.request = request
        def main(self):
            self.signal = None
            
            resource = {
                'statuscode' : '200 OK',
                'headers' : [('content-type', 'text/plain')],
                'data' : self.request.get('body'),
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
                
            self.send(self.signal, 'signal')
            print 'SimpleHandler dying!'
    
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
    
    Pipeline(https, tc).run()
