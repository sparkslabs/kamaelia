#!/usr/bin/python
"""
Splitting server. This expects a single inbound connection on one port and spits it out to all recipients who connect on another port. This can be
used as an alternate server for the TCPRelayMulticast to connect to, and
it would expect to be fed using MulticastTCPClientRelay.

"""

from Kamaelia.Util.Backplane import Backplane, publishTo, subscribeTo
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.SingleServer import SingleServer
from config import tcp_tcp_splitter_port, tcp_splitter_client_port

p = Backplane("Splitting").activate()

pipeline(
    SingleServer( tcp_tcp_splitter_port ),
    publishTo("Splitting"),
).activate()

def SubscribeToSplitData(): # Protocol handler for each connected client
     return subscribeTo("Splitting")

SimpleServer( SubscribeToSplitData, tcp_splitter_client_port).run()
