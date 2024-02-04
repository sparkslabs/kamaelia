---
pagename: Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.VideoSurface
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.html){.reference}.[VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.VideoSurface.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.html){.reference}

------------------------------------------------------------------------

::: {.section}
class VideoSurface([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-VideoSurface}
----------------------------------------------------------------------------------------------------

VideoSurface(\[position\]) -\> new VideoSurface component

> Displays a pygame surface using the Pygame Display service component,
> for displaying RGB video frames sent to its \"inbox\" inbox.
>
> The surface is sized and configured by the first frame of
> (uncompressed) video data is receives.
>
> Keyword arguments:

-   position \-- (x,y) pixels position of top left corner
    (default=(0,0))

::: {.section}
### [Inboxes]{#symbol-VideoSurface.Inboxes}

-   **control** : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   **callback** : Receive callbacks from Pygame Display
-   **inbox** : Video frame data structures containing RGB data
:::

::: {.section}
### [Outboxes]{#symbol-VideoSurface.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   **display\_signal** : Outbox used for sending signals of various
    kinds to the display service
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
#### [\_\_init\_\_(self\[, position\])]{#symbol-VideoSurface.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [formatChanged(self, frame)]{#symbol-VideoSurface.formatChanged}

Returns True if frame size or pixel format is new/different for this
frame.
:::

::: {.section}
#### [main(self)]{#symbol-VideoSurface.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-VideoSurface.shutdown}
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-VideoSurface.waitBox}

Generator. yield\'s 1 until data is ready on the named inbox.
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
