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
# WARNING: UNTESTED (initial integration of two _working and tested_
# components however)
#

import socket
import Axon

class Multicast_transreceiver(Axon.Component.component):
   def __init__(self, local_addr, local_port, remote_addr, remote_port):
       self.__super.__init__()
       self.local_addr = local_addr   # Multicast address we join
       self.local_port = local_port   # and port
       self.remote_addr = remote_addr # Multicast address we send to (may be same)
       self.remote_port = remote_port # and port.

    def __init__(self, address, port):
       self.__super.__init__()
       self.mcast_addr = address
       self.port = port

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.local_addr,self.local_port)) # Receive from server on this port

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        status = sock.setsockopt(socket.IPPROTO_IP,
                                 socket.IP_ADD_MEMBERSHIP,
                                 socket.inet_aton(self.local_addr) + socket.inet_aton("0.0.0.0"))

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
           if self.dataReady("inbox"):
              data = self.recv()
              l = sock.sendto(data, (self.remote_addr,self.remote_port) );

def tests():
   print "Needs test harness. This is a modified version of the"
   print "sender/receiver so a test harness should follow the same"
   print "sort of structure."

if __name__=="__main__":

    tests()
5~     