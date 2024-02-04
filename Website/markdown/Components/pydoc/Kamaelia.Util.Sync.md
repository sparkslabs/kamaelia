---
pagename: Components/pydoc/Kamaelia.Util.Sync
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Sync](/Components/pydoc/Kamaelia.Util.Sync.html){.reference}
==============================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Sync](/Components/pydoc/Kamaelia.Util.Sync.Sync.html){.reference}**
:::

-   [Wait for \'n\' items before sending one of them
    on](#232){.reference}
    -   [Example Usage](#233){.reference}
    -   [Behaviour](#234){.reference}
:::

::: {.section}
Wait for \'n\' items before sending one of them on {#232}
==================================================

For every \'n\' items received, one is sent out (the first one received
in the latest batch).

::: {.section}
[Example Usage]{#example-usage} {#233}
-------------------------------

Wait for two tasks to finish, before propagating the shutdown message:

``` {.literal-block}
Graphline( A    = TaskA(),
           B    = TaskB(),
           SYNC = Sync(2),
           linkages = {
               ("A", "signal") : ("SYNC", "inbox"),
               ("B", "signal") : ("SYNC", "inbox"),

               ("SYNC", "outbox") : ("SYNC", "control"),
               ("SYNC", "signal") : ("", "signal"),
           }
```

The slightly strange wiring is to make sure the Sync component is also
shut down. The shutdown message is used to shutdown Sync itself. The
shutdown message it emits is then the one that propogates out of the
graphline.
:::

::: {.section}
[Behaviour]{#behaviour} {#234}
-----------------------

At initialisation, specify the number of items Sync should wait for.

Once that number of items have arrived at Sync\'s \"inbox\" inbox; the
first that arrived is sent on out of its \"outbox\" outbox. This process
is repeated until Sync is shut down.

If more han the specified number of items arrive in one go; the excess
items roll over to the next cycle. They are not ignored or lost.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Sync](/Components/pydoc/Kamaelia.Util.Sync.html){.reference}.[Sync](/Components/pydoc/Kamaelia.Util.Sync.Sync.html){.reference}
=================================================================================================================================================================================================================================================

::: {.section}
class Sync([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Sync}
--------------------------------------------------------------------------------------------

Sync(\[n\]) -\> new Sync component.

After ever \'n\' items received, the first in each batch received is
sent on.

Keyword arguments:

``` {.literal-block}
- n  -- The number of items to expect (default=2)
```

::: {.section}
### [Inboxes]{#symbol-Sync.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
:::

::: {.section}
### [Outboxes]{#symbol-Sync.Outboxes}

-   **outbox** : First data item from last batch
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
#### [\_\_init\_\_(self\[, n\])]{#symbol-Sync.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Sync.main}

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
