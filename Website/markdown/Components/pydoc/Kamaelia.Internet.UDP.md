---
pagename: Components/pydoc/Kamaelia.Internet.UDP
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}
========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PostboxPeer](/Components/pydoc/Kamaelia.Internet.UDP.PostboxPeer.html){.reference}**
-   **component
    [SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP.SimplePeer.html){.reference}**
-   **component
    [TargettedPeer](/Components/pydoc/Kamaelia.Internet.UDP.TargettedPeer.html){.reference}**
:::

-   [Simple UDP components](#108){.reference}
    -   [Example Usage](#109){.reference}
    -   [Behaviour](#110){.reference}
    -   [Implementation Details](#111){.reference}
:::

::: {.section}
Simple UDP components {#108}
=====================

These components provide simple support for sending and receiving UDP
packets.

*Note* that this components are deemed somewhat experimental.

::: {.section}
[Example Usage]{#example-usage} {#109}
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
[Behaviour]{#behaviour} {#110}
-----------------------

When any of these components receive a UDP packet on the local address
and port they are bound to; they send out a tuple (data,(host,port)) out
of their \"outbox\" outboxes. \'data\' is a string containing the
payload of the packet. (host,port) is the address of the
sender/originator of the packet.

SimplePeer is the simplest to use. Any data sent to its \"inbox\" inbox
is sent as a UDP packet to the destination (receiver) specified at
initialisation.

TargettedPeer behaves identically to SimplePeer; however the destination
(receiver) it sends UDP packets to can be changed by sending a new
(host,port) tuple to its \"target\" inbox.

PostboxPeer does not have a fixed destination (receiver) to which it
sends UDP packets. Send (host,port,data) tuples to its \"inbox\" inbox
to arrange for a UDP packet containing the specified data to be sent to
the specified (host,port).

None of these components terminate. They ignore any messages sent to
their \"control\" inbox and do not send anything out of their \"signal\"
outbox.
:::

::: {.section}
[Implementation Details]{#implementation-details} {#111}
-------------------------------------------------

SimplePeer, TargettedPeer and PostboxPeer are all derived from the base
class BasicPeer. BasicPeer provides some basic code for receiving from a
socket.

Although technically BasicPeer is a component, it is not a usable one as
it does not implement a main() method.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}.[PostboxPeer](/Components/pydoc/Kamaelia.Internet.UDP.PostboxPeer.html){.reference}
============================================================================================================================================================================================================================================================================

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

-   **control** : Not listened to
-   **inbox** : Send (host,port,data) tuples here to send a UDP packet
    to (host,port) containing data
:::

::: {.section}
### [Outboxes]{#symbol-PostboxPeer.Outboxes}

-   **outbox** : Data received on the socket is passed out here, form:
    ((host, port), data)
-   **signal** : No data sent to
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
:::

::: {.section}
#### [main(self)]{#symbol-PostboxPeer.main}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP.BasicPeer :

-   [receive\_packet](/Components/pydoc/Kamaelia.Internet.UDP.html#symbol-BasicPeer.receive_packet){.reference}(self,
    sock)
:::
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}.[SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP.SimplePeer.html){.reference}
==========================================================================================================================================================================================================================================================================

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

-   **control** : NOT USED
-   **inbox** : Raw binary string data packets to be sent to the
    destination (receiver host,port)
:::

::: {.section}
### [Outboxes]{#symbol-SimplePeer.Outboxes}

-   **outbox** : (data,(host,port)) tuples for each packet received
-   **signal** : NOT USED
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
:::

::: {.section}
#### [main(self)]{#symbol-SimplePeer.main}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP.BasicPeer :

-   [receive\_packet](/Components/pydoc/Kamaelia.Internet.UDP.html#symbol-BasicPeer.receive_packet){.reference}(self,
    sock)
:::
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}.[TargettedPeer](/Components/pydoc/Kamaelia.Internet.UDP.TargettedPeer.html){.reference}
================================================================================================================================================================================================================================================================================

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

-   **control** : Not listened to
-   **inbox** : Data recieved here is sent to the reciever addr/port
-   **target** : Data receieved here changes the receiver addr/port data
    is tuple form: (host, port)
:::

::: {.section}
### [Outboxes]{#symbol-TargettedPeer.Outboxes}

-   **outbox** : Data received on the socket is passed out here, form:
    (data,(host, port))
-   **signal** : No data sent to
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
:::

::: {.section}
#### [main(self)]{#symbol-TargettedPeer.main}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from Kamaelia.Internet.UDP.BasicPeer :

-   [receive\_packet](/Components/pydoc/Kamaelia.Internet.UDP.html#symbol-BasicPeer.receive_packet){.reference}(self,
    sock)
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
