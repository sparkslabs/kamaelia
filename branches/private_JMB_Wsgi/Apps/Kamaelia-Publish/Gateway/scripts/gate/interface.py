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

from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Util.Backplane import Backplane, SubscribeTo

from headstock.api.im import Message

from gate import InitialMessage, BPLANE_NAME

class Interface(threadedcomponent):
    Inboxes = {
        'inbox' : 'Receive messages from a translator.'\
                'Connected to the service named by BPLANE_NAME',
        'translator_inbox' : 'Receive messages from a translator',
        'translator_control' : 'Receive signals from the translator',
        'xmpp_inbox' : 'Receive messages from the XMPPHandler',
        'xmpp_control' : 'Receive signals from the XMPPHandler'
    }
    Outboxes = {
        'xmpp_signal' : 'Send signals to the XMPPHandler',
        'xmpp_outbox' : 'Send messages to the XMPPHandler to be sent out',
        '_bplane_signal' : 'Send shutdown messages to the backplane',
        '_subscriber_signal' : 'Send shutdown messages to the subscriber',
    }
    def __init__(self, **argd):
        super(Interface, self).__init__(**argd)
        self.session_dict = {}
    
    def createSubcomponents(self):
        self.bplane = Backplane(BPLANE_NAME)
        self.bplane.activate()
        
        self.subscriber = SubscribeTo(BPLANE_NAME)
        self.subscriber.activate()
        self.link((self.subscriber, 'outbox'), (self, 'inbox'))
    
    def main(self):        
        self.createSubcomponents()
        
        self.not_done = True
        while self.not_done:
            for msg in self.Inbox('inbox'):
                self.handleMainInbox(msg)
                
            for msg in self.Inbox('xmpp_inbox'):
                bundle = self.session_dict.get(unicode(msg.thread))
                if bundle:
                    bundle.send(msg, 'outbox')
                
            if not self.anyReady() and self.not_done:
                self.pause()
    
    def handleMainInbox(self, msg):
        if isinstance(msg, InitialMessage):            
            self.session_dict[msg.batch_id] = msg.bundle
            self.send(msg.hMessage, 'xmpp_outbox')
            print 'Interface received the following:'
            print Message.to_element(msg.hMessage).xml()
        elif isinstance(msg, Message):
            self.send(msg, 'xmpp_outbox')
    

