---
pagename: Components/pydoc/Kamaelia.Util.TestResult.TestResult
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[TestResult](/Components/pydoc/Kamaelia.Util.TestResult.html){.reference}.[TestResult](/Components/pydoc/Kamaelia.Util.TestResult.TestResult.html){.reference}
===============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.TestResult.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TestResult([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TestResult}
--------------------------------------------------------------------------------------------------

TestResult() -\> new TestResult.

Component that raises an AssertionError if it receives data on its
\"inbox\" inbox that does not test true. Or raises a StopSystemException
if a StopSystem message is received on its \"control\" inbox.

::: {.section}
### [Inboxes]{#symbol-TestResult.Inboxes}

-   **control** : StopSystemException messages
-   **inbox** : Data to test
:::

::: {.section}
### [Outboxes]{#symbol-TestResult.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
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
#### [mainBody(self)]{#symbol-TestResult.mainBody}
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
