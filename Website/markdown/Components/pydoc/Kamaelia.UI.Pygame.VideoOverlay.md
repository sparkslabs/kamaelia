---
pagename: Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.html){.reference}
===============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay.html){.reference}**
:::

-   [Pygame Video Overlay](#385){.reference}
    -   [Example Usage](#386){.reference}
    -   [How does it work?](#387){.reference}
-   [UNCOMPRESSED FRAME FORMAT](#388){.reference}
:::

::: {.section}
::: {.section}
[Pygame Video Overlay]{#pygame-video-overlay} {#385}
---------------------------------------------

Displays uncompressed video data on a pygame \'overlay\' using the
Pygame Display service.

::: {.section}
### [Example Usage]{#example-usage} {#386}

Read raw YUV data from a file and display it using VideoOverlay:

``` {.literal-block}
imagesize = (352, 288)        # "CIF" size video
fps = 15                      # framerate of video

Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
         RawYUVFramer(imagesize),
         MessageRateLimit(messages_per_second=fps, buffer=fps*2)
         VideoOverlay()
        ).activate()
```

RawYUVFramer is needed to frame raw YUV data into individual video
frames.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#387}

The component waits to receive uncompressed video frames from its
\"inbox\" inbox.

The frames must be encoded as dictionary objects in the format described
below.

When the first frame is received, the component notes the size and pixel
format of the video data and requests an appropriate \'overlay\' surface
from the Pygame Display service component, to which video can be
rendered.

NOTE: Currently the only supported pixelformat is \"YUV420\_planar\".

NOTE: A fudge factor is currently applied to the video size (see below)

Included in the request is a reference to an outbox through which the
component will send the yuv video data for future frames of video. For
video overlays, the video data must be sent direct to the Pygame Display
component rather than be rendered onto an intermediate surface.

Also included in the request is the data for the first frame of video.

When subsequent frames of video are received the yuv data is sent to the
\"yuvdata\" outbox, which by now is linked to the Pygame Display
component.

If the frame of video is of a different pixel format or size then
VideoOverlay will re-request a new overlay.

NOTE: If this happens, the component does NOT dispose of the old
surface. This behaviour should therefore be avoided at present -
repeated changes of video size/pixel format will result in multiple
overlays accumulating in the pygame display.

::: {.section}
#### [Fudge factor]{#fudge-factor}

The size of overlay requested by the VideoOverlay component is adjusted
by a fudge factor.

This is a workaround for problems with Xorg/fbdev based displays on
linux. If the overlay is precisely the right size and shape for the
data, it can\'t be displayed right. The value must be even, and
preferably small. Odd values result in the picture being
sheared/slanted.

This problem rears itself when the following version numbers are
aligned:

-   SDL : 1.2.8
-   pygame : Anything up to/including 1.7.1prerelease
-   xorg : 6.8.2
-   Linux (for fbdev) : 2.6.11.4

The fudge factor does not appear to adversely affect behaviour on other
system configurations.
:::
:::
:::

::: {.section}
[UNCOMPRESSED FRAME FORMAT]{#uncompressed-frame-format} {#388}
-------------------------------------------------------

Uncompresed video frames must be encoded as dictionaries. VidoeOverlay
requires the following entries:

``` {.literal-block}
{
  "yuv" : (y_data, u_data, v_data)  # a tuple of strings
  "size" : (width, height)          # in pixels
  "pixformat" :  "YUV420_planar"    # format of raw video data
}
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.html){.reference}.[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================

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
