---
pagename: Components/pydoc.old/Kamaelia.Protocol.Framing.Framer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Protocol.Framing.Framer
================================

class Framer(Axon.Component.component)
--------------------------------------

Framer() -\> new Framer component.

Frames (tag, data) pairs into strings containing the same data.

#### Inboxes

-   control : shutdown messages (producerFinished)
-   inbox : (tag, data) pairs to be framed

#### Outboxes

-   outbox : framed data strings
-   signal : producerFinished shutdown messages

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

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
