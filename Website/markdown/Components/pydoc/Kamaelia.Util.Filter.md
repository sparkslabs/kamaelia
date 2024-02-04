---
pagename: Components/pydoc/Kamaelia.Util.Filter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Filter](/Components/pydoc/Kamaelia.Util.Filter.html){.reference}
==================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Filter](/Components/pydoc/Kamaelia.Util.Filter.Filter.html){.reference}**
:::

-   [Simple framework for filtering data](#214){.reference}
    -   [Example Usage](#215){.reference}
    -   [How does it work?](#216){.reference}
:::

::: {.section}
Simple framework for filtering data {#214}
===================================

A framework for filtering a stream of data. Write an object providing a
filter(\...) method and plug it into a Filter component.

::: {.section}
[Example Usage]{#example-usage} {#215}
-------------------------------

Filters any non-strings from a stream of data:

``` {.literal-block}
class StringFilter(object):
    def filter(self, input):
        if type(input) == type(""):
            return input
        else:
            return None            # indicates nothing to be output

myfilter = Filter(filter = StringFilter).activate()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#216}
--------------------------------------

Initialize a Filter component, providing an object with a filter(\...)
method.

The method should take a single argument - the data to be filtered. It
should return the result of the filtering/processing. If that result is
None then the component outputs nothing, otherwise it outputs whatever
the value is that was returned.

Data received on the component\'s \"inbox\" inbox is passed to the
filter(\...) method of the object you provided. The result is output on
the \"outbox\" outbox.

If a producerFinished message is received on the \"control\" inbox then
it is sent on out of the \"signal\" outbox. The component will then
terminate.

However, before terminating it will repeatedly call your object\'s
filter(\...) method, passing it an empty string (\"\") until the result
returned is None. If not None, then whatever value the filter(\...)
method returned is output. This is to give your object a chance to flush
any data it may have been buffering.

Irrespective of whether your filtering object buffers any data from one
call to the next, you must ensure that (eventually) calling it with an
empty string (\"\") will result in None being returned.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Filter](/Components/pydoc/Kamaelia.Util.Filter.html){.reference}.[Filter](/Components/pydoc/Kamaelia.Util.Filter.Filter.html){.reference}
===========================================================================================================================================================================================================================================================

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
