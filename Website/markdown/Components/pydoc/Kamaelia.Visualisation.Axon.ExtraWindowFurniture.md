---
pagename: Components/pydoc/Kamaelia.Visualisation.Axon.ExtraWindowFurniture
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[Axon](/Components/pydoc/Kamaelia.Visualisation.Axon.html){.reference}.[ExtraWindowFurniture](/Components/pydoc/Kamaelia.Visualisation.Axon.ExtraWindowFurniture.html){.reference}
=====================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Kamaelia Cat logo renderer](#407){.reference}
    -   [Example Usage](#408){.reference}
    -   [How does it work?](#409){.reference}
:::

::: {.section}
Kamaelia Cat logo renderer {#407}
==========================

Renderer for the topology viewer framework that renders a Kamaelia cat
logo to the top left corner on rendering pass 10.

::: {.section}
[Example Usage]{#example-usage} {#408}
-------------------------------

Create a topology viewer component that also renders
\'ExtraWindowFurniture\' to the display surface:

``` {.literal-block}
TopologyViewer( extraDrawing = ExtraWindowFurniture(),
                ...
              ).activate()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#409}
--------------------------------------

Instances of this class provide a render() generator that renders a
Kamaelia cat logo at coordinates (8,8) to the specified pygame surface.
The cat logo is scaled so its longest dimension (width or height) is 64
pixels.

Rendering is performed by the generator, returned when the render()
method is called. Its behaviour is that needed for the framework for
multi-pass rendering that is used by TopologyViewer.

The generator yields the number of the rendering pass it wishes to be
next on next. Each time it is subsequently called, it performs the
rendering required for that pass. It then yields the number of the next
required pass or completes if there is no more rendering required.

An setOffset() method is also implemented to allow the particles
coordinates to be offset. This therefore makes it possible to scroll the
particles around the display surface.

See TopologyViewer for more details.
:::
:::

------------------------------------------------------------------------

::: {.section}
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
