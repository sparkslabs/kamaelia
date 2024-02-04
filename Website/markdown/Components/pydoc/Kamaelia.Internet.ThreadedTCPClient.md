---
pagename: Components/pydoc/Kamaelia.Internet.ThreadedTCPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.html){.reference}
====================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient.html){.reference}**
:::

-   [Simple Threaded TCP Client](#142){.reference}
    -   [Example Usage](#143){.reference}
    -   [How does it work?](#144){.reference}
:::

::: {.section}
Simple Threaded TCP Client {#142}
==========================

This component is for making a TCP connection to a server. Send to its
\"inbox\" inbox to send data to the server. Pick up data received from
the server on its \"outbox\" outbox.

This component runs in its own separate thread so it can block on the
socket connection. This was written because some platforms that don\'t
support non-blocking calls to read/write data from sockets (eg. Python
for Nokia Series-60).

::: {.section}
[Example Usage]{#example-usage} {#143}
-------------------------------

Sending the contents of a file to a server at address 1.2.3.4 on port
1000:

``` {.literal-block}
Pipeline( RateControlledFileReader("myfile", rate=100000),
          ThreadedTCPClient("1.2.3.4", 1000),
        ).activate()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#144}
--------------------------------------

The component opens a socket connection to the specified server on the
specified port. Data received over the connection appears at the
component\'s \"outbox\" outbox as strings. Data can be sent as strings
by sending it to the \"inbox\" inbox.

The component will shutdown in response to a producerFinished message
arriving on its \"control\" inbox. The socket will be closed, and a
socketShutdown message will be sent to the \"signal\" outbox.

All socket errors exceptions are passed on out of the \"signal\" outbox.
This will always result in the socket being closed (if open) and a
socketShutdown message also being sent to the \"signal\" outbox (after
the exception).

It does not use a ConnectedSocketAdapter, instead handling all socket
communications itself.

The compnent is based on
[Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.html){.reference}.[ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient.html){.reference}
==================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ThreadedTCPClient([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-ThreadedTCPClient}
-----------------------------------------------------------------------------------------------------------------------------------------

ThreadedTCPClient(host,port\[,chargen\]\[,initalsendmessage\]) -\>
threaded component with a TCP connection to a server.

Establishes a TCP connection to the specified server.

Keyword arguments:

-   host \-- address of the server to connect to (string)
-   port \-- port number to connect on
-   initialsendmessage \-- to be send immediately after connection is
    established (default=None)

::: {.section}
### [Inboxes]{#symbol-ThreadedTCPClient.Inboxes}

-   **control** :
-   **inbox** : data to send to the socket
:::

::: {.section}
### [Outboxes]{#symbol-ThreadedTCPClient.Outboxes}

-   **outbox** : data received from the socket
-   **signal** : diagnostic output, errors and shutdown messages
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
#### [\_\_init\_\_(self, host, port\[, chargen\]\[, initialsendmessage\])]{#symbol-ThreadedTCPClient.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-ThreadedTCPClient.main}

Main (thread) loop
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
