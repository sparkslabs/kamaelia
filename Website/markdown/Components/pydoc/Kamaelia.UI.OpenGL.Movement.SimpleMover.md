---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleMover
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[SimpleMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleMover.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SimpleMover([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleMover}
---------------------------------------------------------------------------------------------------

SimpleMover(\...) -\> A new SimpleMover component.

A simple mover component mostly for testing. Moves OpenGLComponents
between the specified borders if connected to their \"position\" boxes.
The amount of movement every frame and the origin can also be specified.

Keyword arguments:

-   amount \-- amount of movement every frame sent
    (default=(0.03,0.03,0.03))
-   borders \-- borders of every dimension (default=(5,5,5))
-   origin \-- origin of movement (default=(0,0,-20))

::: {.section}
### [Inboxes]{#symbol-SimpleMover.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleMover.Outboxes}
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
#### [\_\_init\_\_(self\[, amount\]\[, borders\]\[, origin\])]{#symbol-SimpleMover.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-SimpleMover.main}
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
