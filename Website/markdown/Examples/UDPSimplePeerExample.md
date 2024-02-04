---
pagename: Examples/UDPSimplePeerExample
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 13: How to build a simple system for sending data from a UDP
client to a UDP server. [Components used:
]{style="font-weight:600"}[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[Chargen](/Components/pydoc/Kamaelia.Util.Chargen.Chargen.html),
[ConsoleEchoer](/Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer.html),
[SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP.SimplePeer.html)

Simple Kamaelia Example that shows how to use a simple UDP Peer. A UDP
Peer actually sends and recieves however, so we could havemore fun
example here with the two peers sending each other messages.

It\'s worth noting that these aren\'t \"connected\" peers in any shape
or form, and they\'re fixed who they\'re sending to, etc, which is why
it\'s a simple peer.

```{.python}
#!/usr/bin/python

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
```

**Source:** Examples/example13/UDP_demo.py
