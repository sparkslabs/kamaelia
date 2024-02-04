---
pagename: Docs/Axon/Axon.Linkage
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Linkage](/Docs/Axon/Axon.Linkage.html){.reference}
--------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Linkages
========

::: {.container}
-   **class
    [linkage](/Docs/Axon/Axon.Linkage.linkage.html){.reference}**
:::

-   [Test documentation](#34){.reference}
:::

::: {.section}
Components only have input & output boxes. For data to get from a
producer (eg a file reader) to a consumer (eg an encryption component)
then the output of one component, the source component, must be linked
to the input of another component, the sink component.

-   linkage objects are handles describing a linkage from one postbox to
    another
-   [Axon.Postoffice.postoffice](/Docs/Axon/Axon.Postoffice.postoffice.html){.reference}
    creates and destroys linkages

All components have a postoffice object, this performs the creation and
destruction of linkages. Ask it for a linkage between inboxes and
outboxes and a linkage object is returned as a handle describing the
linkage. When a message is sent to an outbox, it is immediately
delivered along linkage(s) to the destination inbox.

This is *not* the usual technique for software messaging. Normally you
create messages, addressed to something specific, and then the message
handler delivers them.

However the method of communication used here is the norm for *hardware*
systems, and generally results in very pluggable components - the aim of
this system, hence this design approach rather than the normal. This
method of communication is also the norm for one form of software system
- unix shell scripting - something that has shown itself time and again
to be used in ways the inventors of programs/components never
envisioned.

Test documentation {#34}
==================

Tests passed:

-   \_\_init\_\_ - Called with source & sink components forms a
    non-synchronous, non-passthrough linkage between the source
    component\'s outbox to the sink component\'s inbox
-   \_\_init\_\_ - Called with no arguments fails - raises TypeError -
    must supply source & sink components\...
-   \_\_init\_\_ - called with both source/sink in/outboxes in addition
    to min-args forms a linkage between the specified source/sink boxes.
-   \_\_init\_\_ - called with passthrough set to 0 results in a
    standard non-passthrough outbox to inbox linkage.
-   \_\_init\_\_ - called with passthrough set to 1 means the source and
    sink boxes are both inboxes. This means the linkage is
    passthrough-inbound (normally from the inbox of a wrapper component
    to the inbox of a worker/sub-component).
-   \_\_init\_\_ - called with passthrough set to 2 means the source and
    sink boxes are both outboxes. This means the linkage is
    passthrough-outbound (normally from the outbox of a
    worker/sub-component to the outbox of a wrapper component ). ttbw
-   \_\_str\_\_ - Returns a string that indicates the link source and
    sink components and boxes. Precise formatting is checked.
-   test\_sourcePair (\_\_main\_\_.linkage\_Test)
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Linkage](/Docs/Axon/Axon.Linkage.html){.reference}.[linkage](/Docs/Axon/Axon.Linkage.linkage.html){.reference}
========================================================================================================================================================

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
