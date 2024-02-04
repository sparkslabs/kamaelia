---
pagename: Components/pydoc.old/Kamaelia.Internet.UDP.PostboxPeer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.UDP.PostboxPeer
=================================

class PostboxPeer(Kamaelia.Internet.UDP.BasicPeer)
--------------------------------------------------

A postbox peer recieves messages formed of 3 parts:
:   (addr, port, data)

The postbox peer then takes care of delivery of these UDP messages to
the recipient.

#### Inboxes

-   control : Not listened to
-   inbox : Data recieved here is sent to the reciever addr/port

#### Outboxes

-   outbox : Data received on the socket is passed out here, form:
    ((addr, port), data)
-   signal : No data sent to

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, localaddr, localport)

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
