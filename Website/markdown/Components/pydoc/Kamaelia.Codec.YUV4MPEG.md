---
pagename: Components/pydoc/Kamaelia.Codec.YUV4MPEG
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[YUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}
=========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [FrameToYUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.FrameToYUV4MPEG.html){.reference}**
-   **component
    [YUV4MPEGToFrame](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.YUV4MPEGToFrame.html){.reference}**
:::

-   [Parsing and Creation of YUV4MPEG format files](#96){.reference}
    -   [Example Usage](#97){.reference}
    -   [YUV4MPEGToFrame Behaviour](#98){.reference}
    -   [FrameToYUV4MPEG Behaviour](#99){.reference}
-   [UNCOMPRESSED FRAME FORMAT](#100){.reference}
:::

::: {.section}
::: {.section}
[Parsing and Creation of YUV4MPEG format files]{#parsing-and-creation-of-yuv4mpeg-format-files} {#96}
-----------------------------------------------------------------------------------------------

YUV4MPEGToFrame parses YUV4MPEG format data sent to its \"inbox\" inbox
and sends video fram data structures to its \"outbox\" outbox.

FrameToYUV4MPEG does the reverse - taking frame data structures sent to
its \"inbox\" inbox and outputting YUV4MPEG format data to its
\"outbox\" outbox.\"

The YUV4MPEG file format is supported by many tools, such as mjpegtools,
mplayer/mencoder, and ffmpeg.

::: {.section}
### [Example Usage]{#example-usage} {#97}

Playback a YUV4MPEG format file:

``` {.literal-block}
Pipeline( RateControlledFileReader("video.yuv4mpeg",readmode="bytes", ...),
          YUV4MPEGToFrame(),
          VideoOverlay()
        ).run()
```

Decode a dirac encoded video file to a YUV4MPEG format file:

``` {.literal-block}
Pipeline( RateControlledFileReader("video.dirac",readmode="bytes", ...),
          DiracDecoder(),
          FrameToYUV4MPEG(),
          SimpleFileWriter("output.yuv4mpeg")
        ).run()
```
:::

::: {.section}
### [YUV4MPEGToFrame Behaviour]{#yuv4mpegtoframe-behaviour} {#98}

Send binary data as strings containing YUV4MPEG format data to the
\"inbox\" inbox and frame data structures will be sent out of the
\"outbox\" outbox as soon as they are parsed.

See below for a description of the uncompressed frame data structure
format.

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

::: {.section}
### [FrameToYUV4MPEG Behaviour]{#frametoyuv4mpeg-behaviour} {#99}

Send frame data structures to the \"inbox\" inbox of this component.
YUV4MPEG format binary string data will be sent out of the \"outbox\"
outbox.

See below for a description of the uncompressed frame data structure
format.

The header data for the YUV4MPEG file is determined from the first
frame.

All frames sent to this component must therefore be in the same pixel
format and size, otherwise the output data will not be valid YUV4MPEG.

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
[UNCOMPRESSED FRAME FORMAT]{#uncompressed-frame-format} {#100}
-------------------------------------------------------

A frame is a dictionary data structure. It must, at minimum contain the
first 3 (\"yuv\", \"size\" and \"pixformat\"):

``` {.literal-block}
{
  "yuv" : (y_data, u_data, v_data)  # a tuple of strings
  "size" : (width, height)          # in pixels
  "pixformat" :  pixelformat        # format of raw video data
  "frame_rate" : fps                # frames per second
  "interlaced" : 0 or not 0         # non-zero if the frame is two interlaced fields
  "topfieldfirst" : 0 or not 0      # non-zero the first field comes first in the data
  "pixel_aspect" : fraction         # aspect ratio of pixels
  "sequence_meta" : metadata        # string containing extended metadata
                                    # (no whitespace or control characters)
}
```

All other fields are optional when providing frames to FrameToYUV4MPEG.

YUV4MPEGToFrame only guarantees to fill inthe YUV data itself. All other
fields will be filled in if the relevant header data is detected in the
file.

The pixel formats recognised (and therefore supported) are:

``` {.literal-block}
"YUV420_planar"
"YUV411_planar"
"YUV422_planar"
"YUV444_planar"
"YUV4444_planar"
"Y_planar"
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[YUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}.[FrameToYUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.FrameToYUV4MPEG.html){.reference}
=======================================================================================================================================================================================================================================================================================

::: {.section}
class FrameToYUV4MPEG([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-FrameToYUV4MPEG}
-------------------------------------------------------------------------------------------------------

FrameToYUV4MPEG() -\> new FrameToYUV4MPEG component.

Parses uncompressed video frame data structures sent to its \"inbox\"
inbox and writes YUV4MPEG format binary data as strings to its
\"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-FrameToYUV4MPEG.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-FrameToYUV4MPEG.Outboxes}
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
#### [canShutdown(self)]{#symbol-FrameToYUV4MPEG.canShutdown}

Returns true if the component should terminate when it has finished
processing any pending data.
:::

::: {.section}
#### [checkShutdown(self)]{#symbol-FrameToYUV4MPEG.checkShutdown}

Collects any new shutdown messages arriving at the \"control\" inbox,
and ensures self.shutdownMsg contains the highest priority one
encountered so far.
:::

::: {.section}
#### [main(self)]{#symbol-FrameToYUV4MPEG.main}

Main loop
:::

::: {.section}
#### [mustShutdown(self)]{#symbol-FrameToYUV4MPEG.mustShutdown}

Returns true if the component should terminate immediately.
:::

::: {.section}
#### [sendoutbox(self, data)]{#symbol-FrameToYUV4MPEG.sendoutbox}

Generator.

Sends data out of the \"outbox\" outbox. If the destination is full
(noSpaceInBox exception) then it waits until there is space. It keeps
retrying until it succeeds.

If the component is ordered to immediately terminate then \"STOP\" is
raised as an exception.
:::

::: {.section}
#### [write\_frame(self, frame)]{#symbol-FrameToYUV4MPEG.write_frame}

Generator.

Writes out YUV4MPEG format frame marker and data.
:::

::: {.section}
#### [write\_header(self, frame)]{#symbol-FrameToYUV4MPEG.write_header}

Generator.

Sends the YUV4MPEG format header to the \"outbox\" outbox, based on
attributes of the supplied frame data structure.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[YUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}.[YUV4MPEGToFrame](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.YUV4MPEGToFrame.html){.reference}
=======================================================================================================================================================================================================================================================================================

::: {.section}
class YUV4MPEGToFrame([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-YUV4MPEGToFrame}
-------------------------------------------------------------------------------------------------------

YUV4MPEGToFrame() -\> new YUV4MPEGToFrame component.

Parses YUV4MPEG format binarydata, sent as strings to its \"inbox\"
inbox and outputs uncompressed video frame data structures to its
\"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-YUV4MPEGToFrame.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-YUV4MPEGToFrame.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-YUV4MPEGToFrame.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkShutdown(self)]{#symbol-YUV4MPEGToFrame.checkShutdown}

Collects any new shutdown messages arriving at the \"control\" inbox,
and returns \"NOW\" if immediate shutdown is required, or \"WHENEVER\"
if the component can shutdown when it has finished processing pending
data.
:::

::: {.section}
#### [main(self)]{#symbol-YUV4MPEGToFrame.main}

Main loop
:::

::: {.section}
#### [readbytes(self, size)]{#symbol-YUV4MPEGToFrame.readbytes}

Generator.

Read the specified number of bytes from the stream of chunks of binary
string data arriving at the \"inbox\" inbox.

Any excess data is placed into self.remainder ready for the next call to
self.readline or self.readbytes.

Data is only read from the inbox when required. It is not preemptively
fetched.

The read data is placed into self.bytesread

If a shutdown is detected, self.bytesread is set to \"\" and this
generator immediately returns.
:::

::: {.section}
#### [readline(self)]{#symbol-YUV4MPEGToFrame.readline}

Generator.

Read up to the next newline char from the stream of chunks of binary
string data arriving at the \"inbox\" inbox.

Any excess data is placed into self.remainder ready for the next call to
self.readline or self.readbytes.

Data is only read from the inbox when required. It is not preemptively
fetched.

The read data is placed into self.bytesread

If a shutdown is detected, self.bytesread is set to \"\" and this
generator immediately returns.
:::

::: {.section}
#### [safesend(self, data, boxname)]{#symbol-YUV4MPEGToFrame.safesend}

Generator.

Sends data out of the named outbox. If the destination is full
(noSpaceInBox exception) then it waits until there is space and retries
until it succeeds.

If a shutdownMicroprocess message is received, returns early.
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
