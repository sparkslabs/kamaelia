---
pagename: Docs/Axon/Axon.idGen
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[idGen](/Docs/Axon/Axon.idGen.html){.reference}
----------------------------------------------------------------------------------------
:::
:::

::: {.section}
Unique ID generation
====================

::: {.container}
-   **class [idGen](/Docs/Axon/Axon.idGen.idGen.html){.reference}**
:::

-   [Generating a new unique ID](#70){.reference}
:::

::: {.section}
The methods of the idGen class are used to generate unique IDs in
various forms (numbers, strings, etc) which are used to give
microprocesses and other Axon objects a unique identifier and name.

-   Every
    [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}
    gets a unique ID
-   [Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}
    uses unique IDs to identify threads

::: {.section}
[Generating a new unique ID]{#generating-a-new-unique-id} {#70}
---------------------------------------------------------

Do not use the idGen class defined in this module directly. Instead, use
any of these module methods to obtain a unique ID:

-   **Axon.idGen.newId(thing)** - returns a unique identifier as a
    string based on the class name of the object provided
-   **Axon.idGen.strId(thing)** - returns a unique identifier as a
    string based on the class name of the object provided
-   **Axon.idGen.numId()** - returns a unique identifier as a number
-   **Axon.idGen.tupleId(thing)** - returns both the numeric and string
    versions of a new unique id as a tuple (where the string version is
    based on the class name of the object provided)

Calling tupleId(thing) is *not* equivalent to calling numId() then
strId(thing) because doing that would return two different id values!

Examples:

``` {.literal-block}
>>> x=Component.component()
>>> idGen.newId(x)
'Component.component_4'
>>> idGen.strId(x)
'Component.component_5'
>>> idGen.numId()
6
>>> idGen.tupleId(x)
(7, 'Component.component_7')
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[idGen](/Docs/Axon/Axon.idGen.html){.reference}.[idGen](/Docs/Axon/Axon.idGen.idGen.html){.reference}
==============================================================================================================================================

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
