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

from Axon.ThreadedComponent import threadedadaptivecommscomponent

from translator import TranslatorChassis, RequestDeserializer, ResponseSerializer, SimpleHandler

from headstock.api.im import Message, Thread, Body

class _BoxBundle(object):
    SendMethod=None
    RecvMethod=None
    DataReadyMethod=None
    InboxAddMethod=None
    InboxRmMethod=None
    OutboxAddMethod=None
    OutboxRmMethod=None
    
    thread = None
    
    Translator = None
    def __init__(self, **argd):
        self.__dict__.update(**argd)
        self.box_dict = {}
        self.inbox = ''
        self.outbox = ''
        self.control = ''
        self.signal = ''

    def createBoxes(self):
        thread = str(self.thread)
        self.inbox = self.InboxAddMethod('THREAD_' + self.thread + '_INBOX')
        self.control = self.InboxAddMethod('THREAD_' + self.thread + '_CONTROL')
        self.signal = self.OutboxAddMethod('THREAD_' + self.thread + '_SIGNAL')
        self.outbox = self.OutboxAddMethod('THREAD_' + self.thread + '_OUTBOX')
    def destroyBoxes(self):
        self.InboxRmMethod(self.inbox)
        self.InboxRmMethod(self.control)
        self.OutboxRmMethod(self.signal)
        self.OutboxRmMethod(self.outbox)
        
    def recv(self, boxname):
        return self.RecvMethod(self.__dict__[boxname])
    def Inbox(self, boxname):
        while self.dataReady(boxname):
            yield self.recv(boxname)
    def dataReady(self, boxname):
        return self.DataReadyMethod(self.__dict__[boxname])
    def anyReady(self):
        return self.DataReadyMethod(self.inbox) or self.DataReadyMethod(self.control)
    def send(self, msg, boxname):
        self.SendMethod(msg, boxname)
    def __repr__(self):
        return '<transaction for thread %s: %s, %s, %s, %s>' \
            % (self.thread or '(unknown)', self.inbox, self.control, self.outbox, self.control)
        
def BoxBundle(adap, translator=None, thread=None):
    """This factory function will create a new box bundle with all the necessary
    info about a component.  This is done this way to prevent circular references.
    (the alternative would be to pass the adaptive comms component directly to the
    box bundle)."""
    if not isinstance(thread, str):
        thread = str(thread)
    bundle = _BoxBundle(
        SendMethod = adap.send,
        RecvMethod = adap.recv,
        DataReadyMethod = adap.dataReady,
        InboxAddMethod = adap.addInbox,
        InboxRmMethod = adap.deleteInbox,
        OutboxAddMethod = adap.addOutbox,
        OutboxRmMethod = adap.deleteOutbox,
        LinkMethod = adap.link,
        thread = thread,
        Translator=translator,
    )
    return bundle

class TransactionManager(threadedadaptivecommscomponent):
    RequestTranslator = RequestDeserializer
    ResponseTranslator = ResponseSerializer
    HandlerFactory = SimpleHandler
    def __init__(self, **argd):
        super(TransactionManager, self).__init__(**argd)
        self.transactions = {}
    
    def main(self):
        self.signal = None
        while not self.signal:
            for msg in self.Inbox('control'):
                self.signal = msg
                
            for msg in self.Inbox('inbox'):
                self.handleIncoming(msg)

            marked = set()
            for thread, transaction in self.transactions.iteritems():
                if transaction.anyReady():
                    for msg in transaction.Inbox('control'):
                        marked.add(thread)
                        
                    for msg in transaction.Inbox('inbox'):
                        print 'TM received:\n', Message.to_element(msg).xml()
                        
            self._cleanup(marked)

            if not self.anyReady():
                self.pause()
        for k,v in self.transactions.iteritems():
            print repr(v)                        
    
    def handleIncoming(self, msg):
        if not self.transactions.get(str(msg.thread)):
            self._createTranslator(msg)
        else:
            self._sendToTranslator(msg)
        
    def _createTranslator(self, msg):
        translator = TranslatorChassis(msg, self.HandlerFactory)
        transaction = BoxBundle(self, translator, msg.thread)
        transaction.createBoxes()
        
        #link the newly created transaction object to the translator
        self.link((self, transaction.outbox), (translator, 'inbox'))
        self.link((self, transaction.signal), (translator, 'control'))
        self.link((translator, 'outbox'), (self, transaction.inbox))
        self.link((translator, 'signal'), (self, transaction.control))
        
        self.transactions[str(msg.thread)] = transaction
        
        translator.activate()
        self.addChildren(translator)
        
    def _sendToTranslator(self, msg):
        thread = str(msg.thread)
        transaction = self.transactions[thread]
        transaction.send(msg, 'outbox')
        
    def _cleanup(self, marked):
        for thread in marked:
            transaction = self.transactions[thread]
            self.removeChild(transaction.Translator)
            transaction.destroyBoxes()
            del self.transactions[thread]
        
if __name__ == '__main__':
    from Axon.Component import component
    from Axon.Introspector import Introspector
    from Axon.Ipc import producerFinished
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    import simplejson
    
    class Producer(component):
        def main(self):
            for i in xrange(5):
                msg = Message(u'foo@foo.com', u'foo2@foo.com',
                              type=u'chat')
                body = Body(simplejson.dumps({'batch' :  str(i), 'signal' : 'producerFinished'}))
                msg.bodies.append(body)
                msg.thread = Thread(unicode(i))
                self.send(msg, 'outbox')
                yield 1
                
                msg = Message(u'foo@foo.com', u'foo2@foo.com',
                              type=u'chat')
                body = Body(simplejson.dumps({'signal' : 'producerFinished', 'batch': str(i)}))
                msg.bodies.append(body)
                msg.thread = Thread(unicode(i))
                self.send(msg, 'outbox')
                
                yield 1
                
            self.send(producerFinished(self), 'signal')
            
    Pipeline(
        Producer(),
        TransactionManager(),
    ).run()
