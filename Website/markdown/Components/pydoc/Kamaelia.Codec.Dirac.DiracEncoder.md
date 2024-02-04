---
pagename: Components/pydoc/Kamaelia.Codec.Dirac.DiracEncoder
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Dirac](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}.[DiracEncoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracEncoder.html){.reference}
========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DiracEncoder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DiracEncoder}
----------------------------------------------------------------------------------------------------

DiracEncoder(\[preset\]\[,verbose\]\[,encParams\]\[,seqParams\]\[,allParams\])
-\> new Dirac encoder component

Creates a component to encode video using the Dirac codec. Configuration
based on optional preset, optionally overriden by individual encoder and
sequence parameters. All three \'params\' arguments are munged together,
so do what you like :)

Keyword arguments:

-   preset \-- \"CIF\" or \"SD576\" or \"HD720\" or \"HD1080\" (presets
    for common video formats)
-   verbose \-- NOT YET IMPLEMENTED (IGNORED)
-   encParams \-- dict of encoder setup parameters only
-   seqParams \-- dict of video sequence parameters only
-   allParams \-- dict of encoder setup parameters, sequence parameters,
    and source parameters, all munged together

::: {.section}
### [Inboxes]{#symbol-DiracEncoder.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-DiracEncoder.Outboxes}
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
#### [\_\_init\_\_(self\[, preset\]\[, verbose\]\[, encParams\]\[, seqParams\]\[, allParams\])]{#symbol-DiracEncoder.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-DiracEncoder.main}

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
