#!/usr/bin/python
#
# Simple Multicast receiver - listens for packets in the given multicast
# group. Any data received is sent to the receiver's outbox.
#

import socket
import Axon

class Multicast_receiver(Axon.Component.component):
    def __init__(self, address, port):
       self.__super.__init__()
       self.mcast_addr = address
       self.port = port

    def main(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.mcast_addr,self.port)) # Specifically we want to receieve stuff
                                        # from server on this address.
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        status = sock.setsockopt(socket.IPPROTO_IP,
                                 socket.IP_ADD_MEMBERSHIP,
                                 socket.inet_aton(self.mcast_addr) + socket.inet_aton("0.0.0.0"))

        sock.setblocking(0)
        while 1:
           try:
              data, addr = sock.recvfrom(1024)
           except socket.error, e:
              pass
           else:
              message = (addr, data)
              self.send(message,"outbox")
           yield 1

def tests():
   print "This module is acceptance tested as part of a system."
   print "Please see the test/test_BasicMulticastSystem.py script instead"

if __name__=="__main__":

    tests()
