#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""/
============
Entuple data
============

Receives data on its "inbox" inbox; wraps that data inside a tuple, and outputs
that tuple from its "outbox" outbox.



Example Usage
-------------
Taking console input and sandwiching it in a tuple between the strings
("You" and "said") and ("just" and now")::
    
    Pipeline( ConsoleReader(),
              Entuple(prefix=["You","said"], postfix=["just","now"]),
              ConsoleEchoer(),
            ).run()

At runtime::
    >>> Hello there!
    ('You', 'said', 'Hello there!', 'just', 'now')



How does it work?
-----------------

At initialisation specify a list of items to be placed at the front (prefix) and
back (postfix) of the tuples that are output.

When an item of data is received at the "inbox" inbox; it is placed inside a
tuple, after the prefixes and before the postfixes. It is then immediately sent
out of the "outbox" outbox.

For example: if the prefix is [1,2,3] and the postfix is ['a','b'] and the item
of data that arrives is 'flurble' then (1,2,3,'flurble','a','b') will be sent to
the "outbox" outbox.

If Entuple receives a shutdownMicroprocess message on its "control" inbox, it
will pass it on out of the "signal" outbox. The component will then terminate.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Entuple(component):
    """\
    Entuple([prefix][,postfix]) -> new Entuple component.

    Component that takes data received on its "inbox" inbox and wraps it inside
    of a custom tuple; sending it out of its "outbox" outbox.

    Keyword arguments:
    - prefix  -- list of items to go at the front of the tuple (default=[])
    - postfix -- list of items to go at the back of the tuple (default=[])
    """
    def __init__(self, prefix=[], postfix=[]):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Entuple,self).__init__()
        self.prefix = prefix
        self.postfix = postfix
    
    def shutdown(self):
        """Returns True if a shutdown message is received. Forwards on any
        messages."""
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        """Main loop."""
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                entupled = self.prefix + [data] + self.postfix
                self.send( entupled, "outbox" )
            self.pause()
            yield 1

