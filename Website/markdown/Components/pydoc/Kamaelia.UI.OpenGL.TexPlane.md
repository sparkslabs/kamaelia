---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.TexPlane
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[TexPlane](/Components/pydoc/Kamaelia.UI.OpenGL.TexPlane.html){.reference}
=======================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TexPlane](/Components/pydoc/Kamaelia.UI.OpenGL.TexPlane.TexPlane.html){.reference}**
:::

-   [Textured Plane](#306){.reference}
    -   [Example Usage](#307){.reference}
    -   [How does it work?](#308){.reference}
:::

::: {.section}
Textured Plane {#306}
==============

A plane showing a texture loaded from an image file.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

::: {.section}
[Example Usage]{#example-usage} {#307}
-------------------------------

A plane showing an image loaded from the file \"nemo.jpeg\":

``` {.literal-block}
PLANE = TexPlane(position=(0, 0,-6), texture="nemo.jpeg").activate()

Axon.Scheduler.scheduler.run.runThreads()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#308}
--------------------------------------

This component is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides \_\_init\_\_(),
setup(), draw().

In setup() the method loadTexture() get called which loads the texure
from the image file specified. If the image in the file has dimensions
which are not equal a power of two, the texture dimensions get enlarged
(this is needed because of OpenGL texturing limitations).

In draw() a simple plane is drawn whith the loaded texture on it.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[TexPlane](/Components/pydoc/Kamaelia.UI.OpenGL.TexPlane.html){.reference}.[TexPlane](/Components/pydoc/Kamaelia.UI.OpenGL.TexPlane.TexPlane.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================

::: {.section}
class TexPlane(OpenGLComponent) {#symbol-TexPlane}
-------------------------------

TexPlane(\...) -\> A new TexPlane component.

A plane showing a texture loaded from an image file.

Keyword arguments:

-   tex \-- image file name
-   pixelscaling \-- factor for translation from pixels to units in 3D
    space (default=100.0)

::: {.section}
### [Inboxes]{#symbol-TexPlane.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-TexPlane.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-TexPlane.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [draw(self)]{#symbol-TexPlane.draw}

Draws textured plane.
:::

::: {.section}
#### [loadTexture(self)]{#symbol-TexPlane.loadTexture}

Loads texture from specified image file.
:::

::: {.section}
#### [setup(self)]{#symbol-TexPlane.setup}

Load texture.
:::
:::

::: {.section}
:::
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
