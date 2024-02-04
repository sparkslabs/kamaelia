---
pagename: Docs/Axon/Axon.Ipc.newComponent
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[newComponent](/Docs/Axon/Axon.Ipc.newComponent.html){.reference}
------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class newComponent(ipc) {#symbol-newComponent}
-----------------------

::: {.section}
newComponent(\*components) -\> new newComponent ipc message.

Message used to inform the scheduler of a new component that needs a
thread of control and activating.

Use within a microprocess by yielding one back to the scheduler.

Arguments:

-   the components to be activated
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*components)]{#symbol-newComponent.__init__}
:::

::: {.section}
#### [components(self)]{#symbol-newComponent.components}

Returns the list of components to be activated
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
