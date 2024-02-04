---
pagename: Components/pydoc/Kamaelia.Util.Sync.Sync
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Sync](/Components/pydoc/Kamaelia.Util.Sync.html){.reference}.[Sync](/Components/pydoc/Kamaelia.Util.Sync.Sync.html){.reference}
=================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Sync.html){.reference}

------------------------------------------------------------------------

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
