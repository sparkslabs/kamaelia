---
pagename: Components/pydoc/Kamaelia.Internet.UDP_ng
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}
===============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PostboxPeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.PostboxPeer.html){.reference}**
-   **component
    [SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.SimplePeer.html){.reference}**
-   **component
    [TargettedPeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.TargettedPeer.html){.reference}**
-   **component
    [UDPReceiver](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPReceiver.html){.reference}**
-   **component
    [UDPSender](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPSender.html){.reference}**
:::

-   [Simple UDP components](#145){.reference}
    -   [Example Usage](#146){.reference}
    -   [Behaviour](#147){.reference}
    -   [Implementation Details](#148){.reference}
:::

::: {.section}
Simple UDP components {#145}
=====================

These components provide simple support for sending and receiving UDP
packets.

NOTE: This set of components really an evolution of those in UDP.py, and
is likely to replace those in future.

::: {.section}
[Example Usage]{#example-usage} {#146}
-------------------------------

Send console input to port 1500 of myserver.com and receive packets
locally on port 1501 displaying their contents (and where they came
from) on the console:

``` {.literal-block}
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Internet.UDP import SimplePeer

Pipeline( ConsoleReader(),
          SimplePeer("127.0.0.1", 1501, "myserver.com", 1500),
          ConsoleEchoer(),
        ).run()
```

Sends data from a data source as UDP packets, changing between 3
different destinations, once per second:

``` {.literal-block}
class DestinationSelector(component):
    def main(self):
        while 1:
            for dest in [ ("server1.com",1500),
                          ("server2.com",1500),
                          ("server3.com",1500), ]:
                self.send(dest,"outbox")
            next=time.time()+1.0
            while time.time() < next:
                yield 1

Graphline(         SOURCE = MyDataSource(),
    SELECT = DestinationSelector(),
    UDP    = TargettedPeer(),
    linkages = {
        ("SOURCE", "outbox") : ("UDP", "inbox"),
        ("SELECT", "outbox") : ("UDP", "target"),
    }
).run()
```

Send UDP packets containing \"hello\" to several different servers, all
on port 1500:

``` {.literal-block}
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Internet.UDP import PostboxPeer

Pipeline(
    DataSource( [ ("myserver1.com",1500,"hello"),
                  ("myserver2.com",1500,"hello"),
                  ("myserver3.com",1500,"hello"),
                ]
                ),
    PostboxPeer(),
).run()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#147}
-----------------------

When any of these components receive a UDP packet on the local address
and port they are bound to; they send out a tuple (data,(host,port)) out
of their \"outbox\" outboxes. \'data\' is a string containing the
payload of the packet. (host,port) is the address of the
sender/originator of the packet.

SimplePeer is the simplest to use. Any data sent to its \"inbox\" inbox
is sent as a UDP packet to the destination (receiver) specified at
initialisation.

UDPSender and UDPReceiver duplicate the sending and receiving
functionality of SimplePeer in seperate components.

TargettedPeer behaves identically to SimplePeer; however the destination
(receiver) it sends UDP packets to can be changed by sending a new
(host,port) tuple to its \"target\" inbox.

PostboxPeer does not have a fixed destination (receiver) to which it
sends UDP packets. Send (host,port,data) tuples to its \"inbox\" inbox
to arrange for a UDP packet containing the specified data to be sent to
the specified (host,port).

All of the components shutdown upon receiving a ShutdownMicroprocess
message on their \"control\" inbox. UDPSender also shuts down upon
receiving a ProducerFinished message on its \"control\" inbox. In this
case before it shuts down it sends any data in its send queue, and any
data waiting on its inbox.
:::

::: {.section}
[Implementation Details]{#implementation-details} {#148}
-------------------------------------------------

All of the UDP components are all derived from the base class BasicPeer.
BasicPeer provides some basic code for sending and receiving from a
socket.

Although technically BasicPeer is a component, it is not a usable one as
it does not implement a main() method.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}.[PostboxPeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.PostboxPeer.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class PostboxPeer(BasicPeer) {#symbol-PostboxPeer}
----------------------------

PostboxPeer(\[localaddr\]\[,localport\]) -\> new PostboxPeer component.

A simple component for receiving and transmitting UDP packets. It binds
to the specified local address and port - from which it will receive
packets. Sends packets to individually specified destinations

Arguments:

-   localaddr \-- Optional. The local addresss (interface) to bind to.
    (default=\"0.0.0.0\")
-   localport \-- Optional. The local port to bind to. (default=0)

::: {.section}
### [Inboxes]{#symbol-PostboxPeer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PostboxPeer.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, localaddr\]\[, localport\])]{#symbol-PostboxPeer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-PostboxPeer.main}

Main loop
:::

::: {.section}
#### [sendLoop(self)]{#symbol-PostboxPeer.sendLoop}

Safely send any data stored in the send buffer or waiting on the
\"inbox\" inbox
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP\_ng.BasicPeer :

-   [setupSelector](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.setupSelector){.reference}(self)
-   [safeBind](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeBind){.reference}(self,
    target)
-   [safeSend](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeSend){.reference}(self,
    data, target)
-   [recvLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.recvLoop){.reference}(self)
-   [safeRecv](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeRecv){.reference}(self,
    size)
:::
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}.[SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.SimplePeer.html){.reference}
====================================================================================================================================================================================================================================================================================

::: {.section}
class SimplePeer(BasicPeer) {#symbol-SimplePeer}
---------------------------

SimplePeer(\[localaddr\]\[,localport\]\[,receiver\_addr\]\[,receiver\_port\])
-\> new SimplePeer component.

A simple component for receiving and transmitting UDP packets. It binds
to the specified local address and port - from which it will receive
packets and sends packets to a receiver on the specified address and
port.

Arguments:

-   localaddr \-- Optional. The local addresss (interface) to bind to.
    (default=\"0.0.0.0\")
-   localport \-- Optional. The local port to bind to. (default=0)
-   receiver\_addr \-- Optional. The address the receiver is bound to -
    to which packets will be sent. (default=\"0.0.0.0\")
-   receiver\_port \-- Optional. The port the receiver is bound on - to
    which packets will be sent. (default=0)

::: {.section}
### [Inboxes]{#symbol-SimplePeer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimplePeer.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, localaddr\]\[, localport\]\[, receiver\_addr\]\[, receiver\_port\])]{#symbol-SimplePeer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-SimplePeer.main}

Main loop
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP\_ng.BasicPeer :

-   [setupSelector](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.setupSelector){.reference}(self)
-   [safeBind](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeBind){.reference}(self,
    target)
-   [sendLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.sendLoop){.reference}(self,
    target)
-   [safeSend](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeSend){.reference}(self,
    data, target)
-   [recvLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.recvLoop){.reference}(self)
-   [safeRecv](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeRecv){.reference}(self,
    size)
:::
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}.[TargettedPeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.TargettedPeer.html){.reference}
==========================================================================================================================================================================================================================================================================================

::: {.section}
class TargettedPeer(BasicPeer) {#symbol-TargettedPeer}
------------------------------

TargettedPeer(\[localaddr\]\[,localport\]\[,receiver\_addr\]\[,receiver\_port\])
-\> new TargettedPeer component.

A simple component for receiving and transmitting UDP packets. It binds
to the specified local address and port - from which it will receive
packets and sends packets to a receiver on the specified address and
port.

Can change where it is sending to by sending the new (addr,port)
receiver address to the \"target\" inbox.

Arguments:

-   localaddr \-- Optional. The local addresss (interface) to bind to.
    (default=\"0.0.0.0\")
-   localport \-- Optional. The local port to bind to. (default=0)
-   receiver\_addr \-- Optional. The address the receiver is bound to -
    to which packets will be sent. (default=\"0.0.0.0\")
-   receiver\_port \-- Optional. The port the receiver is bound on - to
    which packets will be sent. (default=0)

::: {.section}
### [Inboxes]{#symbol-TargettedPeer.Inboxes}

-   **control** : Recieve shutdown messages
-   **readReady** : Notify that there is incoming data ready on the
    socket
-   **inbox** : Data to sent to the socket
-   **writeReady** : Notify that the socket is ready to send
-   **target** : Data receieved here changes the receiver addr/port data
    is tuple form: (host, port)
:::

::: {.section}
### [Outboxes]{#symbol-TargettedPeer.Outboxes}

-   **outbox** : (data,(host,port)) tuples for each packet received
-   **signal** : Signals receiver is shutting down
-   **\_selectorSignal** : For communication to the selector
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, localaddr\]\[, localport\]\[, receiver\_addr\]\[, receiver\_port\])]{#symbol-TargettedPeer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-TargettedPeer.main}

Main loop
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP\_ng.BasicPeer :

-   [setupSelector](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.setupSelector){.reference}(self)
-   [safeBind](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeBind){.reference}(self,
    target)
-   [sendLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.sendLoop){.reference}(self,
    target)
-   [safeSend](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeSend){.reference}(self,
    data, target)
-   [recvLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.recvLoop){.reference}(self)
-   [safeRecv](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeRecv){.reference}(self,
    size)
:::
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}.[UDPReceiver](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPReceiver.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class UDPReceiver(BasicPeer) {#symbol-UDPReceiver}
----------------------------

UDPReceiver(\[localaddr\]\[,localport\]) -\> new UDPReceiver component.

A simple component for receiving UDP packets. It binds to the specified
local address and port - from which it will receive packets. Packets
received are sent to it \"outbox\" outbox.

Arguments:

-   localaddr \-- Optional. The local addresss (interface) to bind to.
    (default=\"0.0.0.0\")
-   localport \-- Optional. The local port to bind to. (default=0)

::: {.section}
### [Inboxes]{#symbol-UDPReceiver.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-UDPReceiver.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, localaddr\]\[, localport\])]{#symbol-UDPReceiver.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-UDPReceiver.main}

Main loop
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP\_ng.BasicPeer :

-   [setupSelector](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.setupSelector){.reference}(self)
-   [safeBind](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeBind){.reference}(self,
    target)
-   [sendLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.sendLoop){.reference}(self,
    target)
-   [safeSend](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeSend){.reference}(self,
    data, target)
-   [recvLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.recvLoop){.reference}(self)
-   [safeRecv](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeRecv){.reference}(self,
    size)
:::
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}.[UDPSender](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPSender.html){.reference}
==================================================================================================================================================================================================================================================================================

::: {.section}
class UDPSender(BasicPeer) {#symbol-UDPSender}
--------------------------

UDPSender(\[receiver\_addr\]\[,receiver\_port\]) -\> new UDPSender
component.

A simple component for transmitting UDP packets. It sends packets
received from the \"inbox\" inbox to a receiver on the specified address
and port.

Arguments:

-   receiver\_addr \-- Optional. The address the receiver is bound to -
    to which packets will be sent. (default=\"0.0.0.0\")
-   receiver\_port \-- Optional. The port the receiver is bound on - to
    which packets will be sent. (default=0)

::: {.section}
### [Inboxes]{#symbol-UDPSender.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-UDPSender.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, receiver\_addr\]\[, receiver\_port\])]{#symbol-UDPSender.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-UDPSender.main}

Main loop
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP\_ng.BasicPeer :

-   [setupSelector](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.setupSelector){.reference}(self)
-   [safeBind](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeBind){.reference}(self,
    target)
-   [sendLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.sendLoop){.reference}(self,
    target)
-   [safeSend](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeSend){.reference}(self,
    data, target)
-   [recvLoop](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.recvLoop){.reference}(self)
-   [safeRecv](/Components/pydoc/Kamaelia.Internet.UDP_ng.html#symbol-BasicPeer.safeRecv){.reference}(self,
    size)
:::
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
