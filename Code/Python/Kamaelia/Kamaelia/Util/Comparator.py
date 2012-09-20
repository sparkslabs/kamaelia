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
==========================
Comparing two data sources
==========================

The Comparator component tests two incoming streams to see if the items they
contain match (pass an equality test).



Example Usage
-------------
Compares contents of two files and prints "MISMATCH!" whenever one is found::

    class DetectFalse(component):
        def main(self):
            while 1:
                yield 1
                if self.dataReady("inbox"):
                    if not self.recv("inbox"):
                        print ("MISMATCH!")

    Graphline( file1   = RateControlledFileReader(filename="file 1", ...),
               file2   = RateControlledFileReader(filename="file 2", ...),
               compare = Comparator(),
               fdetect = DetectFalse(),
               output  = ConsoleEchoer(),
               linkages = {
                   ("file1","outbox") : ("compare","inA"),
                   ("file2","outbox") : ("compare","inB"),
                   ("compare", "outbox") : ("fdetect", "inbox"),
                   ("fdetect", "outbox") : ("output", "inbox"),
               },
             ).run()



How does it work?
-----------------

The component simply waits until there is data ready on both its "inA" and "inB"
inboxes, then takes an item from each and compares them. The result of the
comparison is sent to the "outbox" outbox.

If data is available at neither, or only one, of the two inboxes, then the
component will wait indefinitely until data is available on both.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox, then a producerFinished message is sent out of the "signal"
outbox and the component terminates.

The comparison is done by the combine() method. This method returns the result
of a simple equality test of the two arguments.

You could always subclass this component and reimplement the combine() method to
perform different functions (for example, an 'adder').

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Comparator(component):
    """\
    Comparator() -> new Comparator component.

    Compares items received on "inA" inbox with items received on "inB" inbox.
    For each pair, outputs True if items compare equal, otherwise False.
    """
                        
    Inboxes = { "inbox"   : "NOT USED",
                "control" : "NOT USED",
                "inA"     : "Source 'A' of items to compare",
                "inB"     : "Source 'B' of items to compare",
              }
    Outboxes = { "outbox" : "Result of comparison",
                 "signal" : "NOT USED",
               }
    
    
    def combine(self, valA, valB):
        """\
        Returns result of (valA == valB)
        
        Reimplement this method to change the type of comparison from equality testing.
        """
        return valA == valB
    
    def mainBody(self):
        """Main loop body."""
        if self.dataReady("inA") and self.dataReady("inB"):
            self.send(self.combine(self.recv("inA"),self.recv("inB")))
        if self.dataReady("control"):
            mes = self.recv("control")
            if isinstance(mes, shutdownMicroprocess) or isinstance(mes,producerFinished):
                self.send(producerFinished(), "signal")
                return 0
        return 1

import Kamaelia.Support.Deprecate as Deprecate

comparator = Deprecate.makeClassStub(
    Comparator,
    "Use Kamaelia.Util.Comparator:Comparator instead of Kamaelia.Util.Comparator:comparator",
    "WARN"
    )

__kamaelia_components__  = ( Comparator, )
