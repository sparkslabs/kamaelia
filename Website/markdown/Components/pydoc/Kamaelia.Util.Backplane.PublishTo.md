---
pagename: Components/pydoc/Kamaelia.Util.Backplane.PublishTo
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}.[PublishTo](/Components/pydoc/Kamaelia.Util.Backplane.PublishTo.html){.reference}
==========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}

------------------------------------------------------------------------

::: {.section}
class PublishTo([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PublishTo}
-------------------------------------------------------------------------------------------------

PublishTo(destination) -\> new PublishTo component

Publishes data to a named Backplane. Any data sent to the \"inbox\"
inbox is sent to all (any) subscribers to the same named Backplane.

Keyword arguments:

-   destination \-- the name of the Backplane to publish data to

::: {.section}
### [Inboxes]{#symbol-PublishTo.Inboxes}

-   **control** : Shutdown signalling (doesn\'t shutdown the Backplane)
-   **inbox** : Send to here data to be published to the backplane
:::

::: {.section}
### [Outboxes]{#symbol-PublishTo.Outboxes}

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
#### [\_\_init\_\_(self, destination)]{#symbol-PublishTo.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-PublishTo.main}

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
