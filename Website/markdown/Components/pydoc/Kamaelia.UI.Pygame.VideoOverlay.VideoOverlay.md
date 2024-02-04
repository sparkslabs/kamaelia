---
pagename: Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.html){.reference}.[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.html){.reference}

------------------------------------------------------------------------

::: {.section}
class VideoOverlay([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-VideoOverlay}
----------------------------------------------------------------------------------------------------

VideoOverlay() -\> new VideoOverlay component

Displays a pygame video overlay using the Pygame Display service
component. The overlay is sized and configured by the first frame of
(uncompressed) video data is receives.

NB: Currently, the only supported pixel format is \"YUV420\_planar\"

::: {.section}
### [Inboxes]{#symbol-VideoOverlay.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Receives uncompressed video frames
:::

::: {.section}
### [Outboxes]{#symbol-VideoOverlay.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling
-   **yuvdata** : Sending yuv video data to overlay display service
-   **displayctrl** : Sending requests to the Pygame Display service
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-VideoOverlay.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [formatChanged(self, frame)]{#symbol-VideoOverlay.formatChanged}

Returns True if frame size or pixel format is new/different for this
frame.
:::

::: {.section}
#### [main(self)]{#symbol-VideoOverlay.main}

Main loop.
:::

::: {.section}
#### [newOverlay(self, frame)]{#symbol-VideoOverlay.newOverlay}

Request an overlay to suit the supplied frame of data
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-VideoOverlay.waitBox}

Generator. yields 1 until data ready on the named inbox.
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
