---
pagename: Components/pydoc/Kamaelia.Codec.RawYUVFramer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.html){.reference}
=================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.RawYUVFramer.html){.reference}**
:::

-   [Raw YUV video data framer](#88){.reference}
    -   [Example Usage](#89){.reference}
    -   [More Detail](#90){.reference}
:::

::: {.section}
Raw YUV video data framer {#88}
=========================

This component takes a raw stream of YUV video data and breaks it into
invidual frames. It sends them out one at a time, tagged with relevant
data such as the frame size.

Many components that expect uncompressed video require it to be
structured into frames in this way, rather than as a raw stream of
continuous data. This component fulfills that requirement.

::: {.section}
[Example Usage]{#example-usage} {#89}
-------------------------------

Reading and encoding raw video:

``` {.literal-block}
imagesize = (352, 288)        # "CIF" size video

Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
         RawYUVFramer(imagesize),
         DiracEncoder(preset="CIF"),
        ).activate()
```
:::

::: {.section}
[More Detail]{#more-detail} {#90}
---------------------------

Receives raw yuv video data, as strings on its \"inbox\" inbox.

Sends out individual frames packaged in a dictionary:

``` {.literal-block}
{
  "yuv" : (y_data, u_data, v_data),  # a tuple of strings
  "size" : (width, height),          # in pixels
  "pixformat" : "YUV420_planar",     # raw video data format
}
```

The component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its \"control\" inbox. The message is passed
on out of the \"signal\" outbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.html){.reference}.[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.RawYUVFramer.html){.reference}
=============================================================================================================================================================================================================================================================================================

::: {.section}
class RawYUVFramer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RawYUVFramer}
----------------------------------------------------------------------------------------------------

RawYUVFramer(size,pixformat) -\> raw yuv video data framing component

Creates a component that frames a raw stream of YUV video data into
frames.

Keyword arguments:

-   size \-- (width,height) size of a video frame in pixels
-   pixformat \-- raw video data format (default=\"YUV420\_Planar\")

::: {.section}
### [Inboxes]{#symbol-RawYUVFramer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RawYUVFramer.Outboxes}
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
#### [\_\_init\_\_(self, size\[, pixformat\])]{#symbol-RawYUVFramer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [flushFrame(self)]{#symbol-RawYUVFramer.flushFrame}

Send out a frame, flushing buffers
:::

::: {.section}
#### [main(self)]{#symbol-RawYUVFramer.main}

Main loop
:::

::: {.section}
#### [packAndSend(self, raw)]{#symbol-RawYUVFramer.packAndSend}

packAndSend(raw) -\> None

Pack incoming raw data into y,u,v planes, and triggers a flush when all
planes are full.
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
