---
pagename: Components/pydoc/Kamaelia.Video.PixFormatConversion
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[PixFormatConversion](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}
===============================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ToRGB\_interleaved](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToRGB_interleaved.html){.reference}**
-   **component
    [ToYUV420\_planar](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToYUV420_planar.html){.reference}**
:::

-   [Converting the pixel format of video frames](#672){.reference}
    -   [Example Usage](#673){.reference}
    -   [Which component for which conversion?](#674){.reference}
    -   [More details](#675){.reference}
:::

::: {.section}
Converting the pixel format of video frames {#672}
===========================================

These components convert the pixel format of video frames, for example,
from interleaved RGB to planar YUV 420.

::: {.section}
[Example Usage]{#example-usage} {#673}
-------------------------------

Decoding a Dirac encoded video file, then converting it to RGB for
display on a pygame display surface:

``` {.literal-block}
Pipeline( RateControlledFileReader("video.drc",readmode="bytes", rate=100000),
          DiracDecoder(),
          ToRGB_interleaved(),
          VideoSurface(),
        ).run()
```
:::

::: {.section}
[Which component for which conversion?]{#which-component-for-which-conversion} {#674}
------------------------------------------------------------------------------

The components here are currently capable of the following pixel format
conversions:

  -------------------------------------------------------------------------
  From                   To                     Which component?
  ---------------------- ---------------------- ---------------------------
  \"RGB\_interleaved\"   \"RGB\_interleaved\"   ToRGB\_interleaved

  \"YUV420\_planar\"     \"RGB\_interleaved\"   ToRGB\_interleaved

  \"YUV422\_planar\"     \"RGB\_interleaved\"   ToRGB\_interleaved

  \"RGB\_interleaved\"   \"YUV420\_planar\"     ToYUV420\_planar

  \"YUV420\_planar\"     \"YUV420\_planar\"     ToYUV420\_planar
  -------------------------------------------------------------------------
:::

::: {.section}
[More details]{#more-details} {#675}
-----------------------------

Send video frames to the \"inbox\" inbox of these components. They will
be converted to the destination pixel format and sent out of the
\"outbox\" outbox. Video frames are dictionaries, they must have the
following keys:

> -   \"rgb\" or \"yuv\" \-- containing the pixel data
> -   \"pixformat\" \-- the pixel format
> -   \"size\" \-- (width,height) in pixels

Any other fields will be transparently passed through, unmodified.

These components support sending data out of its outbox to a size
limited inbox. If the size limited inbox is full, these components will
pause until able to send out the data. Data will not be consumed from
the inbox if these components are waiting to send to the outbox.

If a producerFinished message is received on the \"control\" inbox,
these components will complete converting and frames pending in its
inbox, and finish sending any resulting data to its outbox. They will
then send the producerFinished message on out of its \"signal\" outbox
and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
these components will immediately send it on out of its \"signal\"
outbox and immediately terminate. It will not complete processing, or
sending on any pending data.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[PixFormatConversion](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}.[ToRGB\_interleaved](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToRGB_interleaved.html){.reference}
=============================================================================================================================================================================================================================================================================================================================

::: {.section}
class ToRGB\_interleaved([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ToRGB_interleaved}
----------------------------------------------------------------------------------------------------------

\" ToRGB\_interleaved() -\> new ToRGB\_interleaved component.

Converts video frames sent to its \"inbox\" inbox, to
\"RGB\_interleaved\" pixel format and sends them out of its \"outbox\"

Supports conversion from:

-   YUV420\_planar
-   YUV422\_planar
-   RGB\_interleaved (passthrough)

::: {.section}
### [Inboxes]{#symbol-ToRGB_interleaved.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Video frame
:::

::: {.section}
### [Outboxes]{#symbol-ToRGB_interleaved.Outboxes}

-   **outbox** : RGB\_interleaved pixel format video frame
-   **signal** : Shutdown signalling
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
#### [canStop(self)]{#symbol-ToRGB_interleaved.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-ToRGB_interleaved.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-ToRGB_interleaved.main}

Main loop.
:::

::: {.section}
#### [mustStop(self)]{#symbol-ToRGB_interleaved.mustStop}
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-ToRGB_interleaved.waitSend}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[PixFormatConversion](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}.[ToYUV420\_planar](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToYUV420_planar.html){.reference}
=========================================================================================================================================================================================================================================================================================================================

::: {.section}
class ToYUV420\_planar([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ToYUV420_planar}
--------------------------------------------------------------------------------------------------------

\" ToYUV420\_planar() -\> new ToYUV420\_planar component.

Converts video frames sent to its \"inbox\" inbox, to
\"ToYUV420\_planar\" pixel format and sends them out of its \"outbox\"

Supports conversion from:

-   RGB\_interleaved
-   YUV420\_planar (passthrough)

::: {.section}
### [Inboxes]{#symbol-ToYUV420_planar.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Video frame
:::

::: {.section}
### [Outboxes]{#symbol-ToYUV420_planar.Outboxes}

-   **outbox** : YUV420\_planar pixel format video frame
-   **signal** : Shutdown signalling
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
#### [canStop(self)]{#symbol-ToYUV420_planar.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-ToYUV420_planar.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-ToYUV420_planar.main}

Main loop.
:::

::: {.section}
#### [mustStop(self)]{#symbol-ToYUV420_planar.mustStop}
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-ToYUV420_planar.waitSend}
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
