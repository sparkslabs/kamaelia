---
pagename: Components/pydoc.old/Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter
===============================================================

class ConnectedSocketAdapter(Axon.Component.component)
------------------------------------------------------

ConnectedSocketAdapter(socket) -\> new CSA component wrapping specified
socket

Component for communicating with a socket. Send to its \"DataSend\"
inbox to send data, and receive data from its \"outbox\" outbox.

\"DataReady\" inbox must be wired to something that will notify it when
new data has arrived at the socket.

#### Inboxes

-   control : Shutdown on producerFinished message (incoming & outgoing
    data is flushed first)
-   DataSend : Data for this CSA to send through the socket
    (Axon.Ipc.status message)
-   Initialise : NOT USED
-   DataReady : Notify this CSA that there is incoming data ready on the
    socket

#### Outboxes

-   FactoryFeedback : Signals socketShutdown (this socket has closed)
-   outbox : Data received from the socket
-   signal : Signals shutdownCSA (this CSA is shutting down)

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, listensocket)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### handleControl(self)

Check for producerFinished message and shutdown in response

### handleDataReady(self)

Handle situation when has been notified that there is data waiting to be
read from the socket.

### handleDataSend(self)

Check for and send data to the socket

### mainBody(self)

Main loop.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
