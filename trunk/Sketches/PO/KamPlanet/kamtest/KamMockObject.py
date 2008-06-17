#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

import Axon

import MessageAdder
import MessageStorer

class _KamMockObject(Axon.Component.component):
    def __init__(self, inputComponentToMock, outputComponentToMock, **kwargs):
        self.publicInboxes,  self.publicOutboxes = self._setupInboxesOutboxes(
                                                            inputComponentToMock, 
                                                            outputComponentToMock
                                                    )
        super(_KamMockObject, self).__init__(**kwargs)
        
        self.messageStorer = MessageStorer.MessageStorer(self.publicInboxes)
        self.messageAdder  = MessageAdder.MessageAdder(self.publicOutboxes)
        
        for inboxName in self.publicInboxes:
            self.link((self, '_child_' + inboxName), (self.messageStorer, inboxName))
        for outboxName in self.publicOutboxes:
            self.link((self.messageAdder, outboxName),  (self, '_child_' + outboxName))
        self._stop_within_iterations = None
    
    def _setupInboxesOutboxes(self, inputComponentToMock, outputComponentToMock):
        publicInboxNames = [ inboxName 
                      for inboxName in inputComponentToMock.Inboxes 
                        if not inboxName.startswith('_')
                ]
        publicOutboxNames = [ outboxName 
                       for outboxName in outputComponentToMock.Outboxes 
                        if not outboxName.startswith('_')
                ]
        
        inboxesPlusChildOutboxes = publicInboxNames[:]
        for outboxName in publicOutboxNames:
            inboxesPlusChildOutboxes.append('_child_' + outboxName)
            
        outboxesPlusChildInboxes = publicOutboxNames[:]
        for inboxName in publicInboxNames:
            outboxesPlusChildInboxes.append('_child_' + inboxName)
        
        self.Inboxes  = inboxesPlusChildOutboxes
        self.Outboxes = outboxesPlusChildInboxes
        return publicInboxNames, publicOutboxNames
    
    def stopMockObject(self, within_iterations = 0):
        self._stop_within_iterations = within_iterations
        self.messageStorer.stopMessageStorer(within_iterations)
        self.messageAdder.stopMessageAdder(within_iterations)
        
    def addMessage(self, msg, outbox):
        self.messageAdder.addMessage(msg, outbox)
        
    def addYield(self, n = 1):
        self.messageAdder.addYield(n)
        
    def getMessages(self, inbox):
        return self.messageStorer.getMessages(inbox)
    
    def main(self):
        self.messageStorer.activate()
        self.messageAdder.activate()
        self.addChildren(self.messageStorer)
        self.addChildren(self.messageAdder)
        
        while self._stop_within_iterations is None or self._stop_within_iterations > 0:
            for inbox in self.publicInboxes:
                while self.dataReady(inbox):
                    data = self.recv(inbox)
                    self.send(data, '_child_' + inbox)
                    
            for outbox in self.publicOutboxes:
                while self.dataReady('_child_' + outbox):
                    data = self.recv('_child_' + outbox)
                    self.send(data, outbox)
                
            if self._stop_within_iterations is not None:
                self._stop_within_iterations = self._stop_within_iterations - 1
                
            yield 1
