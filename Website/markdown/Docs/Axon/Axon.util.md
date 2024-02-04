---
pagename: Docs/Axon/Axon.util
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}
--------------------------------------------------------------------------------------
:::
:::

::: {.section}
General utility functions & common includes
===========================================

::: {.container}
-   **class [Finality](/Docs/Axon/Axon.util.Finality.html){.reference}**
-   **[axonRaise](/Docs/Axon/Axon.util.axonRaise.html){.reference}**(someException,
    \*args)
-   **[listSubset](/Docs/Axon/Axon.util.listSubset.html){.reference}**(requiredList,
    suppliedList)
-   **[logError](/Docs/Axon/Axon.util.logError.html){.reference}**(someException,
    \*args)
-   **[removeAll](/Docs/Axon/Axon.util.removeAll.html){.reference}**(xs, y)
-   **[safeList](/Docs/Axon/Axon.util.safeList.html){.reference}**(\[arg\])
-   **[testInterface](/Docs/Axon/Axon.util.testInterface.html){.reference}**(theComponent,
    interface)
:::

-   [Test documentation](#58){.reference}
:::

::: {.section}
Test documentation {#58}
==================

Tests passed:

-   Finality - dummy class deriving from Exception - used for
    implementing try\...finally in a generator.
-   axonRaise - behaviour depends on the value of production. If true it
    will simply return False. Otherwise it will throw an
-   listSubset - returns true if the first list argument is a subset of
    the second list argument.
-   logError - At the moment this function does nothing but can be
    rewritten to log ignored exception data. Equally the test does
    nothing.
-   production - is a module value that turns off some exception to make
    the system tolerant of failure when running in production.
-   removeAll - (xs:list,y) - removes all occurances of y from the list
    xs.
-   safeList - always returns a list even if the arg for constructing
    the list would normally cause a typeerror.
-   safeList - Like list it returns an empty list when called without an
    argument.
-   safeList - returns an empty list if the argument would cause a
    TypeError if passed to list(). That is anything without an iterator
    method.
-   In production mode failed tests will return false. Otherwise they
    will throw an exception that is likely to stop the system.
-   testInterface - returns true for a \_minimal match\_ on the
    interface of the component.
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[Finality](/Docs/Axon/Axon.util.Finality.html){.reference}
=================================================================================================================================================

::: {.section}
class Finality(Exception) {#symbol-Finality}
-------------------------

::: {.section}
Used for implementing try\...finally\... inside a generator.
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[axonRaise](/Docs/Axon/Axon.util.axonRaise.html){.reference}
===================================================================================================================================================

::: {.section}
[axonRaise(someException, \*args)]{#symbol-axonRaise}
-----------------------------------------------------

Raises the supplied exception with the supplied arguments *if*
Axon.util.production is set to True.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[listSubset](/Docs/Axon/Axon.util.listSubset.html){.reference}
=====================================================================================================================================================

::: {.section}
[listSubset(requiredList, suppliedList)]{#symbol-listSubset}
------------------------------------------------------------

Returns true if the requiredList is a subset of the suppliedList.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[logError](/Docs/Axon/Axon.util.logError.html){.reference}
=================================================================================================================================================

::: {.section}
[logError(someException, \*args)]{#symbol-logError}
---------------------------------------------------

Currently does nothing but can be rewritten to log ignored errors if the
production value is true.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[removeAll](/Docs/Axon/Axon.util.removeAll.html){.reference}
===================================================================================================================================================

::: {.section}
[removeAll(xs, y)]{#symbol-removeAll}
-------------------------------------

Very simplistic method of removing all occurances of y in list xs.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[safeList](/Docs/Axon/Axon.util.safeList.html){.reference}
=================================================================================================================================================

::: {.section}
[safeList(\[arg\])]{#symbol-safeList}
-------------------------------------

Returns the list version of arg, otherwise returns an empty list.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[util](/Docs/Axon/Axon.util.html){.reference}.[testInterface](/Docs/Axon/Axon.util.testInterface.html){.reference}
===========================================================================================================================================================

::: {.section}
[testInterface(theComponent, interface)]{#symbol-testInterface}
---------------------------------------------------------------

Look for a minimal match interface for the component. The interface
should be a tuple of lists, i.e. (\[inboxes\],\[outboxes\]).
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
