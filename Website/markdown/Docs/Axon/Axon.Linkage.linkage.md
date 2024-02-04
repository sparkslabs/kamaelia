---
pagename: Docs/Axon/Axon.Linkage.linkage
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Linkage](/Docs/Axon/Axon.Linkage.html){.reference}.[linkage](/Docs/Axon/Axon.Linkage.linkage.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Linkage.html){.reference}

------------------------------------------------------------------------

::: {.section}
class linkage([Axon.Axon.AxonObject](/Docs/Axon/Axon.Axon.AxonObject.html){.reference}) {#symbol-linkage}
---------------------------------------------------------------------------------------

::: {.section}
linkage(source, sink\[, passthrough\]) -\> new linkage object

An object describing a link from a source component\'s inbox/outbox to a
sink component\'s inbox/outbox.

Keyword arguments: - source \-- source component - sink \-- sink
component - sourcebox \-- source component\'s source box name
(default=\"outbox\") - sinkbox \-- sink component\'s sink box name
(default=\"inbox\") - passthrough \-- 0=link is from inbox to outbox;
1=from inbox to inbox; 2=from outbox to outbox (default=0)
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, source, sink\[, sourcebox\]\[, sinkbox\]\[, passthrough\]\[, pipewidth\]\[, synchronous\])]{#symbol-linkage.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [\_\_str\_\_(self)]{#symbol-linkage.__str__}
:::

::: {.section}
#### [getSinkbox(self)]{#symbol-linkage.getSinkbox}

Returns the box object that this linkage goes to.
:::

::: {.section}
#### [getSourcebox(self)]{#symbol-linkage.getSourcebox}

Returns the box object that this linkage goes from.
:::

::: {.section}
#### [setShowTransit(self, showtransit, tag)]{#symbol-linkage.setShowTransit}

Set showTransit to True to cause debugging output whenever a message is
delivered along this linkage. The tag can be anything you want to
identify this occurrence.
:::

::: {.section}
#### [setSynchronous(self\[, pipewidth\])]{#symbol-linkage.setSynchronous}

Legacy method for setting the size limit on a linkage. Instead it sets
the size limit for the destination inbox. A pipewidth of None specifies
that there should be no limit.

This method is likely to be deprecated soon.
:::

::: {.section}
#### [sinkPair(self)]{#symbol-linkage.sinkPair}

Returns (component,boxname) tuple describing where this linkage goes to
:::

::: {.section}
#### [sourcePair(self)]{#symbol-linkage.sourcePair}

Returns (component,boxname) tuple describing where this linkage goes
from
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
