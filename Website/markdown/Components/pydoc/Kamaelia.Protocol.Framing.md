---
pagename: Components/pydoc/Kamaelia.Protocol.Framing
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}
================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DataChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataChunker.html){.reference}**
-   **component
    [DataDeChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataDeChunker.html){.reference}**
-   **component
    [DeFramer](/Components/pydoc/Kamaelia.Protocol.Framing.DeFramer.html){.reference}**
-   **component
    [Framer](/Components/pydoc/Kamaelia.Protocol.Framing.Framer.html){.reference}**
:::

-   [Simple data Framing and chunking](#627){.reference}
    -   [Example Usage](#628){.reference}
    -   [How does it work?](#629){.reference}
        -   [Framer / DeFramer](#630){.reference}
        -   [DataChunker / DataDeChunker](#631){.reference}
:::

::: {.section}
Simple data Framing and chunking {#627}
================================

A simple set of components for framing data and chunking it, and for
reversing the process.

The Framer component frames messages as string, prefixed with a tag (eg.
sequence number) and their length. The Chunker component inserts markers
into the data stream to identify the start of chunks (eg. frames).

The DeChunker and DeFramer reverse the process.

::: {.section}
[Example Usage]{#example-usage} {#628}
-------------------------------

Framing messages for transport over a stream based connection (eg, TCP):

``` {.literal-block}
Pipeline(MessageSource(...),   # emits message
         DataChunker(),
         TCPClient("<server ip>", 1500),
        ).activate()
```

And on the server:

``` {.literal-block}
Pipeline(SingleServer(1500),
         DataDeChunker(),
         MessageReceiver(...)
        ).activate()
```

Packing data for transport over a link that may loose packets:

``` {.literal-block}
Pipeline(DataSource(...),     # emits (sequence_number, data) pairs
         Framer(),
         Chunker(),
         UnreliableTransportMechanismSender(),
        ).activate()
```

At the receiver:

``` {.literal-block}
Pipeline(UnreliableTransportMechanismReceiver(),
         DeChunker(),
         DeFramer(),
         DataHandler()        # receives (sequence_number, data) pairs
        ).activate()
```

Note that this example doesn\'t attempt to fix errors in the stream,
just detect them.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#629}
--------------------------------------

::: {.section}
### [Framer / DeFramer]{#framer-deframer} {#630}

Framer/DeFramer frame and deframe data pairs of the form (tag,data).
\'data\' should be the main payload, and \'tag\' is suitable for
something like a frame sequence number.

Both tag and data are treated as strings. \'data\' can contain any data.
\'tag\' should not contain newline or any whitespace character(s).

The framed data has the format \"\<tag\> \<length\> \<data\>\" where
\'length\' is the length of the \'data\' string.

The SimpleFrame class performs the actual framing and deframing of the
data.

These components terminate if they receive a producerFinished() message
on their \"control\" inbox. They pass the message onto their \"signal\"
outbox before terminating.
:::

::: {.section}
### [DataChunker / DataDeChunker]{#datachunker-datadechunker} {#631}

The DataChunker/DataDeChunker components chunk and dechunk the data by
inserting \'sync\' sequences of characters to delimit chunks of data.
Each message received by DataChunker on its \"inbox\" inbox is
considered a chunk.

DataChunker prefixes each chunk with the \'sync\' message sequence and
escapes any occurrences of that sequence within the data itself. The
result is output on its \"outbox\" outbox.

DataDeChunker does the reverse process. If data is received without a
preceeding \'sync\' sequence then there is no way to tell if that chunk
is complete (whole) and it will be discarded. Once the internal buffer
contains a full chunk of data with a \'sync\' sequence before and after
it, that chunk is output from its \"outbox\" outbox. The \'sync\'
sequences are removed and any escaped occurrences of the \'sync\'
message within the data are un-escaped again.

Note that DataDeChunker buffers chunks until it knows they have been
fully received. If a final chunk is not followed by a occurence of the
\'sync\' message then it will never be output.

However DataDeChunker can be told to flush the remaining contents of its
buffer by sending any message to its \"flush\" inbox.

These components terminate if they receive a producerFinished() message
on their \"control\" inbox. They pass the message onto their \"signal\"
outbox before terminating.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[DataChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataChunker.html){.reference}
========================================================================================================================================================================================================================================================================================

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

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[DataDeChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataDeChunker.html){.reference}
============================================================================================================================================================================================================================================================================================

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

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[DeFramer](/Components/pydoc/Kamaelia.Protocol.Framing.DeFramer.html){.reference}
==================================================================================================================================================================================================================================================================================

::: {.section}
class DeFramer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DeFramer}
------------------------------------------------------------------------------------------------

DeFramer -\> new DeFramer component.

Converts string that were framed using the Framer component back into
(tag, data) pairs.

::: {.section}
### [Inboxes]{#symbol-DeFramer.Inboxes}

-   **control** : shutdown messages (producerFinished)
-   **inbox** : framed data strings
:::

::: {.section}
### [Outboxes]{#symbol-DeFramer.Outboxes}

-   **outbox** : deframed (tag, data) pairs
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
#### [main(self)]{#symbol-DeFramer.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-DeFramer.shutdown}

Shutdown on producerFinished message arriving at \"control\" inbox.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[Framer](/Components/pydoc/Kamaelia.Protocol.Framing.Framer.html){.reference}
==============================================================================================================================================================================================================================================================================

::: {.section}
class Framer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Framer}
----------------------------------------------------------------------------------------------

Framer() -\> new Framer component.

Frames (tag, data) pairs into strings containing the same data.

::: {.section}
### [Inboxes]{#symbol-Framer.Inboxes}

-   **control** : shutdown messages (producerFinished)
-   **inbox** : (tag, data) pairs to be framed
:::

::: {.section}
### [Outboxes]{#symbol-Framer.Outboxes}

-   **outbox** : framed data strings
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
#### [main(self)]{#symbol-Framer.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-Framer.shutdown}

Shutdown on producerFinished message arriving at \"control\" inbox.
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
