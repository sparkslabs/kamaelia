---
pagename: Components/pydoc.old/Kamaelia.Protocol.Framing.DataChunker
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Protocol.Framing.DataChunker
=====================================

class DataChunker(Axon.Component.component)
-------------------------------------------

DataChunker(\[syncmessage\]) -\> new DataChunker component.

Delineates messages by prefixing them with a \'sync\' sequence, allowing
a receiver to synchronise to the chunks in the stream. Any occurrences
of the sequence within the message itself are escaped to prevent
misinterpretation.

Keyword arguments: - syncmessage - string to use as \'sync\' sequence
(default=\"XXXXXXXXXXXXXXXXXXXXXXXX\")

#### Inboxes

-   control : shutdown messages (producerFinished)
-   inbox : message strings to be chunked

#### Outboxes

-   outbox : chunked message strings
-   signal : producerFinished shutdown messages

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, syncmessage)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### encodeChunk(self, message)

Returns the message with the \'sync\' message prefix and escaping done.

### escapeSyncMessage(self, message)

Returns the message, with occurrences of \'sync\' message escaped.

### main(self)

Main loop.

### shutdown(self)

Shutdown on producerFinished message arriving at \"control\" inbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
