#!/usr/bin/python
#
# Simple udp /multicast/ sender and receiver
# Logically these map to being a single component each
#

import socket
import time

ANY = "0.0.0.0"
SENDERPORT = 1501
MCAST_ADDR = "224.168.2.9"
MCAST_PORT = 1600

def datasource():
   while 1:
      yield "Hello World"

def sender(source):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((ANY,SENDERPORT))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
    while 1:
       time.sleep(0.7)
       data = source.next()
       l = sock.sendto(data, (MCAST_ADDR,MCAST_PORT) );
       print "sending...", time.time()
       yield l


def receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((MCAST_ADDR,MCAST_PORT)) # Specifically we want to receieve stuff
                                    # from server on this address.
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
    status = sock.setsockopt(socket.IPPROTO_IP,
                             socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY));

    sock.setblocking(0)
    ts = time.time()
    while 1:
       try:
          data, addr = sock.recvfrom(1024)
       except socket.error, e:
          pass
       else:
          print "We got data!"
          print "FROM: ", addr
          print "DATA: ", data
       yield 1

def tests():
   source= datasource()
   R = receiver()
   S = sender(source)
   while 1:
      S.next()
      R.next()

if __name__=="__main__":


    tests()
     