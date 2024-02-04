---
pagename: Docs/Axon/Axon.AxonExceptions.AccessToUndeclaredTrackedVariable
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[AccessToUndeclaredTrackedVariable](/Docs/Axon/Axon.AxonExceptions.AccessToUndeclaredTrackedVariable.html){.reference}
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.AxonExceptions.html){.reference}

------------------------------------------------------------------------

::: {.section}
class AccessToUndeclaredTrackedVariable(AxonException) {#symbol-AccessToUndeclaredTrackedVariable}
------------------------------------------------------

::: {.section}
Attempt to access a value being tracked by the coordinating assistant
tracker that isn\'t actually being tracked yet!

Arguments:

-   the name of the value that couldn\'t be accessed
-   the value that it was to be updated with (optional)

Possible causes:

-   Attempt to update or retrieve a value with a misspelt name?
-   Attempt to update or retrieve a value before it starts being
    tracked?
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
