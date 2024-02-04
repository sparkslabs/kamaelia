---
pagename: Components/pydoc.old/Kamaelia.Internet.Multicast_sender.Multicast_sender
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.Multicast\_sender.Multicast\_sender
=====================================================

class Multicast\_sender(Axon.Component.component)
-------------------------------------------------

Multicast\_sender(local\_addr, local\_port, remote\_addr, remote\_port)
-\> component that sends to a multicast group.

Creates a component that sends data received on its \"inbox\" inbox to
the specified multicast group.

Keyword arguments: - local\_addr \-- local address (interface) to send
from (string) - local\_port \-- local port number - remote\_addr \--
address of multicast group to send to (string) - remote\_port \-- port
number

#### Inboxes

-   control : NOT USED
-   inbox : Data to be sent to the multicast group

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, local\_addr, local\_port, remote\_addr, remote\_port)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
