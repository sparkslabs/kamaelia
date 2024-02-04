---
pagename: Components/pydoc/Kamaelia.Codec.YUV4MPEG.FrameToYUV4MPEG
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[YUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}.[FrameToYUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.FrameToYUV4MPEG.html){.reference}
=======================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}

------------------------------------------------------------------------

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
