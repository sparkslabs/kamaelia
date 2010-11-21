#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
========
Linkages
========

Components only have input & output boxes. For data to get from a producer
(eg a file reader) to a consumer (eg an encryption component) then the output
of one component, the source component, must be linked to the input of
another component, the sink component.

* linkage objects are handles describing a linkage from one postbox to another
* Axon.Postoffice.postoffice creates and destroys linkages

All components have a postoffice object, this performs the creation and
destruction of linkages. Ask it for a linkage between inboxes and outboxes and
a linkage object is returned as a handle describing the linkage. When a message
is sent to an outbox, it is immediately delivered along linkage(s) to the
destination inbox.

This is *not* the usual technique for software messaging. Normally you create
messages, addressed to something specific, and then the message handler delivers
them.

However the method of communication used here is the norm for *hardware* systems,
and generally results in very pluggable components - the aim of this system,
hence this design approach rather than the normal. This method of
communication is also the norm for one form of software system - unix shell
scripting - something that has shown itself time and again to be used in ways
the inventors of programs/components never envisioned.

"""
import time

from AxonExceptions import AxonException, ArgumentsClash
from Axon import AxonObject
import Box
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
#        if synchronous is not None:
#            raise NotImplementedError("Link cannot be set synchronous at present - functionality dropped at present in favour of performance")
        super(linkage,self).__init__()
        self.source = source
        self.sink   = sink
        self.sourcebox = sourcebox
        self.sinkbox   = sinkbox
        self.passthrough = passthrough
        if pipewidth is not None:
           self.getSinkbox().setSize(pipewidth)
        else:
           if synchronous is not None:
               self.getSinkbox().setSize(1) # Restore functionality

        if Box.ShowAllTransits:
            self.getSinkbox().storage.tag = self.short_str()
 
    def sourcePair(self):
        """Returns (component,boxname) tuple describing where this linkage goes from"""
        return self.source, self.sourcebox
 
    def sinkPair(self):
        """Returns (component,boxname) tuple describing where this linkage goes to"""
        return self.sink, self.sinkbox
    
    def getSourcebox(self):
        """Returns the box object that this linkage goes from."""
        if self.passthrough==1:
            return self.source.inboxes[self.sourcebox]
        else:
            try:
                return self.source.outboxes[self.sourcebox]
            except KeyError:
                import time
                print "Linkage isn't being made correctly - does the following component"
                print "have a comma trailing it in the linkage description?"
                print self.source
                time.sleep(3)
                raise
        
    def getSinkbox(self):
        """Returns the box object that this linkage goes to."""
        if self.passthrough==2:
            return self.sink.outboxes[self.sinkbox]
        else:
            return self.sink.inboxes[self.sinkbox]
 
    def __str__(self):
        return "Link( source:[" + self.source.name + "," + self.sourcebox + "], sink:[" + self.sink.name + "," + self.sinkbox + "] )"

    def short_str(self):
        return "(%s,%s):(%s,%s)" % tuple([ X[X.rfind(".")+1:] for X in (self.source.name, self.sourcebox, self.sink.name , self.sinkbox)])

    def setSynchronous(self, pipewidth = None):
        """\
        Legacy method for setting the size limit on a linkage. Instead it sets
        the size limit for the destination inbox. A pipewidth of None specifies
        that there should be no limit.
        
        This method is likely to be deprecated soon.
        """
        # should this be deprecated?
        self.getSinkbox().setSize(pipewidth)
        return self.getSinkbox().getSize()

    def setShowTransit(self, showtransit, tag):
        """\
        Set showTransit to True to cause debugging output whenever a message is
        delivered along this linkage. The tag can be anything you want to
        identify this occurrence.
        """
        self.getSinkbox().setShowTransit(showtransit, tag)


if __name__ == '__main__':
   print "This code current has no test code"
