---
pagename: Components/pydoc/Kamaelia.Codec.RawYUVFramer.RawYUVFramer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.html){.reference}.[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.RawYUVFramer.html){.reference}
=============================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.html){.reference}

------------------------------------------------------------------------

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
