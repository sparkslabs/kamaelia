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
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.ConsoleEcho import consoleEchoer

   class testComponent(Axon.Component.component):
      def main(self):
        receiver = Multicast_receiver("224.168.2.9", 1600)
        display = consoleEchoer()

        self.link((receiver,"outbox"), (display,"inbox"))
        self.addChildren(receiver, display)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           self.pause()
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0.1)

if __name__=="__main__":

    tests()
