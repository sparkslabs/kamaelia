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
This component is the interface between the HTTP code and the XMPP code in the
Kamaelia Publish Gateway.  All messages it receives from the HTTP code will come
in on the backplanes named in gate.__init__ (BPLANE_INBOX and BPLANE_CONTROL).

A translator will register itself by sending a newBatch signal to the interface.
Once the translator has registered, it will receive incoming messages from the
peer it is communicating with.  The interface will continue to listen for incoming
messages from that peer until the translator sends it a batchDone signal.

The interface also serves to forward messages from translators to headstock
to be sent to peers.  Since it currently just passes the messages on, BPLANE_INBOX
may eventually be set up to forward messages to headstock directly.

FIXME:  This component needs a timeout mechanism.  It will currently wait indefinitely
until it receives a response.
"""

from Axon.ThreadedComponent import threadedcomponent, threadedadaptivecommscomponent
from Kamaelia.Util.Backplane import Backplane, SubscribeTo
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.IPC import userLoggedOut, batchDone, newBatch
from Kamaelia.Apps.Web_common.Console import debug, info, warning
from Kamaelia.Apps.Publish.Gateway.consts import BPLANE_INBOX, BPLANE_CONTROL
from Kamaelia.Apps.Publish.Gateway.JIDLookup import setUserStatus

from headstock.api.im import Message
from headstock.api.jid import JID

from BoxManager import BoxManager

_logger_suffix = '.publish.gateway.interface'

class Interface(threadedadaptivecommscomponent):
    ThisJID = None
    Inboxes = {
        'inbox' : 'Receive messages from a translator.'\
                'Connected to the service named by BPLANE_NAME',
        'control' : 'Receive shutdown messages from a translator',
        'xmpp.inbox' : 'Receive messages from the XMPP message dispatcher',
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
        """
        This creates the necessary subcomponents to have messages sent to this component's
        inbox and control box via a backplane.
        """
        self.bplane_in = Backplane(BPLANE_INBOX).activate()
        self.bplane_control = Backplane(BPLANE_CONTROL).activate()
        self.subscriber_in = SubscribeTo(BPLANE_INBOX).activate()
        self.subscriber_control = SubscribeTo(BPLANE_CONTROL).activate()
        
        self.link((self.subscriber_in, 'outbox'), (self, 'inbox'))
        self.link((self.subscriber_control, 'outbox'), (self, 'control'))
        
        self.link((self, '_bplane_signal_in'), (self.bplane_in, 'control'))
        self.link((self, '_bplane_signal_control'), (self.bplane_control, 'control'))
        self.link((self, '_subscriber_signal_in'), (self.subscriber_in, 'control'))
        self.link((self, '_subscriber_signal_control'), (self.subscriber_control, 'control'))
    
    def main(self):        
        self.createSubcomponents()
        
        while self.not_done:
            for msg in self.Inbox('control'):
                self.handleMainControlBox(msg)
                
            for msg in self.Inbox('inbox'):
                self.handleMainInbox(msg)
                
            for msg in self.Inbox('xmpp.inbox'):
                #The interface has a new message from a serving peer.  Get the bundle
                #associated with the thread's translator and forward the message.
                box_manager = self.transactions.get(unicode(msg.thread))
                if box_manager:
                    box_manager.send(msg, 'outbox')
                else:
                    warning('%s received with no box manager.' % (msg),
                            _logger_suffix)
                    
            for msg in self.Inbox('xmpp.available'):
                if msg.from_jid.nodeid() != self.ThisJID.nodeid():
                    debug('%s available.' % (msg.from_jid), _logger_suffix)
                    self.handleAvailable(msg)
                else:
                    debug('%s available.  No action taken.' % (msg.from_jid), _logger_suffix)
            for msg in self.Inbox('xmpp.unavailable'):
                self.handleUnavailable(msg)
                info('User %s logged out.' % (msg.from_jid.nodeid()), _logger_suffix)
                
            if not self.anyReady() and self.not_done:
                self.pause()
        
        self.sendSignals()
    
    def handleMainInbox(self, msg):
        """This function will monitor the incoming inbox for new messages.  If the
        message is an instance of InitialMessage, it will create a BoxManager that
        will create the necessary outboxes and track the translator.  If it is a
        headstock message, it will be forwarded out to be sent via XMPP."""
        if isinstance(msg, Message):
            #Forward the message on to headstock
            self.send(msg, 'xmpp.outbox')
        else:
            warning('Unknown message %s received at interface.  Ignoring'
                    % (msg), _logger_suffix)
            
    def handleMainControlBox(self, msg):
        """This will handle incoming messages from various translators to signal that
        they are done.  This will unlink this component from them and destroy all
        associated boxes."""
        if isinstance(msg, batchDone) and self.transactions.get(msg.batch_id):
            bman.kill()
            del self.transactions[msg.thread]
            debug('Batch %s done.' % (msg.thread), _logger_suffix)
        elif isinstance(msg, newBatch):
            bman=BoxManager(self, msg.bundle, msg.batch_id)
            self.transactions[msg.batch_id] = bman
            bman.createBoxes(inboxes=None, outboxes=['outbox', 'signal'])
            self.link((self, bman.outboxes['outbox']), (msg.bundle, 'xmpp_in'))
            self.link((self, bman.outboxes['signal']), (msg.bundle, 'xmpp_control'))
            
            to_jid = msg.to_jid
            if isinstance(to_jid, JID):
                to_jid = to_jid.node_id()
            elif not isinstance(to_jid, unicode):
                to_jid = unicode(to_jid)
            
            self.jids[to_jid].append(msg.batch_id)
        else:
            warning('Unknown signal %s received at interface.  Ignoring'
                    % (msg), _logger_suffix)
            
    def handleAvailable(self, pres):
        """This function is called when a user comes online.  It will create an
        entry in the JIDs dict that will associate threads with their JID."""
        jid = pres.from_jid.nodeid()
        self.jids[jid] = []
        setUserStatus(jid, active=True)
    
    def handleUnavailable(self, pres):
        """This function will be called when a user goes offline.  It will remove
        all tracked resources associated with that user and set the user's status
        in the database."""
        jid = pres.from_jid.nodeid()
        batches = self.jids.get(jid, None)
        if not (batches is None):
            for batch_id in batches:
                bundle = self.transactions[batch_id]
                bundle.send(userLoggedOut(batch_id), 'signal')
                bundle.kill()
                del self.transactions[batch_id]
            del self.jids[jid]
        else:
            warning('JID %s went unavailable but is not logged in' \
                    % (unicode(jid)), _logger_suffix)
        setUserStatus(pres.from_jid, active=False)
        
    def sendSignals(self):
        """Send out the signals to various components to indicate that this component
        is shuttind down."""
        self.send(self.signal, '_bplane_signal_in')
        self.send(self.signal, '_bplane_signal_control')
        self.send(self.signal, '_subscriber_signal_in')
        self.send(self.signal, '_subscriber_signal_control')
