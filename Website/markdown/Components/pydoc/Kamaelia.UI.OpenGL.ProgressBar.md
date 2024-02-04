---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[ProgressBar](/Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar.html){.reference}
=============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ProgressBar](/Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar.ProgressBar.html){.reference}**
:::

-   [Progress Bar](#348){.reference}
    -   [Example Usage](#349){.reference}
    -   [How does it work?](#350){.reference}
:::

::: {.section}
Progress Bar {#348}
============

A progress bar widget for the OpenGL display service.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

::: {.section}
[Example Usage]{#example-usage} {#349}
-------------------------------

A progress bar with changing value:

``` {.literal-block}
Graphline(
    BOUNCE = bouncingFloat(0.5),
    PROGRESS = ProgressBar(size = (3, 0.5, 0.2), position=(0,0,-10), progress=0.5),
    linkages = {
        ("BOUNCE", "outbox"):("PROGRESS", "progress"),
    }
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#350}
--------------------------------------

ProgressBar is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides \_\_init\_\_(),
draw(), handleEvents() and frame().

This component basically draws a cuboid shaped cage and inside of it a
transparent bar indicating a percentage.

The percentage values are received at the \"progress\" inbox. The values
must be in the range \[0,1\]. If the value is 0.0, the bar is not drawn
at all, if 1.0 the bar has its maximum length. Received values which lie
outside of this range are clamped to it.

Because the progress bar is transparent, the widget has to be drawn in a
special order. First, the cage is drawn normally. Then the depth buffer
is made read only and the transparent bar is drawn.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[ProgressBar](/Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar.html){.reference}.[ProgressBar](/Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar.ProgressBar.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ProgressBar(OpenGLComponent) {#symbol-ProgressBar}
----------------------------------

ProgressBar(\...) -\> new ProgressBar component.

Create a progress bar widget using the OpenGLDisplay service. Shows a
tranparent bar indicating a percentage.

Keyword arguments:

-   cagecolour \-- Cage colour (default=(0,0,0))
-   barcolour \-- Bar colour (default=(200,200,244))
-   progress \-- Initial progress value (default=0.0)

::: {.section}
### [Inboxes]{#symbol-ProgressBar.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-ProgressBar.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-ProgressBar.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [draw(self)]{#symbol-ProgressBar.draw}
:::

::: {.section}
#### [frame(self)]{#symbol-ProgressBar.frame}
:::

::: {.section}
#### [handleProgress(self)]{#symbol-ProgressBar.handleProgress}
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
