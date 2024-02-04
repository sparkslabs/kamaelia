---
pagename: Components/pydoc/Kamaelia.Util.Clock
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Clock](/Components/pydoc/Kamaelia.Util.Clock.html){.reference}
================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [CheapAndCheerfulClock](/Components/pydoc/Kamaelia.Util.Clock.CheapAndCheerfulClock.html){.reference}**
:::

-   [Cheap And Cheerful Clock](#155){.reference}
:::

::: {.section}
Cheap And Cheerful Clock {#155}
========================

Outputs the message True repeatedly. The interval between messages is
the parameter \"interval\" specified at the creation of the component.

This component is useful because it allows another component to sleep,
not using any CPU time, but waking periodically (components are unpaused
when they are sent a message).

Why is it \"cheap and cheerful\"?

\...Because it uses a thread just for itself. All clocks could share a
single thread if some services kung-fu was pulled. Opening lots of
threads is a bad thing - they have much greater overhead than normal
generator-based components. However, the one-thread-per-clock approach
used here is many times shorter and simpler than one using services.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Clock](/Components/pydoc/Kamaelia.Util.Clock.html){.reference}.[CheapAndCheerfulClock](/Components/pydoc/Kamaelia.Util.Clock.CheapAndCheerfulClock.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class CheapAndCheerfulClock([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-CheapAndCheerfulClock}
---------------------------------------------------------------------------------------------------------------------------------------------

Outputs the message True every interval seconds

::: {.section}
### [Inboxes]{#symbol-CheapAndCheerfulClock.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-CheapAndCheerfulClock.Outboxes}
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
#### [\_\_init\_\_(self, interval)]{#symbol-CheapAndCheerfulClock.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-CheapAndCheerfulClock.main}
:::
:::

::: {.section}
:::
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
