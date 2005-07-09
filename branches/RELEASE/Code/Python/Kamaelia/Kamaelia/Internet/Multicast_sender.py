#!/usr/bin/python
#
# Simple Multicast sender - takes any data received on the component's inbox
# and sends to the multicast group previously specified.
#

import socket
import Axon

class Multicast_sender(Axon.Component.component):
   def __init__(self, local_addr, local_port, remote_addr, remote_port):
       super(Multicast_sender, self).__init__()
       self.local_addr = local_addr
       self.local_port = local_port
       self.remote_addr = remote_addr
       self.remote_port = remote_port

   def main(self):
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
       sock.bind((self.local_addr,self.local_port))
       sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
       while 1:
          if self.dataReady("inbox"):
             data = self.recv()
             l = sock.sendto(data, (self.remote_addr,self.remote_port) );
          yield 1

def tests():
   print "This module is acceptance tested as part of a system."
   print "Please see the test/test_BasicMulticastSystem.py script instead"

if __name__=="__main__":

    tests()
     