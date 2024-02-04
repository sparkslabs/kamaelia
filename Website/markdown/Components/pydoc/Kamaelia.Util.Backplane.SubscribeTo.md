---
pagename: Components/pydoc/Kamaelia.Util.Backplane.SubscribeTo
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}.[SubscribeTo](/Components/pydoc/Kamaelia.Util.Backplane.SubscribeTo.html){.reference}
==============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SubscribeTo([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SubscribeTo}
---------------------------------------------------------------------------------------------------

SubscribeTo(source) -\> new SubscribeTo component

Subscribes to a named Backplane. Receives any data published to that
backplane and sends it on out of its \"outbox\" outbox.

Keyword arguments:

-   source \-- the name of the Backplane to subscribe to for data

::: {.section}
### [Inboxes]{#symbol-SubscribeTo.Inboxes}

-   **control** : Shutdown signalling (doesn\'t shutdown the Backplane)
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-SubscribeTo.Outboxes}

-   **outbox** : Data received from the backplane (that was published to
    it)
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
#### [\_\_init\_\_(self, source)]{#symbol-SubscribeTo.__init__}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-SubscribeTo.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-SubscribeTo.main}

Main loop.
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
