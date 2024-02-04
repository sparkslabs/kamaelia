---
pagename: Components/pydoc/Kamaelia.Codec.WAV.WAVWriter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[WAV](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}.[WAVWriter](/Components/pydoc/Kamaelia.Codec.WAV.WAVWriter.html){.reference}
============================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}

------------------------------------------------------------------------

::: {.section}
class WAVWriter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-WAVWriter}
-------------------------------------------------------------------------------------------------

WAVWriter(channels, sample\_format, sample\_rate) -\> new WAVWriter
component.

Send raw audio data as binary strings to the \"inbox\" inbox and WAV
format audio data will be sent out of the \"outbox\" outbox as binary
strings.

::: {.section}
### [Inboxes]{#symbol-WAVWriter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-WAVWriter.Outboxes}
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
#### [\_\_init\_\_(self, channels, sample\_format, sample\_rate)]{#symbol-WAVWriter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [canStop(self)]{#symbol-WAVWriter.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-WAVWriter.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-WAVWriter.main}
:::

::: {.section}
#### [mustStop(self)]{#symbol-WAVWriter.mustStop}
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-WAVWriter.waitSend}
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
