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
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1
        
    def main(self):
        """Main loop."""
        while self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                entupled = self.prefix + [data] + self.postfix
                self.send( entupled, "outbox" )
            self.pause()
            yield 1

