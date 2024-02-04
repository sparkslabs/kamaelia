---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.PygameWrapper
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.html){.reference}.[PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.PygameWrapper.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.html){.reference}

------------------------------------------------------------------------

::: {.section}
class PygameWrapper(OpenGLComponent) {#symbol-PygameWrapper}
------------------------------------

PygameWrapper(\...) -\> A new PygameWrapper component.

A wrapper for two dimensional pygame components that allows to display
them on a Plane in 3D using OpenGL.

Keyword arguments:

-   wrap \-- Pygame component to wrap
-   pixelscaling \-- Factor to convert pixels to units in 3d, ignored if
    size is specified (default=100)
-   sidecolour \-- Colour of side and back planes
    (default=(200,200,244))
-   thickness \-- Thickness of wrapper, ignored if size is specified
    (default=0.3)

::: {.section}
### [Inboxes]{#symbol-PygameWrapper.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PygameWrapper.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-PygameWrapper.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [draw(self)]{#symbol-PygameWrapper.draw}

Draw cuboid.
:::

::: {.section}
#### [frame(self)]{#symbol-PygameWrapper.frame}
:::

::: {.section}
#### [handleEventRequests(self)]{#symbol-PygameWrapper.handleEventRequests}
:::

::: {.section}
#### [handleEvents(self)]{#symbol-PygameWrapper.handleEvents}
:::

::: {.section}
#### [setup(self)]{#symbol-PygameWrapper.setup}
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
