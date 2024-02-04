---
pagename: Components/pydoc/Kamaelia.Chassis.ConnectedServer.ServerCore
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}.[ServerCore](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.ServerCore.html){.reference}
==========================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ServerCore([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-ServerCore}
------------------------------------------------------------------------------------------------------------------------------------------------------

ServerCore(protocol\[,port\]) -\> new Simple protocol server component

A simple single port, multiple connection server, that instantiates a
protocol handler component to handle each connection. The function that
creates the protocol must access arguments providing information about
the connection.

Keyword arguments:

-   protocol \-- function that returns a protocol handler component
-   port \-- Port number to listen on for connections (default=1601)

::: {.section}
### [Inboxes]{#symbol-ServerCore.Inboxes}

-   **control** : We expect to get serverShutdown messages here
-   **\_socketactivity** : Messages about new and closing connections
    here
:::

::: {.section}
### [Outboxes]{#symbol-ServerCore.Outboxes}

-   **\_serversignal** : we send shutdown messages to the TCP server
    here
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-ServerCore.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [handleClosedCSA(self, shutdownCSAMessage)]{#symbol-ServerCore.handleClosedCSA}

handleClosedCSA(shutdownCSAMessage) -\> None

Terminates and unwires the protocol handler for the closing socket.

Keyword arguments: shutdownCSAMessage \-- shutdownCSAMessage.object is
the ConnectedSocketAdapter for socket that is closing.
:::

::: {.section}
#### [handleNewConnection(self, newCSAMessage)]{#symbol-ServerCore.handleNewConnection}

handleNewConnection(newCSAMessage) -\>
[Axon.Ipc.newComponent](/Docs/Axon/Axon.Ipc.newComponent.html){.reference}(protocol
handler)

Creates and returns a protocol handler for new connection.

Keyword arguments:

-   newCSAMessage \-- newCSAMessage.object is the ConnectedSocketAdapter
    component for the connection
:::

::: {.section}
#### [initialiseServerSocket(self)]{#symbol-ServerCore.initialiseServerSocket}
:::

::: {.section}
#### [main(self)]{#symbol-ServerCore.main}
:::

::: {.section}
#### [mkProtocolHandler(self, \*\*sock\_info)]{#symbol-ServerCore.mkProtocolHandler}
:::

::: {.section}
#### [stop(self)]{#symbol-ServerCore.stop}
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
