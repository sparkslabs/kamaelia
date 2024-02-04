---
pagename: Docs/Axon/Axon.Box.nullsink
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[nullsink](/Docs/Axon/Axon.Box.nullsink.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Box.html){.reference}

------------------------------------------------------------------------

::: {.section}
class nullsink(object) {#symbol-nullsink}
----------------------

::: {.section}
nullsink() -\> new nullsink object

A dummy piece of storage for postboxes, that behaves a bit like a list.

Discards data given to it by calling append() and always reports that it
contains no items.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-nullsink.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [\_\_len\_\_(self)]{#symbol-nullsink.__len__}

Returns number of items in the list (always zero)
:::

::: {.section}
#### [\_\_repr\_\_(self)]{#symbol-nullsink.__repr__}
:::

::: {.section}
#### [append(self, data)]{#symbol-nullsink.append}

Append item to the list - though actually it just gets discarded.
:::

::: {.section}
#### [pop(self, index)]{#symbol-nullsink.pop}

Returns an item from the list (always raises IndexError
:::

::: {.section}
#### [setShowTransit(self, showtransit, tag)]{#symbol-nullsink.setShowTransit}

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
