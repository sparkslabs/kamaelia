!/usr/bin/python
#
# Simple udp /multicast/ sender and receiver
# Logically these map to being a single component each
#

import socket
import time
import Axon

class Chargen(Axon.Component.component):
   def main(self):
      while 1:
         self.send("Hello World", "outbox")
         yield 1
 
class Multicast_sender(Axon.Component.component):
   def __init__(self, local_addr, local_port, remote_addr, remote_port):
       self.__super.__init__()
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
        ts = time.time()
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

   ANY = "0.0.0.0"
   ANYPORT = 0
   MCAST_ADDR = "224.168.2.9"
   MCAST_PORT = 1600

   class testComponent(Axon.Component.component):
      def main(self):
        chargen= Chargen()
        sender = Multicast_sender(ANY, ANYPORT, MCAST_ADDR, MCAST_PORT)
        receiver = Multicast_receiver(MCAST_ADDR, MCAST_PORT)
        display = consoleEchoer()

        self.link((chargen,"outbox"), (sender,"inbox"))
        self.link((receiver,"outbox"), (display,"inbox"))
        self.addChildren(chargen, sender, receiver, display)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           self.pause()
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0.1)

if __name__=="__main__":

    tests()
     