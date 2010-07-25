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
========================
Non-blocking DNS lookups
========================

This component will process DNS requests, using the blocking syscall
gethostbyname(). It will take hostnames recieved on "inbox" and puts a tuple of
(hostname, ip) in "outbox". In the event of a failure, the specific message will
be placed on "signal" in the form (hostname, error code).

Example Usage
-------------

Type hostnames, and they will be resolved and printed out::

    Pipeline(
        ConsoleReader(">>> ", ""),
        GetHostByName(),
        ConsoleEchoer(),
    ).run()


How does it work?
-----------------

The gethostbyname() syscall is a blocking one, and its use unmodified in a
kamaelia system can be a problem. This threadedcomponent processes requests and
can block without problems. Note that although all requests are processed
sequentially, this may not always be the case, and should not be relied on,
hence returning the hostname along with the IP address.

If this component recieves producerFinished or shutdown on the "signal" inbox, 
it will emit a producerFinished on the "control" outbox, and shut down.
"""

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess
import socket

class GetHostByName(threadedcomponent):
    def __init__(self, oneShot = False):
        self.oneShot = oneShot
        super(GetHostByName, self).__init__()

    def doLookup(self, data): 
        try: hostname = socket.gethostbyname(data)
        except socket.gaierror, e:
            self.send((data, e[1]), "signal")
        else: self.send((data, hostname), "outbox")

    def main(self):
        if self.oneShot:
            self.doLookup(self.oneShot)
            self.send(producerFinished(self), "signal")
            return
        while True:
            while self.dataReady("inbox"):
                returnval = self.doLookup(self.recv("inbox"))
                if returnval != None:
                    self.send(returnval, "outbox")
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(producerFinished(self), "signal")
                    return
            self.pause()

__kamaelia_components__  = ( GetHostByName, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    Pipeline(ConsoleReader(">>> ", ""),GetHostByName(),ConsoleEchoer()).run()