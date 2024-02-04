---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleCube](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube.html){.reference}
===========================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleCube](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube.SimpleCube.html){.reference}**
:::

-   [Simple Cube component](#334){.reference}
    -   [Example Usage](#335){.reference}
    -   [How does it work?](#336){.reference}
:::

::: {.section}
Simple Cube component {#334}
=====================

A simple cube for the OpenGL display service.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

::: {.section}
[Example Usage]{#example-usage} {#335}
-------------------------------

Three cubes in different positions with various rotation and sizes:

``` {.literal-block}
Graphline(
    CUBEC = SimpleCube(position=(0, 0,-12), rotation=(40,90,0), size=(1,1,1)).activate(),
    CUBER = SimpleCube(position=(4,0,-22), size=(2,2,2)).activate(),
    CUBEB = SimpleCube(position=(0,-4,-18), rotation=(0,180,20), size=(1,3,2)).activate(),
    linkages = {}
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#336}
--------------------------------------

SimpleButton is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides draw().

In draw() a simple cube made of 6 quads with different colours is drawn.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleCube](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube.html){.reference}.[SimpleCube](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube.SimpleCube.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleCube(OpenGLComponent) {#symbol-SimpleCube}
---------------------------------

SimpleCube(\...) -\> new SimpleCube component.

A simple cube for the OpenGL display service.

::: {.section}
### [Inboxes]{#symbol-SimpleCube.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleCube.Outboxes}
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
#### [draw(self)]{#symbol-SimpleCube.draw}
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
