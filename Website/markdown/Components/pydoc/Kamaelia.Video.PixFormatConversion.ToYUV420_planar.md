---
pagename: Components/pydoc/Kamaelia.Video.PixFormatConversion.ToYUV420_planar
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[PixFormatConversion](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}.[ToYUV420\_planar](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToYUV420_planar.html){.reference}
=========================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}

------------------------------------------------------------------------

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
