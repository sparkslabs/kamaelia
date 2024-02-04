---
pagename: Components/pydoc/Kamaelia.Util.Filter.Filter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Filter](/Components/pydoc/Kamaelia.Util.Filter.html){.reference}.[Filter](/Components/pydoc/Kamaelia.Util.Filter.Filter.html){.reference}
===========================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Filter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Filter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Filter}
----------------------------------------------------------------------------------------------

Filter(\[filter\]) -\> new Filter component.

Component that can modify and filter data passing through it. Plug your
own \'filter\' into it.

Keyword arguments:

-   filter \-- an object implementing a filter(data) method
    (default=NullFilter instance)

::: {.section}
### [Inboxes]{#symbol-Filter.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data to be filtered
:::

::: {.section}
### [Outboxes]{#symbol-Filter.Outboxes}

-   **outbox** : Filtered data
-   **signal** : Shutdown signalling
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, filter\])]{#symbol-Filter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-Filter.closeDownComponent}

Flush any data remaining in the filter before shutting down.
:::

::: {.section}
#### [mainBody(self)]{#symbol-Filter.mainBody}

Main loop body.
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

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
