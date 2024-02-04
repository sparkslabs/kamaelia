---
pagename: Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.html){.reference}.[ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient.html){.reference}
==================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.html){.reference}

------------------------------------------------------------------------

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
