---
pagename: Components/pydoc/Kamaelia.Util.Detuple.SimpleDetupler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Detuple](/Components/pydoc/Kamaelia.Util.Detuple.html){.reference}.[SimpleDetupler](/Components/pydoc/Kamaelia.Util.Detuple.SimpleDetupler.html){.reference}
==============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Detuple.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SimpleDetupler([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleDetupler}
------------------------------------------------------------------------------------------------------

This class expects to recieve tuples (or more accurately indexable
objects) on its inboxes. It extracts the item tuple\[index\] from the
tuple (or indexable object) and passes this out its outbox.

This component does not terminate.

This component was originally created for use with the multicast
component. (It could however be used for extracting a single field from
a dictionary like object).

Example usage:

``` {.literal-block}
Pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    detuple(1), # Extract data, through away sender
    SRM_Receiver(),
    detuple(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
```

::: {.section}
### [Inboxes]{#symbol-SimpleDetupler.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleDetupler.Outboxes}
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
#### [\_\_init\_\_(self, index)]{#symbol-SimpleDetupler.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-SimpleDetupler.main}
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
