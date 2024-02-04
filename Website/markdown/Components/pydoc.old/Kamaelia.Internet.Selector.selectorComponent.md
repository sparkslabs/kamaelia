---
pagename: Components/pydoc.old/Kamaelia.Internet.Selector.selectorComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.Selector.selectorComponent
============================================

class selectorComponent(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent)
---------------------------------------------------------------------------

selectorComponent() -\> new selectorComponent component

Use selectorComponent.getSelectorService(\...) in preference as it
returns an existing instance, or automatically creates a new one.

#### Inboxes

-   control : NOT USED
-   inbox : NOT USED
-   notify : newCSA(\...) and shutdownCSA(\...) notifications

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### checkForClosedSockets(self)

### handleExceptionalSocket(self, sock)

Currently there is no support for exceptional sockets

### handleNotify(self)

Handle requests to register/deregister (component,socket) pairs.

### handleReadableSocket(self, sock)

Notifys corresponding component that its socket is ready for reading new
data.

### handleWriteableSocket(self, sock)

Notifys corresponding component that its socket is ready for writing new
data.

### main(self)

Main loop

### wireInComponent(self, socketComponentPair)

Wires in the (component, socket) pair, so the component receives
notifications of events on socket.

Checks their interfaces with validComponentInput().

Does not check if the component,socket pair has already been wired in.

### wireOutComponent(self, socketComponentPair)

Unwires the specified (component, socket) pair, so it no longer receives
notifications of events on the socket.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
