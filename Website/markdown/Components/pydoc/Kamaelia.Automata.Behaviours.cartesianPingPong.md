---
pagename: Components/pydoc/Kamaelia.Automata.Behaviours.cartesianPingPong
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[cartesianPingPong](/Components/pydoc/Kamaelia.Automata.Behaviours.cartesianPingPong.html){.reference}
=============================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}

------------------------------------------------------------------------

::: {.section}
class cartesianPingPong([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-cartesianPingPong}
---------------------------------------------------------------------------------------------------------

cartesianPingPong(point,width,height,border) -\> new cartesianPingPong
component

A component that emits (x,y) values that bounce around within the
specified bounds.

Keyword arguments:

-   point \-- starting (x,y) coordinates
-   width, height \-- bounds of the area
-   border \-- distance in from bounds at which bouncing happens

::: {.section}
### [Inboxes]{#symbol-cartesianPingPong.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-cartesianPingPong.Outboxes}
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
#### [\_\_init\_\_(self, point, width, height, border)]{#symbol-cartesianPingPong.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-cartesianPingPong.main}

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
