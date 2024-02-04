---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SkyGrassBackground](/Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground.html){.reference}
===========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SkyGrassBackground](/Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground.SkyGrassBackground.html){.reference}**
:::

-   [Sky & Grass background](#319){.reference}
    -   [Example Usage](#320){.reference}
:::

::: {.section}
Sky & Grass background {#319}
======================

A very simple component showing a plane with the upper half coloured
light blue and the lower half green. Can be used for a background.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

::: {.section}
[Example Usage]{#example-usage} {#320}
-------------------------------

Only a background:

``` {.literal-block}
SkyGrassBackground(size=(5000,5000,0), position=(0,0,-100)).activate()
Axon.Scheduler.scheduler.run.runThreads()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SkyGrassBackground](/Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground.html){.reference}.[SkyGrassBackground](/Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground.SkyGrassBackground.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SkyGrassBackground(OpenGLComponent) {#symbol-SkyGrassBackground}
-----------------------------------------

SkyGrassBackground(\...) -\> A new SkyGrassBackground component.

A very simple component showing a plane with the upper half coloured
light blue and the lower half green. Can be used for a background.

::: {.section}
### [Inboxes]{#symbol-SkyGrassBackground.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SkyGrassBackground.Outboxes}
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
#### [draw(self)]{#symbol-SkyGrassBackground.draw}
:::

::: {.section}
#### [setup(self)]{#symbol-SkyGrassBackground.setup}
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
