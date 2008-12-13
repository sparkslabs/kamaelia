#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import Axon

class SimpleDetupler(Axon.Component.component):
    """
This class expects to recieve tuples (or more accurately
indexable objects) on its inboxes. It extracts the item
tuple[index] from the tuple (or indexable object) and
passes this out its outbox.

This component does not terminate.

This component was originally created for use with the
multicast component. (It could however be used for
extracting a single field from a dictionary like object).

Example usage:

pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    detuple(1), # Extract data, through away sender
    SRM_Receiver(),
    detuple(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()

"""
    def __init__(self, index):
        super(SimpleDetupler, self).__init__()
        self.index = index
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                tuple=self.recv("inbox")
                self.send(tuple[self.index], "outbox")
            if not self.anyReady():
                self.pause()
            yield 1

__kamaelia_components__  = ( SimpleDetupler, )

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    class TupleSauce(Axon.Component.component):
        def main(self):
            while 1:
                self.send( ("greeting", "hello", "world"), "outbox")
                yield 1

    class CheckResultIsHello(Axon.Component.component):
        def main(self):
            while 1:
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    if data != "hello":
                        print "WARNING: expected", "hello", "received", data
                yield 1

    pipeline(
        TupleSauce(),
        SimpleDetupler(1),
        CheckResultIsHello(),
    ).run()
