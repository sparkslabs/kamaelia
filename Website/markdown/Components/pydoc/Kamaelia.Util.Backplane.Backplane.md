---
pagename: Components/pydoc/Kamaelia.Util.Backplane.Backplane
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.Backplane.html){.reference}
==========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Backplane([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Backplane}
-------------------------------------------------------------------------------------------------

Backplane(name) -\> new Backplane component.

A named backplane to which data can be published for subscribers to pick
up.

-   Use PublishTo components to publish data to a Backplane.
-   Use SubscribeTo components to receive data published to a Backplane.

Keyword arguments:

-   name \-- The name for the backplane. publishers and subscribers
    connect to this by using the same name.

::: {.section}
### [Inboxes]{#symbol-Backplane.Inboxes}

-   **control** : Shutdown signalling (shuts down the backplane and all
    subscribers
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-Backplane.Outboxes}

-   **outbox** : NOT USED
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
#### [\_\_init\_\_(self, name)]{#symbol-Backplane.__init__}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Backplane.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Backplane.main}

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
