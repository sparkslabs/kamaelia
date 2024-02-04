---
pagename: Components/pydoc/Kamaelia.Internet.UDP_ng.UDPSender
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}.[UDPSender](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPSender.html){.reference}
==================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}

------------------------------------------------------------------------

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
