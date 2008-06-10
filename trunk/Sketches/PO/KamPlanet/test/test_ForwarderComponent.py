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

from Axon.Ipc import producerFinished, shutdownMicroprocess

import KamTestCase

import ForwarderComponent

class ForwarderComponentTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.forwarderComponent = ForwarderComponent.Forwarder()
        self.initializeSystem(self.forwarderComponent)
        
    def testSimpleUse(self):
        self.messageAdder.addMessage("message1", 'inbox')
        self.messageAdder.addMessage("message2", 'inbox')
        self.messageAdder.addYield(50) # let it breathe
        self.messageAdder.addMessage("message3", 'inbox')
        self.messageAdder.addMessage("message4", 'inbox')
        producerFinishedObj = producerFinished()
        self.messageAdder.addMessage(producerFinishedObj, "control")
        self.messageAdder.addYield(50) # let it breathe
        # The following message will not be considered since the component has already finished
        self.messageAdder.addMessage(producerFinishedObj, "control")
        self.assertStopping()
        messages = self.messageStorer.getMessages('outbox')
        self.assertEquals(4, len(messages))
        for i in xrange(4):
            expected = "message%s" % (i + 1)
            actual   = messages[i]
            self.assertEquals(expected, actual, "Failed on i = %s: <%s> != <%s>" % (i, expected, actual))
        messages = self.messageStorer.getMessages('signal')
        self.assertEquals(1, len(messages)) # and only one, the second one did not arrive
        self.assertEquals(producerFinishedObj, messages[0])

    def testSimpleSecondaryUse(self):
        self.messageAdder.addMessage("message1", 'secondary-inbox')
        self.messageAdder.addMessage("message2", 'secondary-inbox')
        self.messageAdder.addYield(50) # let it breathe
        self.messageAdder.addMessage("message3", 'secondary-inbox')
        self.messageAdder.addMessage("message4", 'secondary-inbox')
        producerFinishedObj = producerFinished()
        self.messageAdder.addMessage(producerFinishedObj, "secondary-control")
        self.messageAdder.addYield(50) # let it breathe
        # The following message will not be considered since the component has already finished
        self.messageAdder.addMessage(producerFinishedObj, "secondary-control")
        self.assertStopping()
        messages = self.messageStorer.getMessages('outbox')
        self.assertEquals(4, len(messages))
        for i in xrange(4):
            expected = "message%s" % (i + 1)
            actual   = messages[i]
            self.assertEquals(expected, actual, "Failed on i = %s: <%s> != <%s>" % (i, expected, actual))
        messages = self.messageStorer.getMessages('signal')
        self.assertEquals(1, len(messages)) # and only one, the second one did not arrive
        self.assertEquals(producerFinishedObj, messages[0])
    
    def testSimpleMixedUse(self):
        # Take into account that the yields are necessary, since the
        # Forwarder component can't ensure the order among messages received in
        # two different inboxes
        self.messageAdder.addMessage("message1", 'inbox')
        self.messageAdder.addMessage("message2", 'inbox')
        self.messageAdder.addYield(50) # let it breathe
        self.messageAdder.addMessage("message3", 'secondary-inbox')
        self.messageAdder.addMessage("message4", 'secondary-inbox')
        self.messageAdder.addYield(50) # let it breathe
        self.messageAdder.addMessage("message5", 'inbox')
        self.messageAdder.addYield(50) # let it breathe
        self.messageAdder.addMessage("message6", 'secondary-inbox')
        self.messageAdder.addYield(50) # let it breathe
        self.messageAdder.addMessage("message7", 'inbox')
        producerFinishedObj = producerFinished()
        self.messageAdder.addMessage(producerFinishedObj, "control")
        self.assertStopping()
        messages = self.messageStorer.getMessages('outbox')
        self.assertEquals(7, len(messages))
        for i in xrange(7):
            expected = "message%s" % (i + 1)
            actual   = messages[i]
            self.assertEquals(expected, actual, "Failed on i = %s: <%s> != <%s>" % (i, expected, actual))
        messages = self.messageStorer.getMessages('signal')
        self.assertEquals(1, len(messages))
        self.assertEquals(producerFinishedObj, messages[0])

def suite():
    return KamTestCase.makeSuite(ForwarderComponentTestCase.getTestCase())
    
if __name__ == '__main__':
    KamTestCase.main()
