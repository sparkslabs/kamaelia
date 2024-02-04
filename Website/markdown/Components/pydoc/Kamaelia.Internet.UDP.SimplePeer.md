---
pagename: Components/pydoc/Kamaelia.Internet.UDP.SimplePeer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}.[SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP.SimplePeer.html){.reference}
==========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}

------------------------------------------------------------------------

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
