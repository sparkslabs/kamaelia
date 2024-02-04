---
pagename: Docs/Axon/Axon.AxonExceptions.NamespaceClash
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[NamespaceClash](/Docs/Axon/Axon.AxonExceptions.NamespaceClash.html){.reference}
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.AxonExceptions.html){.reference}

------------------------------------------------------------------------

::: {.section}
class NamespaceClash(AxonException) {#symbol-NamespaceClash}
-----------------------------------

::: {.section}
Clash of names.

Possible causes:

-   two or more requests made to coordinating assistant tracker to track
    values under a given name (2nd request will clash with first)?
-   should have used updateValue() method to update a value being
    tracked by the coordinating assistant tracker?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
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
