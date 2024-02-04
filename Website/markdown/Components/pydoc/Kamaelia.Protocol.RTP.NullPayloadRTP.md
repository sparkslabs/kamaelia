---
pagename: Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[NullPayloadRTP](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP.html){.reference}
==================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [NullPayloadPreFramer](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP.NullPayloadPreFramer.html){.reference}**
:::
:::

::: {.section}
Null Payload RTP Classes. Null Payload Pre-Framer. Null Payload RTP
Packet Stuffer - Same thing.

This Null payload also assumes constant bit rate load.

Subcomponents functionality:

-   

    FileControl: - Only if RFA internal - isn\'t

    :   -   FileReader - only if internal - isn\'t
        -   FileSelector - only if internal - isn\'t

-   Format Decoding

-   DataFramaing

-   Command Interpreter (Likely to be component core code)
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[NullPayloadRTP](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP.html){.reference}.[NullPayloadPreFramer](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP.NullPayloadPreFramer.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class NullPayloadPreFramer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NullPayloadPreFramer}
------------------------------------------------------------------------------------------------------------

Inboxes:
:   control -\> File select, file read control, framing control recvsrc
    -\> Block/Chunks of raw disk data

Outboxes:
:   activatesrc -\> Control messages to the file reading subsystem
    output -\> The framed data, payload ready

::: {.section}
### [Inboxes]{#symbol-NullPayloadPreFramer.Inboxes}

-   **(\'control\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
-   **(\'recvsrc\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
:::

::: {.section}
### [Outboxes]{#symbol-NullPayloadPreFramer.Outboxes}

-   **(\'output\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
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
#### [\_\_init\_\_(self, sourcename\[, sourcebitrate\]\[, chunksize\])]{#symbol-NullPayloadPreFramer.__init__}

-   Name of source - at \_\_init\_\_
-   Data Rate - at \_\_init\_\_
-   Chunksize - at \_\_init\_\_
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-NullPayloadPreFramer.closeDownComponent}

No closedown/shutdown code
:::

::: {.section}
#### [handleControl(self)]{#symbol-NullPayloadPreFramer.handleControl}

returns quit flag - True means quit
:::

::: {.section}
#### [handleShutdown(self)]{#symbol-NullPayloadPreFramer.handleShutdown}
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-NullPayloadPreFramer.initialiseComponent}

No initialisation
:::

::: {.section}
#### [mainBody(self)]{#symbol-NullPayloadPreFramer.mainBody}

Loopbody:
:::

::: {.section}
#### [makeChunk(self, datatosend)]{#symbol-NullPayloadPreFramer.makeChunk}

C.makeChunk(datatosend) -\> chunk : network ready data
:::

::: {.section}
#### [sendCurrentChunk(self\[, sendpartial\])]{#symbol-NullPayloadPreFramer.sendCurrentChunk}

-   grab first (current chunk size) bytes
-   frame chunk
-   send chunk
:::

::: {.section}
#### [updateTimestamp(self, datatosend)]{#symbol-NullPayloadPreFramer.updateTimestamp}

C.updateTimestamp(datatosend)

self.timestamp stores the timestamp of the end of the most recently
transmitted data, whenever we send some data this timestamp needs to be
updated. This method represents the calculation involved. (calculate the
time period the data covers, and increment the timestamp)
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
