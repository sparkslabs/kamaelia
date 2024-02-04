---
pagename: Components/pydoc.old/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.chunks_to_lines
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Visualisation.PhysicsGraph.chunks\_to\_lines.chunks\_to\_lines
=======================================================================

class chunks\_to\_lines(Axon.Component.component)
-------------------------------------------------

chunks\_to\_lines() -\> new chunks\_to\_lines component.

Takes in chunked textual data and splits it at line breaks into
individual lines.

#### Inboxes

-   control : Shutdown signalling
-   inbox : Chunked textual data

#### Outboxes

-   outbox : Individual lines of text
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### main(self)

Main loop.

### shutdown(self)

Returns True if a shutdownMicroprocess or producerFinished message was
received.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
