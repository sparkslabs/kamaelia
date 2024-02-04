---
pagename: Components/pydoc.old/Kamaelia.Codec.RawYUVFramer.RawYUVFramer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Codec.RawYUVFramer.RawYUVFramer
========================================

class RawYUVFramer(Axon.Component.component)
--------------------------------------------

RawYUVFramer(size,pixformat) -\> raw yuv video data framing component

Creates a component that frames a raw stream of YUV video data into
frames.

Keyword arguments: size = (width,height) \-- size of a video frame in
pixels pixformat = \"YUV420\_Planar\" \-- raw video data format

#### Inboxes

-   control : Secondary inbox often used for signals. The closest
    analogy is unix signals
-   inbox : Default inbox for bulk data. Used in a pipeline much like
    stdin

#### Outboxes

-   outbox : Default data out outbox, used in a pipeline much like
    stdout
-   signal : The default signal based outbox - kinda like stderr, but
    more for sending singal type signals

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, size, pixformat)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### flushFrame(self)

Send out a frame, flushing buffers

### main(self)

Main loop

### packAndSend(self, raw)

packAndSend(raw) -\> None

Pack incoming raw data into y,u,v planes, and triggers a flush when all
planes are full.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
