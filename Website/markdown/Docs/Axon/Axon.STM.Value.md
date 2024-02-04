---
pagename: Docs/Axon/Axon.STM.Value
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[STM](/Docs/Axon/Axon.STM.html){.reference}.[Value](/Docs/Axon/Axon.STM.Value.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.STM.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Value(object) {#symbol-Value}
-------------------

::: {.section}
Value(version, value, store, key) -\> new Value object

A simple versioned key-value pair which belongs to a thread-safe store

Arguments:

-   version \-- the initial version of the value
-   value \-- the object\'s initial value
-   store \-- a Store object to hold the value and it\'s history
-   key \-- a key to refer to the value

Note: You do not instantiate these - the Store does that
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, version, value, store, key)]{#symbol-Value.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_\_repr\_\_(self)]{#symbol-Value.__repr__}
:::

::: {.section}
#### [clone(self)]{#symbol-Value.clone}

Returns a clone of the value
:::

::: {.section}
#### [commit(self)]{#symbol-Value.commit}

Commit a new version of the value to the store
:::

::: {.section}
#### [set(self, value)]{#symbol-Value.set}

Set the value without storing
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
