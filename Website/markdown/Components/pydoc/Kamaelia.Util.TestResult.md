---
pagename: Components/pydoc/Kamaelia.Util.TestResult
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[TestResult](/Components/pydoc/Kamaelia.Util.TestResult.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TestResult](/Components/pydoc/Kamaelia.Util.TestResult.TestResult.html){.reference}**
:::

-   [Basic Result Tester](#229){.reference}
    -   [Example Usage](#230){.reference}
    -   [How does it work?](#231){.reference}
:::

::: {.section}
Basic Result Tester {#229}
===================

A simple component for testing that a stream of data tests true. This is
NOT intended for live systems, but for testing and development purposes
only.

::: {.section}
[Example Usage]{#example-usage} {#230}
-------------------------------

::
:   Pipeline( source(), TestResult() ).activate()

Raises an assertion error if source() generates a value that doesn\'t
test true.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#231}
--------------------------------------

If the component receives a value on its \"inbox\" inbox that does not
test true, then an AssertionError is raised.

If the component receives a StopSystem message on its \"control\" inbox
then a StopSystemException message is raised as an exception.

This component does not terminate (unless it throws an exception).

It does not pass on the data it receives.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[TestResult](/Components/pydoc/Kamaelia.Util.TestResult.html){.reference}.[TestResult](/Components/pydoc/Kamaelia.Util.TestResult.TestResult.html){.reference}
===============================================================================================================================================================================================================================================================================

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
