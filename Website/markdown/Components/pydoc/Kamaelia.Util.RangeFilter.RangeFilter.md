---
pagename: Components/pydoc/Kamaelia.Util.RangeFilter.RangeFilter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.html){.reference}.[RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.RangeFilter.html){.reference}
====================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.RangeFilter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class RangeFilter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RangeFilter}
---------------------------------------------------------------------------------------------------

RangeFilter(ranges) -\> new RangeFilter component.

Filters out items of the form (value, \...) not within at least one of a
specified value set of range. Items within range are passed through.

Keyword arguments:

``` {.literal-block}
- ranges  -- list of (low,high) pairs representing ranges of value. Ranges are inclusive.
```

::: {.section}
### [Inboxes]{#symbol-RangeFilter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RangeFilter.Outboxes}

-   **outbox** : items in range
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
#### [\_\_init\_\_(self, ranges)]{#symbol-RangeFilter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [canStop(self)]{#symbol-RangeFilter.canStop}

Checks for any shutdown messages arriving at the \"control\" inbox, and
returns true if the component should terminate when it has finished
processing any pending data.
:::

::: {.section}
#### [handleControl(self)]{#symbol-RangeFilter.handleControl}

Collects any new shutdown messages arriving at the \"control\" inbox,
and ensures self.shutdownMsg contains the highest priority one
encountered so far.
:::

::: {.section}
#### [inRange(self, index)]{#symbol-RangeFilter.inRange}

Returns one of the ranges that the specified index falls within,
otherwise returns None.
:::

::: {.section}
#### [main(self)]{#symbol-RangeFilter.main}

Main loop
:::

::: {.section}
#### [mustStop(self)]{#symbol-RangeFilter.mustStop}

Checks for any shutdown messages arriving at the \"control\" inbox, and
returns true if the component should terminate immediately.
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-RangeFilter.waitSend}

Generator.

Sends data out of the \"outbox\" outbox. If the destination is full
(noSpaceInBox exception) then it waits until there is space. It keeps
retrying until it succeeds.

If the component is ordered to immediately terminate then \"STOP\" is
raised as an exception.
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
