---
pagename: Docs/Axon/Axon.STM.Store
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[Store](/Docs/Axon/Axon.STM.Store.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.STM.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Store(object) {#symbol-Store}
-------------------

::: {.section}
Store() -\> new Store object

A thread-safe versioning store for key-value pairs

You instantiate this as per the documentation for this module
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_can\_update(self, key, value)]{#symbol-Store.__can_update}

Returns true if a value can be safely updated. Potentially not
thread-safe
:::

::: {.section}
#### [\_\_do\_update(self, key, value)]{#symbol-Store.__do_update}

Update a key-value pair and increment the version. Not thread-safe
:::

::: {.section}
#### [\_\_get(self, key)]{#symbol-Store.__get}

Retreive a value. Returns a clone of the Value. Not thread-safe.
:::

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-Store.__init__}
:::

::: {.section}
#### [\_\_make(self, key)]{#symbol-Store.__make}

Create a new key-value pair. Not thread-safe
:::

::: {.section}
#### [dump(self)]{#symbol-Store.dump}
:::

::: {.section}
#### [set(self, key, value)]{#symbol-Store.set}

Tries to update a value in the store. If the store is already in use a
BusyRetry error is raised. If the value has been updated by another
thread a ConcurrentUpdate error is raised
:::

::: {.section}
#### [set\_values(self, D)]{#symbol-Store.set_values}

Tries to update a selection of values in the store. If the store is
already in use a BusyRetry error is raised. If one of the values has
been updated by another thread a ConcurrentUpdate error is raised.
:::

::: {.section}
#### [usevar(self, key\[, islocked\])]{#symbol-Store.usevar}

Tries to get an item from the store. Returns the requested Value object.
If the store is already in use a BusyRetry error is raised.
:::

::: {.section}
#### [using(self, \*keys)]{#symbol-Store.using}

Tries to get a selection of items from the store. Returns a Collection
dictionary containing the requested values. If the store is already in
use a BusyRetry error is raised.
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
