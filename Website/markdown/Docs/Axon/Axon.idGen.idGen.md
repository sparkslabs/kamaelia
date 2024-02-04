---
pagename: Docs/Axon/Axon.idGen.idGen
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[idGen](/Docs/Axon/Axon.idGen.html){.reference}.[idGen](/Docs/Axon/Axon.idGen.idGen.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.idGen.html){.reference}

------------------------------------------------------------------------

::: {.section}
class idGen(object) {#symbol-idGen}
-------------------

::: {.section}
Unique ID creator.

Use numId(), strId(), and tupleId() methods to obtain unique IDs.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [idToString(self, thing, aNumId)]{#symbol-idGen.idToString}

**INTERNAL**

Combines the \'str()\' of the object\'s class with the id to form a
string id
:::

::: {.section}
#### [next(self)]{#symbol-idGen.next}

**INTERNAL**

Returns the next unique id, incrementing the private class variable
:::

::: {.section}
#### [nextId(self)]{#symbol-idGen.nextId}

**INTERNAL**

Returns the next unique id, incrementing the private class variable
:::

::: {.section}
#### [numId(self)]{#symbol-idGen.numId}

Allocates & returns the next available id
:::

::: {.section}
#### [strId(self, thing)]{#symbol-idGen.strId}

Allocates & returns the next available id combined with the object\'s
class name, in string form
:::

::: {.section}
#### [tupleId(self, thing)]{#symbol-idGen.tupleId}

Allocates the next available id and returns it both as a tuple (num,str)
containing both the numeric version and a string version where it is
combined with the object\'s class name.
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
