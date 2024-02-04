---
pagename: Components/pydoc/Kamaelia.Protocol.EchoProtocol
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol.html){.reference}
==========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol.EchoProtocol.html){.reference}**
:::

-   [Simple Echo Protocol](#659){.reference}
    -   [Example Usage](#660){.reference}
    -   [How does it work?](#661){.reference}
:::

::: {.section}
Simple Echo Protocol {#659}
====================

A simple protocol component that echoes back anything sent to it.

It simply copies its input to its output.

::: {.section}
[Example Usage]{#example-usage} {#660}
-------------------------------

A simple server that accepts connections on port 1501, echoing back
anything sent to it:

``` {.literal-block}
>>> SimpleServer(protocol=EchoProtocol, port=1501).run()
```

On a unix/linux client:

``` {.literal-block}
> telnet <server ip> 1501
Trying <server ip>...
Connected to <server ip>...
hello world, this will be echoed back when I press return (newline)
hello world, this will be echoed back when I press return (newline)
oooh, thats nice!
oooh, thats nice!
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#661}
--------------------------------------

The component receives data on its \"inbox\" inbox and immediately
copies it to its \"outbox\" outbox.

If a producerFinished or shutdownMicroprocess message is received on its
\"control\" inbox, the component sends a producerFinished message to its
\"signal\" outbox and terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol.html){.reference}.[EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol.EchoProtocol.html){.reference}
=========================================================================================================================================================================================================================================================================================================

::: {.section}
class EchoProtocol([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-EchoProtocol}
----------------------------------------------------------------------------------------------------

EchoProtocol() -\> new EchoProtocol component

Simple component that copies anything sent to its \"inbox\" inbox to its
\"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-EchoProtocol.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-EchoProtocol.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-EchoProtocol.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [mainBody(self)]{#symbol-EchoProtocol.mainBody}

Main body.
:::

::: {.section}
#### [shutdown(self)]{#symbol-EchoProtocol.shutdown}

Return 0 if a shutdown message is received, else return 1.
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
