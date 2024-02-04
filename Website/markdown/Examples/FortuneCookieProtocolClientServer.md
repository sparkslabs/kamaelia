---
pagename: Examples/FortuneCookieProtocolClientServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size: 24pt; font-weight: 600;"}

[How can I\...?]{style="font-size: 18pt;"}

Example 1: Building a Simple TCP Based Server that allows multiple
connections at once and sends a fortune cookie to the client. Includes
simple TCP based client that displays the fortune cookie. 
[Components used: ]{style="font-weight: 600;"}[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html),
[FortuneCookieProtocol](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.FortuneCookieProtocol.html),
[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html),
[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html),
[ConsoleEchoer](/Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer.html)

```{.python}
#!/usr/bin/python

from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

import random

clientServerTestPort=random.randint(1500,1599)

SimpleServer(protocol=FortuneCookieProtocol, port=clientServerTestPort).activate ()

Pipeline(
         TCPClient("127.0.0.1",clientServerTestPort),
         ConsoleEchoer()
).run()
```

Source: Examples/example1/FortuneCookie_ServerClient.py

