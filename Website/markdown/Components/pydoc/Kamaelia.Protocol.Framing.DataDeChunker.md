---
pagename: Components/pydoc/Kamaelia.Protocol.Framing.DataDeChunker
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[DataDeChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataDeChunker.html){.reference}
============================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DataDeChunker([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DataDeChunker}
-----------------------------------------------------------------------------------------------------

DataDeChunker(\[syncmessage\]) -\> new DataDeChunker component.

Synchronises to a stream of string data, delimited into chunks by a
\'sync\' sequence. Chunks are buffered until the next \'sync sequence is
received and are then passed on.

Keyword arguments:

-   syncmessage \-- string to use as \'sync\' sequence
    (default=\"XXXXXXXXXXXXXXXXXXXXXXXX\")

::: {.section}
### [Inboxes]{#symbol-DataDeChunker.Inboxes}

-   **control** : shutdown messages (producerFinished)
-   **inbox** : partial message chunk strings
-   **flush** : instructions to flush the internal buffer
:::

::: {.section}
### [Outboxes]{#symbol-DataDeChunker.Outboxes}

-   **outbox** : dechunked message strings
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
#### [\_\_init\_\_(self\[, syncmessage\])]{#symbol-DataDeChunker.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [decodeChunk(self, chunk)]{#symbol-DataDeChunker.decodeChunk}

unEscape and return the chunk, sans the \'sync\' sequence prefix, or
raise IncompleteChunk if the chunk isn\'t prefixed with the \'sync\'
sequence (can\'t guarantee the chunk is whole).
:::

::: {.section}
#### [main(self)]{#symbol-DataDeChunker.main}

Main loop.
:::

::: {.section}
#### [shouldFlush(self)]{#symbol-DataDeChunker.shouldFlush}

Returns non-zero if a message has been received on the \"flush\" inbox
:::

::: {.section}
#### [shutdown(self)]{#symbol-DataDeChunker.shutdown}

Shutdown on producerFinished message arriving at \"control\" inbox.
:::

::: {.section}
#### [unEscapeSyncMessage(self, message)]{#symbol-DataDeChunker.unEscapeSyncMessage}

Returns message with escaped occurrences of the \'sync\' message
unescaped again.
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
