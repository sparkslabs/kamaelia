---
pagename: Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Multiplex
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Core](/Components/pydoc/Kamaelia.Device.DVB.Core.html){.reference}.[DVB\_Multiplex](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Multiplex.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Core.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DVB\_Multiplex([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-DVB_Multiplex}
--------------------------------------------------------------------------------------------------------------------------------------

This is a DVB Multiplex Tuner.

This tunes the given DVB card to the given frequency. This then sets up
the dvr0 device node to recieve the data recieved on a number of PIDs.

A special case use of these is to tune to 2 specific PIDs - the audio
and video for a specific TV channel. If you pass just 2 PIDs then
you\'re tuning to a specific channel.

NOTE 1: This multiplex tuner deliberately does not know what frequency
the multiplex is on, and does not know what PIDs are inside that
multiplex. You are expected to find out this information independently.

NOTE 2: This means also that producing a mock for the next stages in
this system should be relatively simple - we run this code once and dump
to disk.

::: {.section}
### [Inboxes]{#symbol-DVB_Multiplex.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-DVB_Multiplex.Outboxes}
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
#### [\_\_init\_\_(self, freq, pids\[, feparams\]\[, card\])]{#symbol-DVB_Multiplex.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-DVB_Multiplex.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-DVB_Multiplex.shutdown}
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
