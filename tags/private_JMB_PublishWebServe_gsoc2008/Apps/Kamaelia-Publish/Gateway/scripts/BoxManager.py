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

class _BoxManager(object):
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
    UnlinkMethod=None
    
    thread = None
    
    Translator = None
    def __init__(self, **argd):
        self.__dict__.update(**argd)
        self.inboxes = {}
        self.outboxes = {}

    def createBoxes(self, inboxes=('inbox', 'control'), outboxes=('outbox', 'signal')):
        """Create a set of inboxes and outboxes.  You will be responsible for linking
        them."""
        thread = self.thread
        BOX_TEMPLATE='THREAD_%s_%s'
        for box in inboxes or []:
            self.inboxes[box] = self.InboxAddMethod(BOX_TEMPLATE % (thread, box))
        for box in outboxes or []:
            self.outboxes[box] = self.OutboxAddMethod(BOX_TEMPLATE % (thread, box))
    def kill(self):
        """Destroy and unlink all boxes that are managed by this box manager."""
        self.UnlinkMethod(self.Translator)
        self._destroy_boxes()
    def recv(self, boxname):
        """Receive a message from an inbox.  Maps a human-friendly boxname
        to an AdaptiveCommsComponent boxname."""
        return self.RecvMethod(self.inboxes[boxname])
    def Inbox(self, boxname):
        """Iterate over the messages in an inbox."""
        while self.dataReady(boxname):
            yield self.recv(boxname)
    def dataReady(self, boxname):
        """Checks to see if a box has ready data.  Maps a human-friendly boxname
        to an AdaptiveCommsComponent boxname."""
        return self.DataReadyMethod(self.inboxes[boxname])
    def send(self, msg, boxname):
        """Maps send a message using a human-friendly boxname that translates to
        an AdaptiveCommsComponent boxname."""
        self.SendMethod(msg, self.outboxes[boxname])
    def __repr__(self):
        return '<BoxManager for thread %s>' % (self.thread)        
    def _get_done(self):
        """Returns true if the managed translator is stopped.  Intended to be called
        via the property done."""
        return self.Translator._isStopped()
    done = property(fget=_get_done)
    def _destroy_boxes(self):
        """Destroys all managed boxes without unlinking them."""
        for box in self.inboxes:
            self.InboxRmMethod(self.inboxes[box])
        for box in self.outboxes:
            self.OutboxRmMethod(self.outboxes[box])
        #Recreate the box dictionaries in case we need to reuse this object
        self.inboxes={}
        self.outboxes={}

def BoxManager(adap, translator=None, thread=None):
    """This factory function will create a new box bundle with all the necessary
    info about a component.  This is done this way to prevent circular references.
    (the alternative would be to pass the adaptive comms component directly to the
    box bundle)."""
    if not isinstance(thread, str):
        thread = str(thread)
    bman = _BoxManager(
        SendMethod = adap.send,
        RecvMethod = adap.recv,
        DataReadyMethod = adap.dataReady,
        InboxAddMethod = adap.addInbox,
        InboxRmMethod = adap.deleteInbox,
        OutboxAddMethod = adap.addOutbox,
        OutboxRmMethod = adap.deleteOutbox,
        UnlinkMethod=adap.unlink,
        thread = thread,
        Translator=translator,
    )
    return bman
