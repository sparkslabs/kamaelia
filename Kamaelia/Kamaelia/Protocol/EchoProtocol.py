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
"""
====================
Simple Echo Protocol
====================

A simple protocol component that echoes back anything sent to it.

It simply copies its input to its output.



Example Usage
-------------

A simple server that accepts connections on port 1501, echoing back anything sent
to it::

    >>> SimpleServer(protocol=EchoProtocol, port=1501).run()

On a unix/linux client::

    > telnet <server ip> 1501
    Trying <server ip>...
    Connected to <server ip>...
    hello world, this will be echoed back when I press return (newline)
    hello world, this will be echoed back when I press return (newline)
    oooh, thats nice!
    oooh, thats nice!



How does it work?
-----------------

The component receives data on its "inbox" inbox and immediately copies it to
its "outbox" outbox.

If any message is received on its "control" inbox, the component passes the message
onto its "signal" outbox and terminates.
"""

from Axon.Component import component

class EchoProtocol(component):
   """\
   EchoProtocol() -> new EchoProtocol component

   Simple component that copies anything sent to its "inbox" inbox to its "outbox"
   outbox.
   """
   def main(self):
       while not self.dataReady("control"):
           for message in self.Inbox("inbox"):
               self.send(message, "outbox")
           if not self.anyReady():
               self.pause()
           yield 1
       self.send(self.recv("control"), "signal")

__kamaelia_components__  = ( EchoProtocol, )


if __name__ == '__main__':
   from Kamaelia.Chassis.ConnectedServer import SimpleServer

   SimpleServer(protocol=EchoProtocol, port=1501).run()
