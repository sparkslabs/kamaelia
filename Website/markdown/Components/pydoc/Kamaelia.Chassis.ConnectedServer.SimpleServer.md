---
pagename: Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}.[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html){.reference}
==============================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SimpleServer(ServerCore) {#symbol-SimpleServer}
------------------------------

SimpleServer(protocol\[,port\]) -\> new Simple protocol server component

A simple single port, multiple connection server, that instantiates a
protocol handler component to handle each connection.

Keyword arguments:

-   protocol \-- function that returns a protocol handler component
-   port \-- Port number to listen on for connections (default=1601)

::: {.section}
### [Inboxes]{#symbol-SimpleServer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleServer.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-SimpleServer.__init__}
:::

::: {.section}
#### [mkProtocolHandler(self, \*\*sock\_info)]{#symbol-SimpleServer.mkProtocolHandler}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.Chassis.ConnectedServer.MoreComplexServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.MoreComplexServer.html){.reference} :

-   [handleNewConnection](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.handleNewConnection){.reference}(self,
    newCSAMessage)
-   [stop](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.stop){.reference}(self)
-   [initialiseServerSocket](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.initialiseServerSocket){.reference}(self)
-   [handleClosedCSA](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.handleClosedCSA){.reference}(self,
    shutdownCSAMessage)
-   [main](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.main){.reference}(self)
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
