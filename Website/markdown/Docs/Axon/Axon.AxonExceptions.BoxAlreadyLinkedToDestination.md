---
pagename: Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.AxonExceptions.html){.reference}

------------------------------------------------------------------------

::: {.section}
class BoxAlreadyLinkedToDestination(AxonException) {#symbol-BoxAlreadyLinkedToDestination}
--------------------------------------------------

::: {.section}
The inbox/outbox already has a linkage going *from* it to a destination.

Arguments:

-   the box that is already linked
-   the box that it is linked to
-   the box you were trying to link it to

Possible causes:

-   Are you trying to make a linkage going from an inbox/outbox to more
    than one destination?
-   perhaps another component has already made a linkage from that
    inbox/outbox?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
