---
pagename: Components/pydoc/Kamaelia.Video.CropAndScale
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.html){.reference}
=================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.CropAndScale.html){.reference}**
:::

-   [Video frame cropping and scaling](#663){.reference}
    -   [Example Usage](#664){.reference}
    -   [More details](#665){.reference}
-   [UNCOMPRESSED FRAME FORMAT](#666){.reference}
:::

::: {.section}
::: {.section}
[Video frame cropping and scaling]{#video-frame-cropping-and-scaling} {#663}
---------------------------------------------------------------------

This component applies a crop and/or scaling operation to frames of RGB
video.

Requires PIL - the [python imaging
library.](http://www.pythonware.com/products/pil/){.reference}

::: {.section}
### [Example Usage]{#example-usage} {#664}

Crop and scale a YUV4MPEG format uncompressed video file so that the
output is the region (100,100) -\>(400,300), scaled up to 720x576:

``` {.literal-block}
from Kamaelia.File.Reading import RateControlledFileReader

Pipeline( RateControlledFileReader("input.yuv4mpeg", ... ),
          YUV4MPEGToFrame(),
          ToRGB_interleaved(),
          CropAndScale(newsize=(720,576), cropbounds=(100,100,400,300)),
          ToYUV420_planar(),
          FrameToYUV4MPEG(),
          SimpleFileWriter("cropped_and_scaled.yuv4mpeg"),
        ).run()
```
:::

::: {.section}
### [More details]{#more-details} {#665}

Initialise this component specifying the region of the incoming video
frames to crop to, and the size of the desired output (the cropped
region will be scaled up/down to match this).

Send frame data structures to the \"inbox\" inbox of this component. The
frames will be cropped and scaled and output from the \"outbox\" outbox.
Only frames with one of the following pixel formats are currently
supported:

> \"RGB\_interleaved\" \"RGBA\_interleaved\" \"Y\_planar\"

See below for a description of the uncompressed frame data structure
format. Send uncompressed video frames, in the format described below,

This component supports sending data out of its outbox to a size limited
inbox. If the size limited inbox is full, this component will pause
until it is able to send out the data. Data will not be consumed from
the inbox if this component is waiting to send to the outbox.

If a producerFinished message is received on the \"control\" inbox, this
component will complete parsing any data pending in its inbox, and
finish sending any resulting data to its outbox. It will then send the
producerFinished message on out of its \"signal\" outbox and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
this component will immediately send it on out of its \"signal\" outbox
and immediately terminate. It will not complete processing, or sending
on any pending data.
:::
:::

::: {.section}
[UNCOMPRESSED FRAME FORMAT]{#uncompressed-frame-format} {#666}
-------------------------------------------------------

A frame is a dictionary data structure, containing at minimum one of
these combinations:

``` {.literal-block}
{
  "yuv" : luminance_data
  "pixformat" :  pixelformat        # format of raw video data
  "size" : (width, height)          # in pixels
}

{
  "rgb" : rgb_interleaved_data
  "pixformat" :  pixelformat        # format of raw video data
  "size" : (width, height)          # in pixels
}
```

CropAndScale only guarantees to fill in the fields above. Any other
fields will be transparently passed through, unmodified.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.html){.reference}.[CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.CropAndScale.html){.reference}
=============================================================================================================================================================================================================================================================================================

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
