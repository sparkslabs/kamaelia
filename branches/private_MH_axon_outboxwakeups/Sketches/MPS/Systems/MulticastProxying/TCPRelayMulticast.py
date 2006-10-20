#!/usr/bin/python
"""
This is a simple proxy to relay data from a TCP Server out over multicast.
This is designed to be used with MulticastTCPRelay to allow tunnelling of
multicast over TCP in a single direction.
"""

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from config import multicast_group, multicast_port, mcast_tcp_splitter_ip, mcast_tcp_splitter_port

pipeline(
   TCPClient(mcast_tcp_splitter_ip, mcast_tcp_splitter_port),
   Multicast_transceiver("0.0.0.0", 0, multicast_group, multicast_port),
).activate()
