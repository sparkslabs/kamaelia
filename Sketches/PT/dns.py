#!/usr/bin/env python

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

Type hostnames, and they will be resolved and printed out.

    pipeline(
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

"""
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdown
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
            self.doLookup(self, oneShot)
            self.send(producerFinished(self), "signal")
            return
        while True:
            while self.dataReady("inbox"):
                returnval = self.doLookup(self.recv("inbox"))
                if returnval != None:
                    self.send(returnval, "outbox")
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return
            self.pause()

__kamaelia_components__  = ( GetHostByName, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    Pipeline(ConsoleReader(">>> ", ""),GetHostByName(),ConsoleEchoer()).run()