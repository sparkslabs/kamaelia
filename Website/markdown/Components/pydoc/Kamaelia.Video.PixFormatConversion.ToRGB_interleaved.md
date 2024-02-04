---
pagename: Components/pydoc/Kamaelia.Video.PixFormatConversion.ToRGB_interleaved
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[PixFormatConversion](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}.[ToRGB\_interleaved](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToRGB_interleaved.html){.reference}
=============================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}

------------------------------------------------------------------------

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
