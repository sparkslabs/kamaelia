---
pagename: Components/pydoc/Kamaelia.Util.UnseenOnly
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly.UnseenOnly.html){.reference}**
:::

-   [UnseenOnly component](#184){.reference}
    -   [Example Usage](#185){.reference}
:::

::: {.section}
UnseenOnly component {#184}
====================

This component forwards on any messages it receives that it has not seen
before.

::: {.section}
[Example Usage]{#example-usage} {#185}
-------------------------------

Lines entered into this setup will only be duplicated on screen the
first time they are entered:

``` {.literal-block}
pipeline(
    ConsoleReader(),
    UnseenOnly(),
    ConsoleEchoer()
).run()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly.html){.reference}.[UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly.UnseenOnly.html){.reference}
===============================================================================================================================================================================================================================================================================

::: {.section}
class UnseenOnly([Kamaelia.Util.PureTransformer.PureTransformer](/Components/pydoc/Kamaelia.Util.PureTransformer.PureTransformer.html){.reference}) {#symbol-UnseenOnly}
---------------------------------------------------------------------------------------------------------------------------------------------------

UnseenOnly() -\> new UnseenOnly component.

Send items to the \"inbox\" inbox. Any items not \"seen\" already will
be forwarded out of the \"outbox\" outbox. Send the same thing two or
more times and it will only be sent on the first time.

::: {.section}
### [Inboxes]{#symbol-UnseenOnly.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-UnseenOnly.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-UnseenOnly.__init__}
:::

::: {.section}
#### [processMessage(self, msg)]{#symbol-UnseenOnly.processMessage}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.Util.PureTransformer.PureTransformer](/Components/pydoc/Kamaelia.Util.PureTransformer.PureTransformer.html){.reference} :

-   [main](/Components/pydoc/Kamaelia.Util.PureTransformer.html#symbol-PureTransformer.main){.reference}(self)
:::
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
