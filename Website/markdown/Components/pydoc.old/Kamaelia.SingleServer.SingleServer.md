---
pagename: Components/pydoc.old/Kamaelia.SingleServer.SingleServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.SingleServer.SingleServer
==================================

class SingleServer(Axon.Component.component)
--------------------------------------------

#### Inboxes

-   control : Default inbox, not actually listened to
-   inbox : Data received on this inbox is sent to the first client who
    connects
-   \_oobinfo : We receive notification of connection on this inbox

#### Outboxes

-   outbox : Any data received from the first connection accepted is
    sent to this outbox
-   signal : When the client disconnects a producerFinished message is
    sent here
-   \_CSA\_signal : Outbox for sending messages to the CSA. Currently
    unused.

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, port)

### handleNewCSA(self, data)

### main(self)

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
