---
pagename: Docs/Axon/Axon.Axon
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Axon](/Docs/Axon/Axon.Axon.html){.reference}
--------------------------------------------------------------------------------------
:::
:::

::: {.section}
Axon base classes
=================

::: {.container}
-   **class
    [AxonObject](/Docs/Axon/Axon.Axon.AxonObject.html){.reference}**
-   **class [AxonType](/Docs/Axon/Axon.Axon.AxonType.html){.reference}**
:::

-   [Test documentation](#71){.reference}
:::

::: {.section}
What is defined here is a metaclass that is used as a base class for
some key classes in Axon.

It was originally created to allow super class calling in a slightly
nicer manner in terms of syntactic sugar easier to get right that still
has the good effects of \"super\" in a multiple inheritance scenario.
**Use of this particular feature has been deprecated** because of more
subtle issues in inheritance situations.

However this metaclass has been retained (and is still used) for
possible future uses.

-   AxonObject is the base class for
    [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}
    and
    [Axon.Linkage.linkage](/Docs/Axon/Axon.Linkage.linkage.html){.reference}

Test documentation {#71}
==================

Tests passed:

-   AxonObject - derives from object, but sets a metaclass of AxonType -
    to allow superclass method calling simply. ttbChecked
-   AxonType.\_\_init\_\_ - adds an extra \_\_super method to all
    objects created from classes with this metaclass simplifying
    superclass method calling. ttbChecked
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Axon](/Docs/Axon/Axon.Axon.html){.reference}.[AxonObject](/Docs/Axon/Axon.Axon.AxonObject.html){.reference}
=====================================================================================================================================================

::: {.section}
class AxonObject(object) {#symbol-AxonObject}
------------------------

::: {.section}
Base class for axon objects.

Uses AxonType as its metaclass.
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Axon](/Docs/Axon/Axon.Axon.html){.reference}.[AxonType](/Docs/Axon/Axon.Axon.AxonType.html){.reference}
=================================================================================================================================================

::: {.section}
class AxonType(type) {#symbol-AxonType}
--------------------

::: {.section}
Metaclass for Axon objects.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(cls, name, bases, dict)]{#symbol-AxonType.__init__}

Override creation of class to set a \'super\' attribute to what you get
when you call super().

**Note** that this \'super\' attribute is deprecated - there are some
subtle issues with it and it should therefore be avoided.
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
