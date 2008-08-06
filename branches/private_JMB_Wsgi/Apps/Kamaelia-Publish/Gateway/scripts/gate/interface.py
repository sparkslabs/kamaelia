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

from Axon.ThreadedComponent import threadedcomponent, threadedadaptivecommscomponent
from Kamaelia.Util.Backplane import Backplane, SubscribeTo
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.IPC import userLoggedOut
from Kamaelia.Apps.Wsgi.BoxManager import BoxManager

from headstock.api.im import Message

from gate import InitialMessage, BPLANE_NAME, BPLANE_SIGNAL
import JIDLookup

class Interface(threadedadaptivecommscomponent):
    ThisJID = None
    Inboxes = {
        'inbox' : 'Receive messages from a translator.'\
                'Connected to the service named by BPLANE_NAME',
        'control' : 'Receive shutdown messages from a translator',
        'translator_inbox' : 'Receive messages from a translator',
        'translator_control' : 'Receive signals from the translator',
        'xmpp.inbox' : 'Receive messages from the XMPPHandler',
        'xmpp.control' : 'Receive signals from the XMPPHandler',
        'xmpp.available' : 'Receive notification when a user becomes available',
        'xmpp.unavailable' : 'Receive notification when a user becomes unavailable',
    }
    Outboxes = {
        'xmpp.signal' : 'Send signals to the XMPPHandler',
        'xmpp.outbox' : 'Send messages to the XMPPHandler to be sent out',
        '_bplane_signal_in' : 'Send shutdown messages to the in backplane',
        '_bplane_signal_control' : 'Send shutdown messages to the control backplane',
        '_subscriber_signal_in' : 'Send shutdown messages to the in subscriber',
        '_subscriber_signal_control' : 'Send shutdown messages to the control subscriber'
    }
    def __init__(self, **argd):
        super(Interface, self).__init__(**argd)
        self.transactions = {}
        self.jids = {}
        self.not_done = True
    
    def createSubcomponents(self):
        self.bplane_in = Backplane(BPLANE_NAME).activate()
        self.bplane_control = Backplane(BPLANE_SIGNAL).activate()
        
        self.subscriber_in = SubscribeTo(BPLANE_NAME).activate()
        self.subscriber_control = SubscribeTo(BPLANE_SIGNAL).activate()
        
        self.link((self.subscriber_in, 'outbox'), (self, 'inbox'))
        self.link((self.subscriber_control, 'signal'), (self, 'control'))
        
        self.link((self, '_bplane_signal_in'), (self.bplane_in, 'control'))
        self.link((self, '_bplane_signal_control'), (self.bplane_control, 'control'))
        self.link((self, '_subscriber_signal_in'), (self.subscriber_in, 'control'))
        self.link((self, '_subscriber_signal_control'), (self.subscriber_control, 'control'))
    
    def main(self):        
        self.createSubcomponents()
        
        while self.not_done:
            for msg in self.Inbox('inbox'):
                self.handleMainInbox(msg)
                
            for msg in self.Inbox('xmpp.inbox'):
                #The interface has a new message from a serving peer.  Get the bundle
                #associated with the thread's translator and forward the message.
                bundle = self.transactions.get(unicode(msg.thread))
                if bundle:
                    bundle.send(msg, 'outbox')
                    
            for msg in self.Inbox('xmpp.available'):
                if msg.from_jid.nodeid() != self.ThisJID.nodeid():
                    print '%s available.' % (msg.from_jid)
                    self.handleAvailable(msg)
                else:
                    print '%s available.  No action taken.' % (msg.from_jid)
            for msg in self.Inbox('xmpp.unavailable'):
                self.handleUnavailable(msg)
                #print 'Received unavailable:  %s' % (repr(msg))
                
            if not self.anyReady() and self.not_done:
                self.pause()
        
        self.sendSignals()
    
    def handleMainInbox(self, msg):
        if isinstance(msg, InitialMessage):
            #This is the first message in the transaction.
            
            #Add the bundle to the transaction list so that we can look it up when
            #we receive a response
            bman = BoxManager(self, msg.bundle, msg.batch_id)
            bundle = msg.bundle
            self.transactions[msg.batch_id] = bman
            bman.createBoxes(inboxes=None, outboxes=['outbox', 'signal'])
            self.link((self, bman.outboxes['outbox']), (bundle, 'xmpp_in'))
            self.link((self, bman.outboxes['signal']), (bundle, 'xmpp_control'))
            
            #Add the thread to the jids dict so that we can get back to any associated
            #bundles if the user goes offline
            self.jids[msg.hMessage.to_jid].append(msg.batch_id)
            self.send(msg.hMessage, 'xmpp.outbox')
        elif isinstance(msg, Message):
            self.send(msg, 'xmpp.outbox')
            
    def handleAvailable(self, pres):
        
        jid = pres.from_jid.nodeid()
        self.jids[jid] = []
        JIDLookup.setUserStatus(jid, active=True)
        #print self.jids
    
    def handleUnavailable(self, pres):
        jid = pres.from_jid.nodeid()
        for batch_id in self.jids[jid]:
            #print 'Killing %s...' % (batch_id)
            bundle = self.transactions[batch_id]
            #print bundle
            bundle.send(userLoggedOut(batch_id), 'signal')
            bundle.kill()
            del self.transactions[batch_id]
        
        del self.jids[jid]
        JIDLookup.setUserStatus(pres.from_jid, active=False)
        
    def sendSignals(self):
        self.send(self.signal, '_bplane_signal_in')
        self.send(self.signal, '_bplane_signal_control')
        self.send(self.signal, '_subscriber_signal_in')
        self.send(self.signal, '_subscriber_signal_control')
