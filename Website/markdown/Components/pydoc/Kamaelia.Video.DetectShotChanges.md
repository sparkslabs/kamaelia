---
pagename: Components/pydoc/Kamaelia.Video.DetectShotChanges
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.html){.reference}
===========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.DetectShotChanges.html){.reference}**
:::

-   [Detecting cuts/shot changes in video](#667){.reference}
    -   [Example Usage](#668){.reference}
    -   [More detail](#669){.reference}
    -   [Implementation details](#670){.reference}
-   [UNCOMPRESSED FRAME FORMAT](#671){.reference}
:::

::: {.section}
::: {.section}
[Detecting cuts/shot changes in video]{#detecting-cuts-shot-changes-in-video} {#667}
-----------------------------------------------------------------------------

DetectShotChanges takes in (framenumber, videoframe) tuples on its
\"inbox\" inbox and attempts to detect where shot changes have probably
occurred in the sequence. When it thinks one has ocurred, a
(framenumber, confidencevalue) tuple is sent out of the \"outbox\"
outbox.

::: {.section}
### [Example Usage]{#example-usage} {#668}

Reading in a video in uncompressed YUV4MPEG file format, and outputting
the frame numbers (and confidence values) where cuts probably occur:

``` {.literal-block}
Pipeline( RateControlledFileReader(..)
          YUV4MPEGToFrame(),
          TagWithSequenceNumber(),      # pair up frames with a frame number
          DetectShotChanges(threshold=0.85),
          ConsoleEchoer(),
        ).run()
```

Expect output like this:

``` {.literal-block}
(17, 0.885)(18, 0.912)(56, 0.91922)(212, 0.818)(213, 0.825)(214, 0.904) ...
```
:::

::: {.section}
### [More detail]{#more-detail} {#669}

Send (frame-number, video-frame) tuples to this component\'s \"inbox\"
inbox and (frame-number, confidence-value) tuples will be sent out of
the \"outbox\" outbox whenever it thinks a cut has occurred.

Frames must be in a YUV format. See below for details. Frame numbers
need not necessarily be sequential; but they must be unique! If they are
not, then it is your own fault when you can\'t match up detected shot
changes to actual video frames!

Internally, the cut detector calculates a \'confidence\' value
representing how likely that a shot change has occurred. At
initialisation you set a threshold value - if the confidence value
reaches or exceeds this threshold, then a cut is deemed to have taken
place, and output will be generated.

How do you choose a threshold? It is a rather inexact science (as is the
subjective decision of whether something consitutes a shot change!) -
you really need to get a feel for it experimentally. As a rough guide,
values between 0.8 and 0.9 are usually reasonable, depending on the type
of video material.

Because of the necessary signal processing, this component has a delay
of several frames of data through it before you will get output. It
therefore will not necessarily detect cuts in the first 15 frames or so
of a sequence sent to it. Neither will it generate any output for the
last 15 frames or so - they will never make it through the internal
signal processing.

Send a producerFinished() or shutdownMicroprocess() message to this
component\'s \"control\" inbox and it will immediately terminate. It
will also forward on the message out of its \"signal\" outbox.
:::

::: {.section}
### [Implementation details]{#implementation-details} {#670}

The algorithm used is based on a simple \"mean absolute difference\"
between pixels of one frame and the next; with some signal processing on
the resulting stream of frame-to-frame difference values, to detect a
spike possibly indicating a shot change.

The algorithm is courtesy of Jim Easterbrook of BBC Research. It is also
available in its own right as an independent open source library
[here.](http://sourceforge.net/projects/shot-change){.reference}

As signal processing is done on the confidence values internally to
emphasise spikes - which are likely to indicate a sudden increase in the
level of change from one frame to the next - a conseuqence is that this
component internally buffers inter-frame difference values for several
frames, resulting in a delay of about 15 frames through this component.
This is the reason why it is necessary to pair up video frames with a
frame number, otherwise you cannot guarantee being able to match up the
resulting detected cuts with the actual frame where they took place!

The change detection algorithm only looks at the Y (luminance) data in
the video frame.
:::
:::

::: {.section}
[UNCOMPRESSED FRAME FORMAT]{#uncompressed-frame-format} {#671}
-------------------------------------------------------

A frame is a dictionary data structure. It must, for this component, at
minimum contain a key \"yuv\" that returns a tuple containing (y\_data,
u\_data, v\_data).

Any other entries are ignored.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.html){.reference}.[DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.DetectShotChanges.html){.reference}
======================================================================================================================================================================================================================================================================================================================

::: {.section}
class DetectShotChanges([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DetectShotChanges}
---------------------------------------------------------------------------------------------------------

DetectShotChanges(\[threshold\]) -\> new DetectShotChanges component.

Send (framenumber, videoframe) tuples to the \"inbox\" inbox. Sends out
(framenumber, confidence) to its \"outbox\" outbox when a cut has
probably occurred in the video sequence.

Keyword arguments:

-   threshold \-- threshold for the confidence value, above which a cut
    is detected (default=0.9)

::: {.section}
### [Inboxes]{#symbol-DetectShotChanges.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-DetectShotChanges.Outboxes}
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
#### [\_\_init\_\_(self\[, threshold\])]{#symbol-DetectShotChanges.__init__}
:::

::: {.section}
#### [detectCut(self, framenum, ydata)]{#symbol-DetectShotChanges.detectCut}
:::

::: {.section}
#### [main(self)]{#symbol-DetectShotChanges.main}

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
