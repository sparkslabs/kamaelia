#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""Kamaelia Concurrency Component Framework.

LINKAGES

Components only have input & output boxes. For data to get from a producer
(eg a file reader) to a consumer (eg an encryption component) then the output
of one component, the source component, must be linked to the input of
another component, the sink component.

All components have a postoffice object, this performs the creation and
destruction of linkages. Ask it for a linkage between inboxes and outboxes and
a linkage object is returned as a handle describing the linkage. When a message
is sent to an outbox, it is immediately delivered along linkage(s) to the
destination inbox.

This is NOT the usual technique for software messaging. Normally you create
messages, addressed to something specific, and then the message handler delivers
them.

However the method of communication used here is the norm for _hardware_ systems,
and generally results in very pluggable components - the aim of this system,
hence this design approach rather than the normal. This method of
communication is also the norm for one form of software system - unix shell
scripting - something that has shown itself time and again to be used in ways
the inventors of programs/components never envisioned.

"""
import time

from AxonExceptions import AxonException, ArgumentsClash
from Axon import AxonObject
from util import removeAll
from idGen import strId, numId,Debug
from debug import debug


class linkage(AxonObject):
    """\
    linkage(source, sink[, passthrough]) -> new linkage object
    
    An object describing a link from a source component's inbox/outbox to a
    sink component's inbox/outbox.
    
    Keyword arguments:
    - source       -- source component
    - sink         -- sink component
    - sourcebox    -- source component's source box name (default="outbox")
    - sinkbox      -- sink component's sink box name (default="inbox")
    - passthrough  -- 0=link is from inbox to outbox; 1=from inbox to inbox; 2=from outbox to outbox (default=0)
    """
    def __init__(self, source, sink, sourcebox="outbox", sinkbox="inbox", passthrough=0, pipewidth=None, synchronous=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature."""
        if synchronous is not None:
            raise NotImplementedError("Link cannot be set synchronous at present - functionality dropped at present in favour of performance")
        super(linkage,self).__init__()
        self.source = source
        self.sink   = sink
        self.sourcebox = sourcebox
        self.sinkbox   = sinkbox
        self.passthrough = passthrough
        if pipewidth is not None:
           self.getSinkbox().setSize(pipewidth)
 
    def sourcePair(self):
        return self.source, self.sourcebox
 
    def sinkPair(self):
        return self.sink, self.sinkbox
    
    def getSourcebox(self):
        if self.passthrough==1:
            return self.source.inboxes[self.sourcebox]
        else:
            return self.source.outboxes[self.sourcebox]
        
    def getSinkbox(self):
        if self.passthrough==2:
            return self.sink.outboxes[self.sinkbox]
        else:
            return self.sink.inboxes[self.sinkbox]
 
    def __str__(self):
        return "Link( source:[" + self.source.name + "," + self.sourcebox + "], sink:[" + self.sink.name + "," + self.sinkbox + "] )"

    def setSynchronous(self, pipewidth = None):
        self.getSinkbox().setSize(pipewidth)
        return self.getSinkbox().getSize()

    def setShowTransit(self, showtransit, tag):
        self.getSinkbox().setShowTransit(showtransit, tag)


if __name__ == '__main__':
   print "This code current has no test code"
