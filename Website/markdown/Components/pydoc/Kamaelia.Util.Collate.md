---
pagename: Components/pydoc/Kamaelia.Util.Collate
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Collate](/Components/pydoc/Kamaelia.Util.Collate.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Collate](/Components/pydoc/Kamaelia.Util.Collate.Collate.html){.reference}**
:::

-   [Collate everything received into a single
    message](#162){.reference}
    -   [Example Usage](#163){.reference}
    -   [Behaviour](#164){.reference}
:::

::: {.section}
Collate everything received into a single message {#162}
=================================================

Buffers all data sent to it. When shut down, sends all data it has
received as collated as a list in a single message.

::: {.section}
[Example Usage]{#example-usage} {#163}
-------------------------------

Read a file, in small chunks, then collate them into a single chunk:

``` {.literal-block}
Pipeline( RateControlledFileReader("big_file", ... ),
          Collate(),
          ...
        )
```
:::

::: {.section}
[Behaviour]{#behaviour} {#164}
-----------------------

Send data items to its \"inbox\" inbox to be collated.

Send a producerFinished or shutdownMicroprocess message to the
\"control\" inbox to terminate this component.

All collated data items will be sent out of the \"outbox\" outbox as a
list in a single message. The items are collated in the same order they
first arrived.

The component will then send on the shutdown message to its \"signal\"
outbox and immediately terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Collate](/Components/pydoc/Kamaelia.Util.Collate.html){.reference}.[Collate](/Components/pydoc/Kamaelia.Util.Collate.Collate.html){.reference}
================================================================================================================================================================================================================================================================

::: {.section}
class Collate([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Collate}
-----------------------------------------------------------------------------------------------

Collate() -\> new Collate component.

Buffers all data sent to it. When shut down, sends all data it has
received as a single message.

::: {.section}
### [Inboxes]{#symbol-Collate.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
:::

::: {.section}
### [Outboxes]{#symbol-Collate.Outboxes}

-   **outbox** : All data items collated into one message
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
#### [main(self)]{#symbol-Collate.main}

Main loop
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
