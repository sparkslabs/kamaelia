---
pagename: Components/pydoc/Kamaelia.Internet.TCPServer.TCPServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.html){.reference}.[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.TCPServer.html){.reference}
==========================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.TCPServer.html){.reference}

------------------------------------------------------------------------

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
