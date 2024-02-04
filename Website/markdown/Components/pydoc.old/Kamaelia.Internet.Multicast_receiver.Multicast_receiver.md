---
pagename: Components/pydoc.old/Kamaelia.Internet.Multicast_receiver.Multicast_receiver
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.Multicast\_receiver.Multicast\_receiver
=========================================================

class Multicast\_receiver(Axon.Component.component)
---------------------------------------------------

Multicast\_receiver(address, port) -\> component that receives multicast
traffic.

Creates a component that receives multicast packets in the given
multicast group and sends it out of its \"outbox\" outbox.

Keyword arguments: - address \-- address of multicast group (string) -
port \-- port number

#### Inboxes

-   control : NOT USED
-   inbox : NOT USED

#### Outboxes

-   outbox : Emits (src\_addr, data\_received)
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, address, port)

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
