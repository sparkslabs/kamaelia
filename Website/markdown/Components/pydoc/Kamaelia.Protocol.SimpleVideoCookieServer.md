---
pagename: Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleVideoCookieServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer.html){.reference}
================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [HelloServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer.HelloServer.html){.reference}**
:::
:::

::: {.section}
Simple Video based fortune cookie server

To watch the video, on a linux box do this:

netcat \<server ip\> 1500 \| plaympeg -2 -
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleVideoCookieServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer.html){.reference}.[HelloServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer.HelloServer.html){.reference}
========================================================================================================================================================================================================================================================================================================================================

::: {.section}
class HelloServer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-HelloServer}
---------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-HelloServer.Inboxes}

-   **(\'datain\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
-   **(\'inbox\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
-   **(\'control\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
:::

::: {.section}
### [Outboxes]{#symbol-HelloServer.Outboxes}

-   **(\'outbox\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
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
#### [\_\_init\_\_(self\[, filename\]\[, debug\])]{#symbol-HelloServer.__init__}
:::

::: {.section}
#### [handleDataIn(self)]{#symbol-HelloServer.handleDataIn}
:::

::: {.section}
#### [handleInbox(self)]{#symbol-HelloServer.handleInbox}
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-HelloServer.initialiseComponent}
:::

::: {.section}
#### [mainBody(self)]{#symbol-HelloServer.mainBody}
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
