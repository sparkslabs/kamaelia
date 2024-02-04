---
pagename: Components/pydoc/Kamaelia.Internet.SingleServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}
==========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.SingleServer.html){.reference}**
-   **component
    [echo](/Components/pydoc/Kamaelia.Internet.SingleServer.echo.html){.reference}**
:::
:::

::: {.section}
This is a simpler server than the SimpleServer component. Specifically
it only allows a single connection to occur at a time. Any data received
on that connection is sent to the component\'s outbox, and any data
received on its inbox is sent to the connection. When a connection
closes, it sends a producerFinished signal.

TODO: If there is already a connection, then any new connections are
shutdown. It would be better if they weren\'t accepted in the first
place, but that requires changes to TCPServer.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}.[SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.SingleServer.html){.reference}
=========================================================================================================================================================================================================================================================================================================

::: {.section}
class SingleServer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SingleServer}
----------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-SingleServer.Inboxes}

-   **control** : Default inbox, not actually listened to
-   **inbox** : Data received on this inbox is sent to the first client
    who connects
-   **\_oobinfo** : We receive notification of connection on this inbox
:::

::: {.section}
### [Outboxes]{#symbol-SingleServer.Outboxes}

-   **outbox** : Any data received from the first connection accepted is
    sent to this outbox
-   **signal** : When the client disconnects a producerFinished message
    is sent here
-   **\_CSA\_signal** : Outbox for sending messages to the CSA.
    Currently unused.
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
#### [\_\_init\_\_(self\[, port\])]{#symbol-SingleServer.__init__}
:::

::: {.section}
#### [handleNewCSA(self, data)]{#symbol-SingleServer.handleNewCSA}
:::

::: {.section}
#### [main(self)]{#symbol-SingleServer.main}
:::

::: {.section}
#### [stop(self)]{#symbol-SingleServer.stop}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}.[echo](/Components/pydoc/Kamaelia.Internet.SingleServer.echo.html){.reference}
=========================================================================================================================================================================================================================================================================================

::: {.section}
class echo([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-echo}
--------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-echo.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-echo.Outboxes}
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
#### [main(self)]{#symbol-echo.main}
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
