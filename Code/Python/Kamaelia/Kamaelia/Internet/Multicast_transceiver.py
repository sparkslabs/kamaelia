#!/usr/bin/python
#
# Simple Multicast transceiver
#
# Listens for packets in the given multicast group. Any data received is
# sent to the receiver's outbox. The logic here is likely to be not quite
# ideal. When complete though, this will be preferable over the sender and
# receiver components since it models what multicast really is rather than
# what people tend to think it is.
#
# See test/test_MulticastTransceiverSystem.py for how to build senders and
# receivers that use the transciever.
#

import socket
import Axon

class Multicast_transceiver(Axon.Component.component):
   def __init__(self, local_addr, local_port, remote_addr, remote_port):
       super(Multicast_transceiver, self).__init__()
       self.local_addr = local_addr   # Multicast address we join
       self.local_port = local_port   # and port
       self.remote_addr = remote_addr # Multicast address we send to (may be same)
       self.remote_port = remote_port # and port.

   def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.local_addr,self.local_port)) # Receive from server on this port

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

        status = sock.setsockopt(socket.IPPROTO_IP,
                                    socket.IP_ADD_MEMBERSHIP,
                                    socket.inet_aton(self.remote_addr) + socket.inet_aton("0.0.0.0"))

        sock.setblocking(0)
        tosend = []
        while 1:
           try:
              data, addr = sock.recvfrom(1024)
           except socket.error, e:
              pass
           else:
              message = (addr, data)
              self.send(message,"outbox")
           yield 1
           if self.dataReady("inbox"):
              data = self.recv()
              tosend.append(data)
              try:
                  l = sock.sendto(tosend[0], (self.remote_addr,self.remote_port) );
                  del tosend[0]
              except socket.error, e:
                  # Just keep trying next time
                  pass

def tests():
   print "This module is acceptance tested as part of a system."
   print "Please see the test/test_MulticastTransceiverSystem.py script instead"

if __name__=="__main__":

    tests()
