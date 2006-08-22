#!/usr/bin/python
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
============================
Simple multicast transceiver
============================

A simple component for transmitting and receiving multicast packets.

Remember that multicast is an unreliable connection - packets may be lost,
duplicated or reordered. 



Example Usage
-------------

Send a file to, and receive data from multicast group address 1.2.3.4 port 1000::

    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_transceiver("0.0.0.0", 0, "1.2.3.4", 1000),
            ).activate()

    Pipeline( Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 0)
              consoleEchoer()
            ).activate()

Or::
    
    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 1000),
              consoleEchoer()
            ).activate()

The data emitted by Multicast_transciever (and displayed by consoleEchoer) is of
the form (source_address, data).



More detail
-----------

Data sent to the component's "inbox" inbox is sent to the multicast group.

Data received from the multicast group is emitted as a tuple:
(source_addr, data) where data is a string of the received data.

This component ignores anything received on its "control" inbox. It is not yet
possible to ask it to shut down. It does not terminate.

Multicast groups do not 'shut down', so this component never emits any signals
on its "signal" outbox.



Why a transciever component?
----------------------------
Listens for packets in the given multicast group. Any data received is
sent to the receiver's outbox. The logic here is likely to be not quite
ideal. When complete though, this will be preferable over the sender and
receiver components since it models what multicast really is rather than
what people tend to think it is.
"""

import socket
import Axon

class Multicast_transceiver(Axon.Component.component):
   """\
   Multicast_transciever(local_addr, local_port, remote_addr, remote_port) -> component that send and receives data to/from a multicast group.
    
   Creates a component that sends data received on its "inbox" inbox to the
   specified multicast group; and sends to its "outbox" outbox tuples of the
   form (src_addr, data) containing data received.
   
   Keyword arguments:
   - local_addr   -- local address (interface) to send from (string)
   - local_port   -- port number
   - remote_addr  -- address of multicast group (string)
   - remote_port  -- port number
   """
    
   Inboxes  = { "inbox"   : "Data to be sent to the multicast group",
                "control" : "NOT USED",
              }
   Outboxes = { "outbox" : "Emits (src_addr, data_received)",
                "signal" : "NOT USED",
              }

   def __init__(self, local_addr, local_port, remote_addr, remote_port, debug=False):
       """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
       super(Multicast_transceiver, self).__init__()
       self.local_addr = local_addr   # Multicast address we join
       self.local_port = local_port   # and port
       self.remote_addr = remote_addr # Multicast address we send to (may be same)
       self.remote_port = remote_port # and port.
       self.debug = debug

   def main(self):
        """Main loop"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.local_addr,self.local_port)) # Receive from server on this port

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

        status = sock.setsockopt(socket.IPPROTO_IP,
                                    socket.IP_ADD_MEMBERSHIP,
                                    socket.inet_aton(self.remote_addr) + socket.inet_aton("0.0.0.0"))

        sock.setblocking(0)

        # This buffer collects data to be sent
        tosend = []
        while 1:
           try:
              data, addr = sock.recvfrom(16384)
           except socket.error, e:
              pass
           else:
              message = (addr, data)
              self.send(message,"outbox")
           yield 1

           while self.dataReady("inbox"):
              data = self.recv()
              tosend.append(data)

           if self.debug:
              print self.inboxes["inbox"]

           while len(tosend)>0:
              try:
                  l = sock.sendto(tosend[0], (self.remote_addr,self.remote_port) );
                  del tosend[0]
              except socket.error, e:
                  # break out the loop, since we can't send right now
                  break

def tests():
   print "This module is acceptance tested as part of a system."
   print "Please see the test/test_MulticastTransceiverSystem.py script instead"

__kamaelia_components__  = ( Multicast_transceiver, )


if __name__=="__main__":

    tests()
