#!/usr/bin/python
#
# Very simple Peer to peer radio player.
#
# We have essentially 2 trees constructed - a mesh construction tree and a data tree.
# There are therefore 2 ports for each peer:
#
# control port - request to connect. Either told to connect to a
#    new port number, or given a new ip/port to request to connect to
#
# data port - connecting to here gets you the data. Its good form
#    to ask on the control port first if you can connect there.
#
# As a result that's why there's two SimpleServer instances.
#

import Axon

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient

from likefile import *
background = schedulerThread().start()

class Echo(Axon.Component.component):
   def main(self):
      while 1:
          while self.dataReady("inbox"):
              self.send(self.recv("inbox"), "outbox")
          yield 1

SimpleServer(protocol=Echo, port=1600).activate()

time.sleep(1)

#
# We can then write code here to demo the use of likefile with TCPClient.
#
