---
pagename: Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPDeframer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.html){.reference}.[RTPDeframer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPDeframer.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.html){.reference}

------------------------------------------------------------------------

::: {.section}
class RTPDeframer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RTPDeframer}
---------------------------------------------------------------------------------------------------

RTPDeframer() -\> new RTPDeframer component.

Deconstructs an RTP packet, outputting (seqnum, dict) tuple where seqnum
is for recovering the order of packets, and dict contains the fields
from the RTP packet.

::: {.section}
### [Inboxes]{#symbol-RTPDeframer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RTPDeframer.Outboxes}
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
#### [main(self)]{#symbol-RTPDeframer.main}
:::

::: {.section}
#### [parsePacket(self, packet)]{#symbol-RTPDeframer.parsePacket}
:::

::: {.section}
#### [shutdown(self)]{#symbol-RTPDeframer.shutdown}
:::
:::

::: {.section}
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
