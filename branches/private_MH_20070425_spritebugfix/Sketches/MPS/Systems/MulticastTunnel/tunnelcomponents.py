#!/usr/bin/python
#
# Sketches of components needed for joining multicast islands together.
#
# Issue with the tunnel endpoint is any data recieved isn't detupled before
# being sent, which probably isn't what we want.
#
# If the code looks familiar, it's essentially the code from examples 3 and 4
#
# ==UNTESTED== (and expected non-working)
#

#
# First the tunneled multicast group and port
#
tunnelled_group = "224.168.2.9"
tunnelled_port = 2500


##########################################################################
#
# TCP Server to multicast components
#
# This needs work - largely because whilst it detunnels data correctly, 
# I'm pretty certain it's not tunneling data from the outside world
# correctly.
#


def AdHocSpecificDetupledMulticastTransceiver(destination_group, destination_port):
   class klass(_Axon.Component.component):
      def main(self):
         transceiver = Multicast_transceiver("0.0.0.0", destination_port, destination_group, destination_port)
         detupler = detuple(1)
         
         self.link((transceiver,"outbox"), (detupler,"inbox"))
         self.link((detupler,"outbox"), (self,"outbox"), passthrough=2)
         self.link((self,"inbox"), (transceiver,"inbox"), passthrough=1)

         self.addChildren(transceiver, detupler)
         yield _Axon.Ipc.newComponent(*(self.children))

         while 1:
            self.pause()
            yield 1
   return klass

class Multicast_Tunnel_EndPoint(_Axon.Component.component):
   def main(self):
      import random
      clientServerTestPort=1500

      server=SimpleServer(protocol=AdHocSpecificDetupledMulticastTransceiver(tunnelled_group, tunnelled_port), 
                           port=clientServerTestPort)

      self.addChildren(server)
      yield _Axon.Ipc.newComponent(*(self.children))

      while 1:
         self.pause()
         yield 1

##########################################################################
#
# Multicast to TCP Client components
#
# This looks correct, but needs validation.
#
# Listens on a multicast address, sends all data received over a TCP
# connection to an endpoint. Any data received over the TCP connection is
# retransmitted over the multicast group. This essentially forms a NAT for
# the multicast session.
#
# This will be more generally useful as software we can just give people for
# bypassing the lack of multicast deployment over the internet. (Hmm...
# Thinking about it, this also relieves the more general issues with routing
# since explicit network joins in this manner mean that not everyone needs WAN
# based multicast enabled)
#
# In a fun way this will also allow companies to join a BBC multicast
# group...
#
class detuple(Axon.Component.component):
   def __init__(self, index):
      self.__super.__init__()
      self.index = index

   def main(self):
      while 1:
         if self.dataReady("inbox"):
            tuple=self.recv("inbox")
            self.send(tuple[self.index], "outbox")
         yield 1

def tunnel_start():
   from Axon.Scheduler import scheduler

   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class Multicast_Tunnel_StartPoint((Axon.Component.component):
      def main(self):

        multicast_tunnel_endpoint = "132.185.0.0"
        multicast_tunnel_endport = 2500
        local_multicast_group = "224.168.2.9"
        local_multicast_port = 1600

        multicast_receiver = Multicast_transceiver("0.0.0.0", local_multicast_port, local_multicast_group, local_multicast_port)
        detupler = detuple(1)
        tunnel_client=TCPClient(multicast_tunnel_endpoint, multicast_tunnel_endport)

        self.link((multicast_receiver,"outbox"), (detupler,"inbox"))
        self.link((detupler,"outbox"), (tunnel_client,"inbox"))
        self.link((tunnel_client,"outbox"), (multicast_receiver,"inbox"))

        self.addChildren(multicast_receiver, detupler, tunnel_client)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           yield 1

   harness = Multicast_Tunnel_StartPoint()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":
    tunnel_start()
