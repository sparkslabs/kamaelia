#!/usr/bin/python
"""
This is a simple proxy to relay multicast data from a given multicast
group and port to a TCP server which may choose to do something with the
data (eg split and forward).
"""

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Internet.TCPClient import TCPClient
from config import mcast_group, mcast_port, mcast_tcp_splitter_port
from config import tcp_tcp_splitter_ip, tcp_tcp_splitter_port

pipeline(
   Multicast_transceiver("0.0.0.0", mcast_port, mcast_group, 0),
   TCPClient(tcp_tcp_splitter_ip, tcp_tcp_splitter_port),
).activate()

def RelayMulticastData(): # Protocol handler for each connected client
     return subscribeTo("MulticastProxy")

SimpleServer( RelayMulticastData, TCPPORT).run()
