---
pagename: Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.html){.reference}.[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html){.reference}
==========================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.TCPClient.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TCPClient([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TCPClient}
-------------------------------------------------------------------------------------------------

TCPClient(host,port\[,delay\]) -\> component with a TCP connection to a
server.

Establishes a TCP connection to the specified server.

Keyword arguments:

-   host \-- address of the server to connect to (string)
-   port \-- port number to connect on
-   delay \-- delay (seconds) after activation before connecting
    (default=0)

::: {.section}
### [Inboxes]{#symbol-TCPClient.Inboxes}

-   **control** : Shutdown signalling
-   **makessl** : Notifications to the ConnectedSocketAdapter that we
    want to negotiate SSL
-   **inbox** : data to send to the socket
-   **\_socketFeedback** : notifications from the ConnectedSocketAdapter
:::

::: {.section}
### [Outboxes]{#symbol-TCPClient.Outboxes}

-   **outbox** : data received from the socket
-   **signal** : socket errors
-   **sslready** : SSL negotiated successfully
-   **\_selectorSignal** : For registering and deregistering
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
#### [\_\_init\_\_(self, host, port\[, delay\]\[, connect\_timeout\])]{#symbol-TCPClient.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-TCPClient.main}

Main loop.
:::

::: {.section}
#### [runClient(self\[, sock\])]{#symbol-TCPClient.runClient}
:::

::: {.section}
#### [safeConnect(self, sock, \*sockArgsList)]{#symbol-TCPClient.safeConnect}

Connect to socket and handle possible errors that may occur.

Returns True if successful, or False on failure. Unhandled errors are
raised as exceptions.
:::

::: {.section}
#### [setupCSA(self, sock)]{#symbol-TCPClient.setupCSA}

setupCSA(sock) -\> new ConnectedSocketAdapter component

Creates a ConnectedSocketAdapter component for the socket, and wires up
to it. Also sends the CSA to the \"selector\" service.
:::

::: {.section}
#### [shutdown(self)]{#symbol-TCPClient.shutdown}
:::

::: {.section}
#### [stop(self)]{#symbol-TCPClient.stop}

Stop method provided to allow the scheduler to kill TCPClient
connections cleanly if necessary. (Only rarely, if ever, needed - you
are not expected to call this yourself)
:::

::: {.section}
#### [waitCSAClose(self)]{#symbol-TCPClient.waitCSAClose}

Returns True if a socketShutdown message is received on
\"\_socketFeedback\" inbox.
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
