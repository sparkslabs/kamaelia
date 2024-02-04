---
pagename: Components/pydoc.old/Kamaelia.Internet.TCPServer.TCPServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.TCPServer.TCPServer
=====================================

class TCPServer(Axon.Component.component)
-----------------------------------------

TCPServer(listenport) -\> TCPServer component listening on the specified
port.

Creates a TCPServer component that accepts all connection requests on
the specified port.

#### Inboxes

-   DataReady : status(\'data ready\') messages indicating new
    connection waiting to be accepted
-   \_csa\_feedback : for feedback from ConnectedSocketAdapter (shutdown
    messages)

#### Outboxes

-   protocolHandlerSignal : For passing on newly created
    ConnectedSocketAdapter components
-   signal : NOT USED
-   \_selectorSignal : For registering newly created
    ConnectedSocketAdapter components with a selector service

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, listenport)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### checkForClosedSockets(self)

Check \"\_csa\_feedback\" inbox for socketShutdown messages, and close
sockets in response.

### closeSocket(self, shutdownMessage)

Respond to a socketShutdown message by closing the socket.

Sends a shutdownCSA(self, (theCSA, sock)) message to the
selectorComponent. Sends a shutdownCSA(self, theCSA) message to
\"protocolHandlerSignal\" outbox.

### createConnectedSocket(self, sock)

Accepts the connection request on the specified socket and returns a
ConnectedSocketAdapter component for it.

### handleNewConnection(self)

Handle notifications from the selector service of new connection
requests.

Accepts and sets up new connections, wiring them up and passing them on
via the \"protocolHandlerSignal\" outbox.

### initialiseComponent(self)

Obtains a selector service and wires up to it, registering self to be
notified of incoming connection requests on a socket bound to the port
its supposed to be listening to.

### mainBody(self)

Main loop

### makeTCPServerPort(self, suppliedport, HOST, minrange, maxrange, maxlisten)

Returns (socket,port) - a bound TCP listener socket and the port number
it is listening on.

If suppliedPort is not specified, then a random port is chosen between
minrange and maxrange inclusive.

maxlisten is the max number of pending requests the server will allow
(queue up).

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
