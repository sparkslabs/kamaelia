---
pagename: Components/pydoc/Kamaelia.Protocol.Framing.DataChunker
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[DataChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataChunker.html){.reference}
========================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DataChunker([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DataChunker}
---------------------------------------------------------------------------------------------------

DataChunker(\[syncmessage\]) -\> new DataChunker component.

Delineates messages by prefixing them with a \'sync\' sequence, allowing
a receiver to synchronise to the chunks in the stream. Any occurrences
of the sequence within the message itself are escaped to prevent
misinterpretation.

Keyword arguments:

-   syncmessage \-- string to use as \'sync\' sequence
    (default=\"XXXXXXXXXXXXXXXXXXXXXXXX\")

::: {.section}
### [Inboxes]{#symbol-DataChunker.Inboxes}

-   **control** : shutdown messages (producerFinished)
-   **inbox** : message strings to be chunked
:::

::: {.section}
### [Outboxes]{#symbol-DataChunker.Outboxes}

-   **outbox** : chunked message strings
-   **signal** : producerFinished shutdown messages
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
#### [\_\_init\_\_(self\[, syncmessage\])]{#symbol-DataChunker.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [encodeChunk(self, message)]{#symbol-DataChunker.encodeChunk}

Returns the message with the \'sync\' message prefix and escaping done.
:::

::: {.section}
#### [escapeSyncMessage(self, message)]{#symbol-DataChunker.escapeSyncMessage}

Returns the message, with occurrences of \'sync\' message escaped.
:::

::: {.section}
#### [main(self)]{#symbol-DataChunker.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-DataChunker.shutdown}

Shutdown on producerFinished message arriving at \"control\" inbox.
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
