---
pagename: Components/pydoc/Kamaelia.Protocol.Packetise
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Packetise](/Components/pydoc/Kamaelia.Protocol.Packetise.html){.reference}
====================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [MaxSizePacketiser](/Components/pydoc/Kamaelia.Protocol.Packetise.MaxSizePacketiser.html){.reference}**
:::
:::

::: {.section}
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Packetise](/Components/pydoc/Kamaelia.Protocol.Packetise.html){.reference}.[MaxSizePacketiser](/Components/pydoc/Kamaelia.Protocol.Packetise.MaxSizePacketiser.html){.reference}
==========================================================================================================================================================================================================================================================================================================

::: {.section}
class MaxSizePacketiser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-MaxSizePacketiser}
---------------------------------------------------------------------------------------------------------

This is a simple class whose purpose is to take a data stream and
convert it into packets of a maximum size.

The default packet size is 1000 bytes.

This component was created due to limitations of multicast meaning
packets get discarded more easily over a certain size.

Example usage:

``` {.literal-block}
Pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000,
                    chunkrate=50),
    SRM_Sender(),
    blockise(), # Ensure chunks small enough for multicasting!
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).activate()
```

This component acts as a simple filter - data is expected on inboxes and
packets come out the outbox.

This component does not terminate.

::: {.section}
### [Inboxes]{#symbol-MaxSizePacketiser.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-MaxSizePacketiser.Outboxes}
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
#### [\_\_init\_\_(self\[, maxsize\])]{#symbol-MaxSizePacketiser.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-MaxSizePacketiser.main}
:::
:::

::: {.section}
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
