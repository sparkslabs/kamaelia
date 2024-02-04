---
pagename: Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextServiceFilter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[NowNext](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}.[NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextServiceFilter.html){.reference}
========================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}

------------------------------------------------------------------------

::: {.section}
class NowNextServiceFilter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NowNextServiceFilter}
------------------------------------------------------------------------------------------------------------

NowNextServiceFilter(\*services) -\> new NowNextServiceFilter component.

Filters simplified events from Event Information Tables, only letting
through those that match the service ids specified.

Argument list is a list of service id\'s to be let through by the
filter.

::: {.section}
### [Inboxes]{#symbol-NowNextServiceFilter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-NowNextServiceFilter.Outboxes}
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
#### [\_\_init\_\_(self, \*services)]{#symbol-NowNextServiceFilter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-NowNextServiceFilter.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-NowNextServiceFilter.shutdown}

Shutdown handling.
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
