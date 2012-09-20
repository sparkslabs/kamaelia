#!/usr/bin/python
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
=======================
Simple multicast sender
=======================

A simple component for sending data to a multicast group.

Remember that multicast is an unreliable connection - packets may be lost,
duplicated or reordered.



Example Usage
-------------

Multicasting a file to group address 1.2.3.4 on port 1000 (local address 0.0.0.0
port 0)::

    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_sender("0.0.0.0", 0, "1.2.3.4", 1000),
            ).activate()



More detail
-----------

Data sent to the component's "inbox" inbox is sent to the multicast group.

This component ignores anything received on its "control" inbox. It is not yet
possible to ask it to shut down. It does not terminate.

This component never emits any signals on its "signal" outbox.
"""

import socket
import Axon

class Multicast_sender(Axon.Component.component):
   """\
   Multicast_sender(local_addr, local_port, remote_addr, remote_port) -> component that sends to a multicast group.
    
   Creates a component that sends data received on its "inbox" inbox to the
   specified multicast group.
   
   Keyword arguments:
   
   - local_addr   -- local address (interface) to send from (string)
   - local_port   -- local port number
   - remote_addr  -- address of multicast group to send to (string)
   - remote_port  -- port number
   """
    
   Inboxes  = { "inbox"   : "Data to be sent to the multicast group",
                "control" : "NOT USED",
              }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "NOT USED",
              }

   def __init__(self, local_addr, local_port, remote_addr, remote_port):
       """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
       super(Multicast_sender, self).__init__()
       self.local_addr = local_addr
       self.local_port = local_port
       self.remote_addr = remote_addr
       self.remote_port = remote_port

   def main(self):
       """Main loop"""
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
       sock.bind((self.local_addr,self.local_port))
       sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
       while 1:
          if self.dataReady("inbox"):
             data = self.recv()
             l = sock.sendto(data, (self.remote_addr,self.remote_port) );
          yield 1

def tests():
   print ("This module is acceptance tested as part of a system.")
   print ("Please see the test/test_BasicMulticastSystem.py script instead")

__kamaelia_components__  = ( Multicast_sender, )


if __name__=="__main__":

    tests()
     