---
pagename: Components/pydoc/Kamaelia.Codec.Dirac
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Dirac](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}
===================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DiracDecoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder.html){.reference}**
-   **component
    [DiracEncoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracEncoder.html){.reference}**
:::

-   [Dirac video decoder](#81){.reference}
    -   [Example Usage](#82){.reference}
    -   [More detail](#83){.reference}
-   [Dirac video encoder](#84){.reference}
    -   [Example Usage](#85){.reference}
    -   [More detail](#86){.reference}
-   [UNCOMPRESSED FRAME FORMAT](#87){.reference}
:::

::: {.section}
::: {.section}
[Dirac video decoder]{#dirac-video-decoder} {#81}
-------------------------------------------

This component decodes a stream of video, coded using the Dirac codec,
into frames of YUV video data.

This component is a thin wrapper around the Dirac Python bindings.

::: {.section}
### [Example Usage]{#example-usage} {#82}

A simple video player:

``` {.literal-block}
Pipeline(ReadFileAdapter("diracvideofile.drc", ...other args...),
         DiracDecoder(),
         RateLimit(framerate),
         VideoOverlay()
        ).activate()
```
:::

::: {.section}
### [More detail]{#more-detail} {#83}

Reads a raw dirac data stream, as strings, from the \"inbox\" inbox.

Sends out frames of decoded video to the \"outbox\" outbox.

The frames may not be emitted at a constant rate. You may therefore need
to buffer and rate limit them if displaying them.

The decoder will terminate if it receives a shutdownMicroprocess message
on its \"control\" inbox. The message is passed on out of the \"signal\"
outbox.

It will ignore producerFinished messages.

The decoder is able to work out from the data stream when it has reached
the end of the stream. It then sends a producerFinished message out of
the \"signal\" outbox and terminates.

For more information see the Dirac Python bindings documentation.
:::
:::

::: {.section}
[Dirac video encoder]{#dirac-video-encoder} {#84}
-------------------------------------------

This component encodes frames of YUV video data with the Dirac codec.

This component is a thin wrapper around the Dirac Python bindings.

::: {.section}
### [Example Usage]{#id1} {#85}

Raw video file encoder:

``` {.literal-block}
imagesize = (352, 288)      # "CIF" size video

Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
         RawYUVFramer(imagesize),
         DiracEncoder(preset="CIF"),
         WriteFileAdapter("diracvideo.drc")
        ).activate()
```

RawYUVFramer is needed to frame raw YUV data into individual video
frames.
:::

::: {.section}
### [More detail]{#id2} {#86}

Reads video frames from the \"inbox\" inbox.

Sends out encoded video data (as strings) in chunks to the \"outbox\"
outbox.

The encoder can be configured with simple presets and/or more detailed
encoder and sequence parameters. Encoder and sequence parameters
override those set with a preset.

For more information see the Dirac Python bindings documentation.

The encoder will terminate if it receives a shutdownMicroprocess or
producerFinished message on its \"control\" inbox. The message is passed
on out of the \"signal\" outbox. If the message is producerFinished,
then it will also send any data still waiting to be sent out of the
\"outbox\" outbox, otherwise any pending data is lost.

The component does not yet support output of instrumentation or locally
decoded frames (the \"verbose\" option).
:::
:::

::: {.section}
[UNCOMPRESSED FRAME FORMAT]{#uncompressed-frame-format} {#87}
-------------------------------------------------------

Uncompresed video frames are output by the decoder, as dictionaries.
Each contains the following entries:

``` {.literal-block}
{
  "yuv" : (y_data, u_data, v_data)  # a tuple of strings
  "size" : (width, height)          # in pixels
  "frame_rate" : fps                # frames per second
  "interlaced" : 0 or not 0         # non-zero if the frame is two interlaced fields
  "topfieldfirst" : 0 or not 0      # non-zero the first field comes first in the data
  "pixformat" :  "YUV420_planar"    # format of raw video data
  "chroma_size" : (width, height)   # in pixels, for the u and v data
}
```

The encoder expects data in the same format, but only requires \"yuv\",
\"size\", and \"pixformat\".
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Dirac](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}.[DiracDecoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder.html){.reference}
========================================================================================================================================================================================================================================================================

::: {.section}
class DiracDecoder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DiracDecoder}
----------------------------------------------------------------------------------------------------

DiracDecoder() -\> new Dirac decoder component

Creates a component that decodes Dirac video.

::: {.section}
### [Inboxes]{#symbol-DiracDecoder.Inboxes}

-   **control** : for shutdown signalling
-   **inbox** : Strings containing an encoded dirac video stream
:::

::: {.section}
### [Outboxes]{#symbol-DiracDecoder.Outboxes}

-   **outbox** : YUV decoded video frames
-   **signal** : for shutdown/completion signalling
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
#### [\_\_init\_\_(self)]{#symbol-DiracDecoder.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-DiracDecoder.main}

Main loop
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Dirac](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}.[DiracEncoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracEncoder.html){.reference}
========================================================================================================================================================================================================================================================================

::: {.section}
class DiracEncoder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DiracEncoder}
----------------------------------------------------------------------------------------------------

DiracEncoder(\[preset\]\[,verbose\]\[,encParams\]\[,seqParams\]\[,allParams\])
-\> new Dirac encoder component

Creates a component to encode video using the Dirac codec. Configuration
based on optional preset, optionally overriden by individual encoder and
sequence parameters. All three \'params\' arguments are munged together,
so do what you like :)

Keyword arguments:

-   preset \-- \"CIF\" or \"SD576\" or \"HD720\" or \"HD1080\" (presets
    for common video formats)
-   verbose \-- NOT YET IMPLEMENTED (IGNORED)
-   encParams \-- dict of encoder setup parameters only
-   seqParams \-- dict of video sequence parameters only
-   allParams \-- dict of encoder setup parameters, sequence parameters,
    and source parameters, all munged together

::: {.section}
### [Inboxes]{#symbol-DiracEncoder.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-DiracEncoder.Outboxes}
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
#### [\_\_init\_\_(self\[, preset\]\[, verbose\]\[, encParams\]\[, seqParams\]\[, allParams\])]{#symbol-DiracEncoder.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-DiracEncoder.main}

Main loop
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
