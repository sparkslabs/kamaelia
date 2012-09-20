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

import Axon
from Axon.Ipc import shutdownMicroprocess, producerFinished

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

Example usage::

    Pipeline(
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
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                tuple=self.recv("inbox")
                self.send(tuple[self.index], "outbox")
            if not self.anyReady():
                self.pause()
            while self.dataReady("control"):
                msg=self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
            yield 1

__kamaelia_components__  = ( SimpleDetupler, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
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
                        print ("WARNING: expected", "hello", "received", data)
                yield 1

    Pipeline(
        TupleSauce(),
        SimpleDetupler(1),
        CheckResultIsHello(),
    ).run()
