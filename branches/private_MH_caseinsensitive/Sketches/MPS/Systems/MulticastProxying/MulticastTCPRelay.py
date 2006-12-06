#!/usr/bin/python
"""
This is a simple proxy to relay multicast data from a given multicast
group and port as a TCP Service on a given port. It's worth noting that
this is one way - any data from the TCP connection is discarded.
"""

from Kamaelia.Util.Backplane import Backplane, publishTo, subscribeTo
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline
from config import mcast_group, mcast_port, mcast_tcp_splitter_port

p = Backplane("MulticastProxy").activate()


pipeline(
   Multicast_transceiver("0.0.0.0", mcast_port, mcast_group, 0),
   publishTo("MulticastProxy"),
).activate()

def RelayMulticastData(): # Protocol handler for each connected client
     return subscribeTo("MulticastProxy")

SimpleServer( RelayMulticastData, mcast_tcp_splitter_port).run()
