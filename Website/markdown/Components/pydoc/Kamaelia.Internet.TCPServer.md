---
pagename: Components/pydoc/Kamaelia.Internet.TCPServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.html){.reference}
====================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.TCPServer.html){.reference}**
:::

-   [TCP Socket Server](#112){.reference}
    -   [Example Usage](#113){.reference}
    -   [How does it work?](#114){.reference}
:::

::: {.section}
TCP Socket Server {#112}
=================

A building block for creating a TCP based network server. It accepts
incoming connection requests and sets up a component to handle the
socket which it then passes on.

This component does not handle the instantiation of components to handle
an accepted connection request. Another component is needed that
responds to this component and actually does something with the newly
established connection. If you require a more complete implementation
that does this, see
[Kamaelia.Internet.SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}
or
[Kamaelia.Chassis.ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}.

::: {.section}
[Example Usage]{#example-usage} {#113}
-------------------------------

See
[Kamaelia.Internet.SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}
or
[Kamaelia.Chassis.ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}
for examples of how this component can be used.

The process of using a TCPServer component can be summarised as: -
Create a TCP Server - Wait for newCSA messages from the TCP Server\'s
\"protocolHandlerSignal\" outbox - Send what you like to CSA\'s, ensure
you recieve data from the CSAs - Send producerFinished to the CSA to
shut it down.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#114}
--------------------------------------

This component creates a listener socket, bound to the specified port,
and registers itself and the socket with a selectorComponent so it is
notified of incoming connections. The selectorComponent is obtained by
calling selectorComponent.getSelectorService(\...) to look it up with
the local Coordinating Assistant Tracker (CAT).

When the it recieves a new connection it performs an accept, and creates
a ConnectedSocketAdapter (CSA) to handle the activity on that
connection.

The CSA is passed in a newCSA(self,CSA) message to TCPServer\'s
\"protocolHandlerSignal\" outbox.

The CSA is also registered with the selector service by sending it a
newCSA(self,(CSA,sock)) message, to ensure the CSA is notified of
incoming data on its socket.

The client component(s) using the TCPServer should handle the newly
created CSA passed to it in whatever way it sees fit.

If a socketShutdown message is received on the \"\_feedbackFromCSA\"
inbox, then a shutdownCSA(self, CSA) message is sent to TCPServer\'s
\"protocolHandlerSignal\" outbox to notify the client component that the
connection has closed.

Also, a shutdownCSA(self, (CSA, sock)) message is sent to the selector
service to deregister the CSA from receiving notifications.

This component does not terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.html){.reference}.[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.TCPServer.html){.reference}
==========================================================================================================================================================================================================================================================================================

::: {.section}
class TCPServer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TCPServer}
-------------------------------------------------------------------------------------------------

TCPServer(listenport) -\> TCPServer component listening on the specified
port.

Creates a TCPServer component that accepts all connection requests on
the specified port.

::: {.section}
### [Inboxes]{#symbol-TCPServer.Inboxes}

-   **control** : we expect to recieve serverShutdown messages here
-   **newconnection** : We expected to recieve a message here when a new
    connection is ready
-   **\_feedbackFromCSA** : for feedback from ConnectedSocketAdapter
    (shutdown messages)
:::

::: {.section}
### [Outboxes]{#symbol-TCPServer.Outboxes}

-   **protocolHandlerSignal** : For passing on newly created
    ConnectedSocketAdapter components
-   **signal** : NOT USED
-   **\_selectorShutdownSignal** : To deregister our interest with the
    selector
-   **\_selectorSignal** : For registering newly created
    ConnectedSocketAdapter components with a selector service
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self, listenport, socketOptions, \*\*argd)]{#symbol-TCPServer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [anyClosedSockets(self)]{#symbol-TCPServer.anyClosedSockets}

Check \"\_feedbackFromCSA\" inbox for socketShutdown messages, and close
sockets in response.
:::

::: {.section}
#### [closeSocket(self, shutdownMessage)]{#symbol-TCPServer.closeSocket}

Respond to a socketShutdown message by closing the socket.

Sends a removeReader and removeWriter message to the selectorComponent.
Sends a shutdownCSA(self, theCSA) message to \"protocolHandlerSignal\"
outbox.
:::

::: {.section}
#### [createConnectedSocket(self, sock)]{#symbol-TCPServer.createConnectedSocket}

Accepts the connection request on the specified socket and returns a
ConnectedSocketAdapter component for it.
:::

::: {.section}
#### [handleNewConnection(self)]{#symbol-TCPServer.handleNewConnection}

Handle notifications from the selector service of new connection
requests.

Accepts and sets up new connections, wiring them up and passing them on
via the \"protocolHandlerSignal\" outbox.
:::

::: {.section}
#### [main(self)]{#symbol-TCPServer.main}
:::

::: {.section}
#### [makeTCPServerPort(self\[, suppliedport\]\[, HOST\]\[, minrange\]\[, maxrange\]\[, maxlisten\])]{#symbol-TCPServer.makeTCPServerPort}

Returns (socket,port) - a bound TCP listener socket and the port number
it is listening on.

If suppliedPort is not specified, then a random port is chosen between
minrange and maxrange inclusive.

maxlisten is the max number of pending requests the server will allow
(queue up).
:::

::: {.section}
#### [stop(self)]{#symbol-TCPServer.stop}
:::
:::

::: {.section}
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
