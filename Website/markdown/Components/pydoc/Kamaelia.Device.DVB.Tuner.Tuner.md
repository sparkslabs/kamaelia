---
pagename: Components/pydoc/Kamaelia.Device.DVB.Tuner.Tuner
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.html){.reference}.[Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.Tuner.html){.reference}
====================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Tuner.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Tuner([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-Tuner}
-----------------------------------------------------------------------------------------------------------------------------

Tuner(freq\[,feparams\]\[,card\]) -\> new Tuner component.

Tunes the DVB-T card to the given frequency with the given parameters.
Send (ADD, \[PID list\]) or (REMOVE, \[PID list\]) messages to its
\"inbox\" inbox to cuase it to output MPEG transport stream packets
(with the specified PIDs) from its \"outbox\" outbox.

Keyword arguments:

-   freq \-- Frequency to tune to in MHz
-   feparams \-- Dictionary of parameters for the tuner front end
    (default={})
-   card \-- Which DVB device to use (default=0)

::: {.section}
### [Inboxes]{#symbol-Tuner.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Tuner.Outboxes}
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
#### [\_\_init\_\_(self, freq\[, feparams\]\[, card\])]{#symbol-Tuner.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addPID(self, pid)]{#symbol-Tuner.addPID}

Adds the given PID to the transport stream that will be available in
\"/dev/dvb/adapter0/dvr0\"
:::

::: {.section}
#### [handleCommand(self, cmd, demuxers)]{#symbol-Tuner.handleCommand}
:::

::: {.section}
#### [main(self)]{#symbol-Tuner.main}
:::

::: {.section}
#### [notLocked(self)]{#symbol-Tuner.notLocked}

Returns True if the frontend is not yet locked. Returns False if it is
locked.
:::

::: {.section}
#### [shutdown(self)]{#symbol-Tuner.shutdown}
:::

::: {.section}
#### [tune\_DVB(self, frequency\[, feparams\])]{#symbol-Tuner.tune_DVB}
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
