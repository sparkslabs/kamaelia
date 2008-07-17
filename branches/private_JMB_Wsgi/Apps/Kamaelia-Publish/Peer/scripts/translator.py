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
from Axon.Ipc import LookupByText

from xml.sax.saxutils import unescape, escape

import simplejson

class MessageToRequestTranslator(component):
    Inboxes = {'inbox' : '',
               'control' : '',}
    Outboxes = {'outbox' : '',
                '_initial' : 'send the initial output',
                'signal' : ''}
    
    def __init__(self, message, **argd):
        super(MessageToRequestTranslator, self).__init__(**argd)
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
                    msg['signal'] = LookupByText(sig)(self)
                    print 'Signal received: ', msg['signal']
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
        
        assert(isinstance(request, dict))
        self.send(request, '_initial')
        
    def decodeMessage(self, msg):
        temp = [str(x) for x in msg.bodies]
        body = ''.join(temp)
        
        body = unescape(body)
        return simplejson.loads(body)
        
class TranslatorChassis(component):
    Inboxes = {'inbox' : 'Receive body messages.  Forwarded to message translator',
               'control' : '',
               '_msg_translator' : 'Receive messages from the message translator',
               '_handler' : 'Receive outgoing messages from the resource handler',
               '_body_chunks_in' : 'Receive body chunks'}
    Outboxes = {'outbox' : '',
                'signal' : '',
                '_body_chunks_out' : 'Send body chunks to the resource handler.',
                '_msg_translator_signal' : 'Send signals to message translator',}
    
    messageTranslator = MessageToRequestTranslator
    #self.responseTranslator = ResponseToMessageTranslator
    def __init__(self, message, handler_factory, **argd):
        super(TranslatorChassis, self).__init__(**argd)
        self.message = message
        self.handler_factory = handler_factory
        self.initializeComponents()
        
    def initializeComponents(self):
        self._messageTranslator = self.messageTranslator(self.message)
        self.link((self, 'inbox'), (self._messageTranslator, 'inbox'), passthrough=1)
        self.link((self, '_msg_translator_signal'), (self._messageTranslator, 'control'))
        self.link((self._messageTranslator, 'outbox'), (self, '_body_chunks_in'))
        self.link((self._messageTranslator, '_initial'), (self, '_msg_translator'))
        
        self.addChildren(self._messageTranslator)
        
    def main(self):
        self._messageTranslator.activate()
        
        self.signal = None
        initial_message_handled = False
        
        #Wait for the message translator to send its initial output
        while not self.dataReady('_msg_translator'):
            self.pause()
            yield 1
        request = self.recv('_msg_translator')
        #print 'chassis received:\n', request
        
        self.handler = self.handler_factory(request)
        self._messageTranslator.link((self._messageTranslator, 'signal'), (self.handler, 'control'))
        self.link((self.handler, 'outbox'), (self, '_handler'))
        self.link((self, '_body_chunks_out'), (self.handler, 'inbox'))
        self.addChildren(self.handler)
        self.handler.activate()
        
        self.signal = None
        while not self.childrenDone():            
            for msg in self.Inbox('_handler'):
                print 'Chassis Received', msg
                
            for msg in self.Inbox('_body_chunks_in'):
                if msg.get('signal'):
                    self.send(msg['signal'], '_msg_translator_signal')
                self.send(msg, '_body_chunks_out')
                
            if not self.anyReady() and not self.childrenDone():
                self.pause()
            
            yield 1
            
        for msg in self.Inbox('_handler'):
            print msg
            
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
    }
    serial = simplejson.dumps(request)
    serial = unicode(unescape(serial))
    msg = Message(u'foo@foo.com', u'foo2@foo.com',
                  type=u'chat')
    msg.bodies.append(Body(serial))
    
    https = FakeHTTPServer()
    tc = TranslatorChassis(msg, SimpleHandler)
    
    Pipeline(https, tc).run()
