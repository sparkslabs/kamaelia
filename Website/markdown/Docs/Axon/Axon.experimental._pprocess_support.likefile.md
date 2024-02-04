---
pagename: Docs/Axon/Axon.experimental._pprocess_support.likefile
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[likefile](/Docs/Axon/Axon.experimental._pprocess_support.likefile.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}

------------------------------------------------------------------------

::: {.section}
class likefile(object) {#symbol-likefile}
----------------------

::: {.section}
An interface to the message queues from a wrapped component, which is
activated on a backgrounded scheduler.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_del\_\_(self)]{#symbol-likefile.__del__}
:::

::: {.section}
#### [\_\_init\_\_(self, child\[, extraInboxes\]\[, extraOutboxes\]\[, wrapDefault\])]{#symbol-likefile.__init__}
:::

::: {.section}
#### [anyReady(self)]{#symbol-likefile.anyReady}
:::

::: {.section}
#### [empty(self\[, boxname\])]{#symbol-likefile.empty}

Return True if there is no data pending collection on boxname, False
otherwise.
:::

::: {.section}
#### [get(self\[, boxname\]\[, blocking\]\[, timeout\])]{#symbol-likefile.get}

Performs a blocking read on the queue corresponding to the named outbox
on the wrapped component. raises AttributeError if the likefile is not
alive. Optional parameters blocking and timeout function the same way as
in Queue objects, since that is what\'s used under the surface.
:::

::: {.section}
#### [get\_nowait(self\[, boxname\])]{#symbol-likefile.get_nowait}

Equivalent to get(boxname, False)
:::

::: {.section}
#### [put(self, msg\[, boxname\])]{#symbol-likefile.put}

Places an object on a queue which will be directed to a named inbox on
the wrapped component.
:::

::: {.section}
#### [qsize(self\[, boxname\])]{#symbol-likefile.qsize}

Returns the approximate number of pending data items awaiting collection
from boxname. Will never be smaller than the actual amount.
:::

::: {.section}
#### [shutdown(self)]{#symbol-likefile.shutdown}

Sends terminatory signals to the wrapped component, and shut down the
componentWrapper. will warn if the shutdown took too long to confirm in
action.
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
