---
pagename: Components/pydoc/Kamaelia.Video.DetectShotChanges.DetectShotChanges
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Video](/Components/pydoc/Kamaelia.Video.html){.reference}.[DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.html){.reference}.[DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.DetectShotChanges.html){.reference}
======================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Video.DetectShotChanges.html){.reference}

------------------------------------------------------------------------

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
