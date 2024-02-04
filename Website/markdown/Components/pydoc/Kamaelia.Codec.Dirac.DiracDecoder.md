---
pagename: Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Dirac](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}.[DiracDecoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder.html){.reference}
========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DiracDecoder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DiracDecoder}
----------------------------------------------------------------------------------------------------

DiracDecoder() -\> new Dirac decoder component

Creates a component that decodes Dirac video.

::: {.section}
### [Inboxes]{#symbol-DiracDecoder.Inboxes}

-   **control** : for shutdown signalling
-   **inbox** : Strings containing an encoded dirac video stream
:::

::: {.section}
### [Outboxes]{#symbol-DiracDecoder.Outboxes}

-   **outbox** : YUV decoded video frames
-   **signal** : for shutdown/completion signalling
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
#### [\_\_init\_\_(self)]{#symbol-DiracDecoder.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-DiracDecoder.main}

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
