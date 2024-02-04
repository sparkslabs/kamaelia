---
pagename: Components/pydoc.old/Kamaelia.Protocol.Framing.DataDeChunker
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Protocol.Framing.DataDeChunker
=======================================

class DataDeChunker(Axon.Component.component)
---------------------------------------------

DataDeChunker(\[syncmessage\]) -\> new DataDeChunker component.

Synchronises to a stream of string data, delimited into chunks by a
\'sync\' sequence. Chunks are buffered until the next \'sync sequence is
received and are then passed on.

Keyword arguments: - syncmessage - string to use as \'sync\' sequence
(default=\"XXXXXXXXXXXXXXXXXXXXXXXX\")

#### Inboxes

-   control : shutdown messages (producerFinished)
-   inbox : partial message chunk strings
-   flush : instructions to flush the internal buffer

#### Outboxes

-   outbox : dechunked message strings
-   signal : producerFinished shutdown messages

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, syncmessage)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### decodeChunk(self, chunk)

unEscape and return the chunk, sans the \'sync\' sequence prefix, or
raise IncompleteChunk if the chunk isn\'t prefixed with the \'sync\'
sequence (can\'t guarantee the chunk is whole).

### main(self)

Main loop.

### shouldFlush(self)

Returns non-zero if a message has been received on the \"flush\" inbox

### shutdown(self)

Shutdown on producerFinished message arriving at \"control\" inbox.

### unEscapeSyncMessage(self, message)

Returns message with escaped occurrences of the \'sync\' message
unescaped again.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
