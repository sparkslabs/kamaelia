---
pagename: Components/pydoc/Kamaelia.UI.Pygame.VideoSurface
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.html){.reference}
===============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.VideoSurface.html){.reference}**
:::

-   [Pygame Video Surface](#367){.reference}
    -   [Example Usage](#368){.reference}
    -   [How does it work?](#369){.reference}
-   [UNCOMPRESSED FRAME FORMAT](#370){.reference}
:::

::: {.section}
::: {.section}
[Pygame Video Surface]{#pygame-video-surface} {#367}
---------------------------------------------

Displays uncompressed RGB video data on a pygame surface using the
Pygame Display service.

::: {.section}
### [Example Usage]{#example-usage} {#368}

Read raw YUV data from a file, convert it to interleaved RGB and display
it using VideoSurface:

``` {.literal-block}
imagesize = (352, 288)        # "CIF" size video
fps = 15                      # framerate of video

Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
         RawYUVFramer(imagesize),
         MessageRateLimit(messages_per_second=fps, buffer=fps*2),
         ToRGB_interleaved(),
         VideoSurface(),
        ).activate()
```

RawYUVFramer is needed to frame raw YUV data into individual video
frames. ToRGB\_interleaved is needed to convert the 3 planes of Y, U and
V data to a single plane containing RGB data interleaved (R, G, B, R, G,
B, R, G, B, \...)
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#369}

The component waits to receive uncompressed video frames from its
\"inbox\" inbox.

The frames must be encoded as dictionary objects in the format described
below.

When the first frame is received, the component notes the size and pixel
format of the video data and requests an appropriate surface from the
Pygame Display service component, to which video can be rendered.

NOTE: Currently the only supported pixelformat is \"RGB\_interleaved\".

When subsequent frames of video are received the rgb data is rendered to
the surface and the Pygame Display service is notified that the surface
needs redrawing.

At present, VideoSurface cannot cope with a change of pixel format or
video size mid sequence.
:::
:::

::: {.section}
[UNCOMPRESSED FRAME FORMAT]{#uncompressed-frame-format} {#370}
-------------------------------------------------------

Uncompresed video frames must be encoded as dictionaries. VideoSurface
requires the following entries:

``` {.literal-block}
{
  "rgb" : rgbdata                    # a string containing RGB video data
  "size" : (width, height)           # in pixels
  "pixformat" : "RGB_interleaved"    # format of raw video data
}
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.html){.reference}.[VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.VideoSurface.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================

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
