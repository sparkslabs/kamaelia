---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Label.Label
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.html){.reference}.[Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.Label.html){.reference}
============================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Label.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Label(OpenGLComponent) {#symbol-Label}
----------------------------

Label(\...) -\> A new Label component.

A Label widget for the OpenGL display service.

Keyword arguments:

-   caption \-- Label caption (default=\"Label\")
-   bgcolour \-- Colour of surfaces behind caption
    (default=(200,200,200))
-   fgcolour \-- Colour of the caption text (default=(0,0,0)
-   sidecolour \-- Colour of side planes (default=(200,200,244))
-   margin \-- Margin size in pixels (default=8)
-   fontsize \-- Font size for caption text (default=50)
-   pixelscaling \-- Factor to convert pixels to units in 3d, ignored if
    size is specified (default=100)
-   thickness \-- Thickness of Label widget, ignored if size is
    specified (default=0.3)

::: {.section}
### [Inboxes]{#symbol-Label.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Label.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Label.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [buildCaption(self)]{#symbol-Label.buildCaption}

Pre-render the text to go on the label.
:::

::: {.section}
#### [draw(self)]{#symbol-Label.draw}

Draw label cuboid.
:::

::: {.section}
#### [setup(self)]{#symbol-Label.setup}

Build caption.
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
