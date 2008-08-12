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

from Axon.ThreadedComponent import threadedadaptivecommscomponent
from Kamaelia.Util.Backplane import SubscribeTo

from translator import TranslatorChassis, RequestDeserializer, ResponseSerializer, SimpleHandler

from headstock.api.im import Message, Thread, Body

class _BoxBundle(object):
    """
    This object is used to represent a set of boxes in an adaptive comms component.
    It may also store metadata about the transaction.
    """
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
        self.UnlinkMethod(self.Translator)
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
        self.SendMethod(msg, self.__dict__[boxname])
    def __repr__(self):
        return '<transaction for thread %s: %s, %s, %s, %s>' \
            % (self.thread or '(unknown)', self.inbox, self.control, self.outbox, self.control)
        
    def _get_done(self):
        return self.Translator._isStopped()
    
    done = property(fget=_get_done)
        
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
        UnlinkMethod = adap.unlink,
        thread = thread,
        Translator=translator,
    )
    return bundle

class NullBundle(object):
    pass

class TransactionManager(threadedadaptivecommscomponent):
    Inboxes = {'inbox' : 'Receive output from the translators',
               'control' : 'Receive shutdown messages',
               'jid' : 'Receive the JID from headstock'}
    Outboxes = {'outbox' : 'NOT USED',
                'signal' : 'Send shutdown messages'}
    
    """
    This component will manage all the various transactions going on at any given
    point in time.  A transaction represents an HTTP request and response transaction.
    Note that of course the actual HTTP request and response don't actually happen
    here in this program.  They happen at the gateway.
    
    Upon receiving a message that is a part of a thread the TransactionManager has
    not encountered yet, a new BoxBundle is created to represent the transaction.
    In addition, a translator is created to translate data passed back and forth
    between the TransactionManager and the resource handler (that will be created
    by the translator).
    """
    #As of right now, there's not much reason to override the next two attributes.
    #But there may be in the future!
    RequestTranslator = RequestDeserializer
    ResponseTranslator = ResponseSerializer
    HandlerFactory = SimpleHandler
    
    ThisJID=None
    def __init__(self, **argd):
        super(TransactionManager, self).__init__(**argd)
        self.transactions = {}
        self.null = NullBundle()
    
    def main(self):
        self.jid_subscriber = SubscribeTo('JID')
        self.link((self.jid_subscriber, 'outbox'), (self, 'jid'))
        self.jid_subscriber.activate()
        
        self.signal = None
        while not self.signal:
            for msg in self.Inbox('jid'):
                self.ThisJID = msg
                
            for msg in self.Inbox('control'):
                self.signal = msg
                
            for msg in self.Inbox('inbox'):
                self.handleIncoming(msg)

            #This is a set of all the transactions that will be removed once this
            #loop is finished.  We do it this way to prevent the size of self.transactions
            #from changing in the middle of the loop (which will cause an exception).
            marked = set()
            for thread, transaction in self.transactions.iteritems():
                if transaction.anyReady():
                    if transaction.done:
                        marked.add(transaction)
                    
                    self.sync()
                    for msg in transaction.Inbox('inbox'):
                        self.send(msg, 'outbox')
                        
            self._cleanup(marked)

            if not self.anyReady():
                self.pause()
        for k,v in self.transactions.iteritems():
            print repr(v)
    
    def handleIncoming(self, msg):
        if not self.transactions.get(str(msg.thread)):
            self._createTranslator(msg)
        elif isinstance(self.transactions[str(msg.thread)], NullBundle):
            pass
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
        for transaction in marked:
            assert(transaction.Translator._isStopped())
            self.removeChild(transaction.Translator)
            transaction.destroyBoxes()
            del self.transactions[transaction.thread]
        
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
