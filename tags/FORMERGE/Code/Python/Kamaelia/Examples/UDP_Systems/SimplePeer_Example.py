#!/usr/bin/python
"""
Simple Kamaelia Example that shows how to use a simple UDP Peer.
A UDP Peer actually sends and recieves however, so we could have
more fun example here with the two peers sending each other messages.

It's worth noting that these aren't "connected" peers in any shape
or form, and they're fixed who they're sending to, etc, which is why
it's a simple peer.
"""
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Chargen import Chargen
from Kamaelia.Internet.UDP import SimplePeer

server_addr = "127.0.0.1"
server_port = 1600

pipeline(
    Chargen(),
    SimplePeer(receiver_addr=server_addr, receiver_port=server_port),
).activate()

pipeline(
    SimplePeer(localaddr=server_addr, localport=server_port),
    ConsoleEchoer()
).run()
