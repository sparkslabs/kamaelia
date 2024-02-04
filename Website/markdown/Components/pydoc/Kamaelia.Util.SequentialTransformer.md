---
pagename: Components/pydoc/Kamaelia.Util.SequentialTransformer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer.html){.reference}
================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer.SequentialTransformer.html){.reference}**
:::

-   [Sequential Transformer component](#189){.reference}
    -   [Example Usage](#190){.reference}
:::

::: {.section}
Sequential Transformer component {#189}
================================

This component applies all the functions supplied to incoming messages.
If the output from the final function is None, no message is sent.

::: {.section}
[Example Usage]{#example-usage} {#190}
-------------------------------

To read in lines of text, convert to upper case, prepend \"foo\", and
append \"bar!\" and then write to the console:

``` {.literal-block}
Pipeline(
    ConsoleReader(eol=""),
    SequentialTransformer( str,
                           str.upper,
                           lambda x : "foo" + x,
                           lambda x : x + "bar!",
                         ),
    ConsoleEchoer(),
).run()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer.html){.reference}.[SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer.SequentialTransformer.html){.reference}
======================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SequentialTransformer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SequentialTransformer}
-------------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-SequentialTransformer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SequentialTransformer.Outboxes}
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
#### [\_\_init\_\_(self, \*functions)]{#symbol-SequentialTransformer.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-SequentialTransformer.main}
:::

::: {.section}
#### [pipeline(self, msg)]{#symbol-SequentialTransformer.pipeline}
:::

::: {.section}
#### [processMessage(self, msg)]{#symbol-SequentialTransformer.processMessage}
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
