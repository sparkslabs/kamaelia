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
                        print "MISMATCH!"

    Graphline( file1   = RateControlledFileReader(filename="file 1", ...),
               file2   = RateControlledFileReader(filename="file 2", ...),
               compare = Comparator(),
               fdetect = DetectFalse(),
               output  = consoleEchoer(),
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

__kamaelia_components__  = ( Comparator, )


class comparator(Comparator):
    """DEPRECATED"""
    pass
