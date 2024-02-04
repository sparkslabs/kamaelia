---
pagename: Docs/Axon/Axon.Box.realsink
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[realsink](/Docs/Axon/Axon.Box.realsink.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Box.html){.reference}

------------------------------------------------------------------------

::: {.section}
class realsink(list) {#symbol-realsink}
--------------------

::: {.section}
realsink(notify\[,size\]) -\> new realsink object.

A working piece of storage for postboxes, that behaves a bit like a
list.

Stores data given to it by calling append(), up to a limit after which
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
exceptions are raised.

Calls the \'notify\' callback when append() is called. Calls any
callbacks in the self.wakeOnPop list when pop() is called.

Keyword arguments:

-   notify \-- notify() is called whenever append() is called
-   size \-- None, or the maximum number of items this storage can hold
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, notify\[, size\])]{#symbol-realsink.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [append(self, data)]{#symbol-realsink.append}

Appends item to the list, or raises
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
exception if the number of items already meets the size limit.

Calls self.notify() callback
:::

::: {.section}
#### [pop(self, index)]{#symbol-realsink.pop}

Returns an item from the list, or raises IndexError if there are none.

Calls all callbacks listed in self.wakeOnPop
:::

::: {.section}
#### [setShowTransit(self, showtransit, tag)]{#symbol-realsink.setShowTransit}

Set showTransit to True to cause debugging output whenever a message is
delivered to this storage. The tag can be anything you want to identify
this occurrence.
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
