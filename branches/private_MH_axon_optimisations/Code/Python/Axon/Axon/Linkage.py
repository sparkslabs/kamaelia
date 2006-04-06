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

These need to be registered with a postman (see below) who takes messages
from the outputs and delivers them to the appropriate destination. This is NOT
the usual technique for software messaging. Normally you create messages,
addressed to something specific, and then the message handler delivers them.

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
    def __init__(self, source, sink, passthrough=0):
        super(linkage,self).__init__()
        (sourcecomp,sourcebox) = source
        (sinkcomp,sinkbox) = sink
        self.source = sourcecomp
        self.sink   = sinkcomp
        self.sourcebox = sourcebox
        self.sinkbox   = sinkbox
        self.passthrough = passthrough
        
        if passthrough==0:
            self.src = sourcecomp.outboxes[sourcebox]
            self.dst = sinkcomp.inboxes[sinkbox]
        elif passthrough==1:
            self.src = sourcecomp.inboxes[sourcebox]
            self.dst = sinkcomp.inboxes[sinkbox]
        elif passthrough==2:
            self.src = sourcecomp.outboxes[sourcebox]
            self.dst = sinkcomp.outboxes[sinkbox]
        else:
            raise "passthrough value wrong"


    def sourcePair(self):
        return self.source, self.sourcebox
 
    def sinkPair(self):
        return self.sink, self.sinkbox
 
    def __str__(self):
        return "Link( source:[" + self.source.name + "," + self.sourcebox + "], sink:[" + self.sink.name + "," + self.sinkbox + "] )"

if __name__ == '__main__':
   print "This code current has no test code"
