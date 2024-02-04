---
pagename: Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter.html){.reference}
==============================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter.html){.reference}**
:::

-   [Talking to network sockets](#138){.reference}
    -   [Example Usage](#139){.reference}
    -   [See also](#140){.reference}
    -   [How does it work?](#141){.reference}
:::

::: {.section}
Talking to network sockets {#138}
==========================

A Connected Socket Adapter (CSA) component talks to a network server
socket. Data is sent to and received from the socket via this
component\'s inboxes and outboxes. A CSA is effectively a wrapper for a
socket.

Most components should not need to create CSAs themselves. Instead, use
components such as TCPClient to make an outgoing connection, or
TCPServer or SimpleServer to be a server that responds to incoming
connections.

::: {.section}
[Example Usage]{#example-usage} {#139}
-------------------------------

See source code for TCPClient to see how Connected Socket Adapters can
be used.
:::

::: {.section}
[See also]{#see-also} {#140}
---------------------

-   TCPClient \-- for making a connection to a server
-   TCPServer \--
-   SimpleServer \-- a prefab chassis for building a server
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#141}
--------------------------------------

A CSA is usually created either by a component such as TCPClient that
wants to establish a connection to a server; or by a primary listener
socket - a component acting as a server - listening for incoming
connections from clients.

The socket should be set up and passed to the constructor to make the
CSA.

Incoming data, read by the CSA, is sent out of its \"outbox\" outbox as
strings containing the received binary data. Send data by sending it, as
strings, to the \"inbox\" outbox.

The CSA expects to be wired to a component that will notify it when new
data has arrived at its socket (by sending an
[Axon.Ipc.status](/Docs/Axon/Axon.Ipc.status.html){.reference} message
to its \"ReadReady\" inbox. This is to allow the CSA to sleep rather
than busy-wait or blocking when waiting for new data to arrive.
Typically this is the Selector component.

This component will terminate (and close its socket) if it receives a
producerFinished or shutdownMicroprocess message on its \"control\"
inbox.

When this component terminates, it sends a socketShutdown(socket)
message out of its \"CreatorFeedback\" outbox and a
shutdownCSA((selfCSA,self.socket)) message out of its \"signal\" outbox.

The message sent to \"CreatorFeedback\" is to notify the original
creator that the socket is now closed and that this component should be
unwired.

The message sent to the \"signal\" outbox serves to notify any other
component involved - such as the one feeding notifications to the
\"ReadReady\" inbox (eg. the Selector component).
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter.html){.reference}.[ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ConnectedSocketAdapter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ConnectedSocketAdapter}
--------------------------------------------------------------------------------------------------------------

ConnectedSocketAdapter(socket) -\> new CSA component wrapping specified
socket

Component for communicating with a socket. Send to its \"inbox\" inbox
to send data, and receive data from its \"outbox\" outbox.

\"ReadReady\" inbox must be wired to something that will notify it when
new data has arrived at the socket.

::: {.section}
### [Inboxes]{#symbol-ConnectedSocketAdapter.Inboxes}

-   **control** : Shutdown on producerFinished message (incoming &
    outgoing data is flushed first)
-   **ReadReady** : Notify this CSA that there is incoming data ready on
    the socket
-   **makessl** : Notify this CSA that the socket should be wrapped into
    SSL
-   **inbox** : Data for this CSA to send through the socket
    ([Axon.Ipc.status](/Docs/Axon/Axon.Ipc.status.html){.reference}
    message)
-   **SendReady** : Notify this CSA that the socket is ready to send
:::

::: {.section}
### [Outboxes]{#symbol-ConnectedSocketAdapter.Outboxes}

-   **outbox** : Data received from the socket
-   **CreatorFeedback** : Expected to be connected to some form of
    signal input on the CSA\'s creator. Signals socketShutdown (this
    socket has closed)
-   **sslready** : Notifies components that the socket is now wrapped
    into SSL
-   **signal** : Signals shutdownCSA (this CSA is shutting down)
-   **\_selectorSignal** : For communication to the selector
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
#### [\_\_init\_\_(self, listensocket, selectorService\[, crashOnBadDataToSend\]\[, noisyErrors\])]{#symbol-ConnectedSocketAdapter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_saferecv(self, sock\[, size\])]{#symbol-ConnectedSocketAdapter._saferecv}

Internal only function, used for recieving data, and handling EAGAIN
style retry scenarios gracefully
:::

::: {.section}
#### [\_safesend(self, sock, data)]{#symbol-ConnectedSocketAdapter._safesend}

Internal only function, used for sending data, and handling EAGAIN style
retry scenarios gracefully
:::

::: {.section}
#### [canDoSomething(self)]{#symbol-ConnectedSocketAdapter.canDoSomething}
:::

::: {.section}
#### [checkSocketStatus(self)]{#symbol-ConnectedSocketAdapter.checkSocketStatus}
:::

::: {.section}
#### [flushSendQueue(self)]{#symbol-ConnectedSocketAdapter.flushSendQueue}
:::

::: {.section}
#### [handleControl(self)]{#symbol-ConnectedSocketAdapter.handleControl}

Check for producerFinished message and shutdown in response
:::

::: {.section}
#### [handleReceive(self)]{#symbol-ConnectedSocketAdapter.handleReceive}
:::

::: {.section}
#### [main(self)]{#symbol-ConnectedSocketAdapter.main}
:::

::: {.section}
#### [passOnShutdown(self)]{#symbol-ConnectedSocketAdapter.passOnShutdown}
:::

::: {.section}
#### [stop(self)]{#symbol-ConnectedSocketAdapter.stop}
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
