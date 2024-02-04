---
pagename: Components/pydoc/Kamaelia.Chassis.Graphline.Graphline
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.Graphline.html){.reference}
======================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Graphline([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Graphline}
-------------------------------------------------------------------------------------------------

Graphline(linkages,\*\*components) -\> new Graphline component

Encapsulates the specified set of components and wires them up with the
specified linkages.

Keyword arguments:

-   linkages \-- dictionary mapping (\"componentname\",\"boxname\") to
    (\"componentname\",\"boxname\")
-   components \-- dictionary mapping names to component instances
    (default is nothing)

::: {.section}
### [Inboxes]{#symbol-Graphline.Inboxes}

-   **control** :
-   **inbox** :
:::

::: {.section}
### [Outboxes]{#symbol-Graphline.Outboxes}

-   **outbox** :
-   **signal** :
-   **\_cs** : For signaling to subcomponents shutdown
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
#### [\_\_init\_\_(self, linkages, \*\*components)]{#symbol-Graphline.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addExternalPostboxes(self)]{#symbol-Graphline.addExternalPostboxes}

Adds to self.Inboxes and self.Outboxes any postboxes mentioned in
self.layout that don\'t yet exist
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Graphline.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Graphline.main}

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
