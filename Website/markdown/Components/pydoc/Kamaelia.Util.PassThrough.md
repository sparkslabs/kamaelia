---
pagename: Components/pydoc/Kamaelia.Util.PassThrough
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough.html){.reference}
============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough.PassThrough.html){.reference}**
:::

-   [Passthrough of data](#207){.reference}
    -   [Example Usage](#208){.reference}
    -   [More Detail](#209){.reference}
:::

::: {.section}
Passthrough of data {#207}
===================

The PassThrough component simply passes through data from its \"inbox\"
inbox to its \"outbox\" outbox.

This can be used, for example, as a dummy \'protocol\' component -
slotting it into a system where ordinarily a component would go that
somehow changes or processes the data passing through it.

::: {.section}
[Example Usage]{#example-usage} {#208}
-------------------------------

Creating a simple tcp socket server on port 1850 that echoes back to
clients whatever they send to it:

``` {.literal-block}
def echoProtocol:
    return PassThrough()

SimpleServer( protocol=echoProtocol, port=1850 ).run()
```
:::

::: {.section}
[More Detail]{#more-detail} {#209}
---------------------------

Send any item to PassThrough component\'s \"inbox\" inbox and it will
immediately be sent on out of the \"outbox\" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox then this component will immediately terminate. It
will send the message on out of its \"signal\" outbox. Any pending data
waiting in the \"inbox\" inbox may be lost.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough.html){.reference}.[PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough.PassThrough.html){.reference}
====================================================================================================================================================================================================================================================================================

::: {.section}
class PassThrough([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PassThrough}
---------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-PassThrough.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Messages to be passed through
:::

::: {.section}
### [Outboxes]{#symbol-PassThrough.Outboxes}

-   **outbox** : Passed through messages
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self\[, shutdownOn\])]{#symbol-PassThrough.__init__}
:::

::: {.section}
#### [mainBody(self)]{#symbol-PassThrough.mainBody}
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
