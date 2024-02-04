---
pagename: Components/pydoc/Kamaelia.Video.CropAndScale.CropAndScale
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.html){.reference}.[CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.CropAndScale.html){.reference}
=============================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Video.CropAndScale.html){.reference}

------------------------------------------------------------------------

::: {.section}
class CropAndScale([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-CropAndScale}
----------------------------------------------------------------------------------------------------

CropAndScale(newsize, cropbounds) -\> new CropAndScale component.

Crops and scales frames of video in RGB format.

Keyword arguments:

-   newsize \-- (width, height) of the resulting output video frames (in
    pixels)
-   cropbounds \-- (x0,y0,x1,y1) region to crop out from the incoming
    video frames (in pixels)

::: {.section}
### [Inboxes]{#symbol-CropAndScale.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-CropAndScale.Outboxes}
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
#### [\_\_init\_\_(self, newsize, cropbounds)]{#symbol-CropAndScale.__init__}
:::

::: {.section}
#### [canStop(self)]{#symbol-CropAndScale.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-CropAndScale.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-CropAndScale.main}
:::

::: {.section}
#### [mustStop(self)]{#symbol-CropAndScale.mustStop}
:::

::: {.section}
#### [processFrame(self, frame)]{#symbol-CropAndScale.processFrame}
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-CropAndScale.waitSend}
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
