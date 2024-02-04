---
pagename: Components/pydoc/Kamaelia.Codec.YUV4MPEG.YUV4MPEGToFrame
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[YUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}.[YUV4MPEGToFrame](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.YUV4MPEGToFrame.html){.reference}
=======================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}

------------------------------------------------------------------------

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
