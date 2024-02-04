---
pagename: Components/pydoc/Kamaelia.Internet.TCPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.html){.reference}
====================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html){.reference}**
:::

-   [Simple TCP Client](#104){.reference}
    -   [Example Usage](#105){.reference}
    -   [Example Usage - SSL](#106){.reference}
    -   [How does it work?](#107){.reference}
:::

::: {.section}
Simple TCP Client {#104}
=================

This component is for making a TCP connection to a server. Send to its
\"inbox\" inbox to send data to the server. Pick up data received from
the server on its \"outbox\" outbox.

::: {.section}
[Example Usage]{#example-usage} {#105}
-------------------------------

Sending the contents of a file to a server at address 1.2.3.4 on port
1000:

``` {.literal-block}
Pipeline( RateControlledFileReader("myfile", rate=100000),
          TCPClient("1.2.3.4", 1000),
        ).activate()
```
:::

::: {.section}
[Example Usage - SSL]{#example-usage-ssl} {#106}
-----------------------------------------

It is also possible to cause the TCPClient to switch into SSL mode. To
do this you send it a message on its \"makessl\" inbox. It is necessary
for a number of protocols to be able to switch between non-ssl and ssl,
hence this approach rather than simply saying \"ssl client\" or
\"non-ssl client\":

``` {.literal-block}
Graphline(
       MAKESSL = OneShot(" make ssl "),
       CONSOLE = ConsoleReader(),
       ECHO = ConsoleEchoer(),
       CONNECTION = TCPClient("kamaelia.svn.sourceforge.net", 443),
       linkages = {
           ("MAKESSL", "outbox"): ("CONNECTION", "makessl"),
           ("CONSOLE", "outbox"): ("CONNECTION", "inbox"),
           ("CONNECTION", "outbox"): ("ECHO", "inbox"),
       }
)
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#107}
--------------------------------------

TCPClient opens a socket connection to the specified server on the
specified port. Data received over the connection appears at the
component\'s \"outbox\" outbox as strings. Data can be sent as strings
by sending it to the \"inbox\" inbox.

An optional delay (between component activation and attempting to
connect) can be specified. The default is no delay.

It creates a ConnectedSocketAdapter (CSA) to handle the socket
connection and registers it with a selectorComponent so it is notified
of incoming data. The selectorComponent is obtained by calling
selectorComponent.getSelectorService(\...) to look it up with the local
Coordinating Assistant Tracker (CAT).

TCPClient wires itself to the \"CreatorFeedback\" outbox of the CSA. It
also wires its \"inbox\" inbox to pass data straight through to the
CSA\'s \"inbox\" inbox, and its \"outbox\" outbox to pass through data
from the CSA\'s \"outbox\" outbox.

Socket errors (after the connection has been successfully established)
may be sent to the \"signal\" outbox.

This component will terminate if the CSA sends a socketShutdown message
to its \"CreatorFeedback\" outbox.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to its \"control\" inbox. This message
is forwarded onto the CSA. TCPClient will then wait for the CSA to
terminate. It then sends its own shutdownMicroprocess message out of the
\"signal\" outbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.html){.reference}.[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html){.reference}
==========================================================================================================================================================================================================================================================================================

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
