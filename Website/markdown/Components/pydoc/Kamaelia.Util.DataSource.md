---
pagename: Components/pydoc/Kamaelia.Util.DataSource
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[DataSource](/Components/pydoc/Kamaelia.Util.DataSource.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DataSource](/Components/pydoc/Kamaelia.Util.DataSource.DataSource.html){.reference}**
-   **prefab
    [TriggeredSource](/Components/pydoc/Kamaelia.Util.DataSource.TriggeredSource.html){.reference}**
:::

-   [Data Source component](#244){.reference}
    -   [Example Usage](#245){.reference}
-   [Triggered Source component](#246){.reference}
    -   [Example Usage](#247){.reference}
:::

::: {.section}
::: {.section}
[Data Source component]{#data-source-component} {#244}
-----------------------------------------------

This component outputs messages specified at its creation one after
another.

::: {.section}
### [Example Usage]{#example-usage} {#245}

To output \"hello\" then \"world\":

``` {.literal-block}
pipeline(
    DataSource(["hello", "world"]),
    ConsoleEchoer()
).run()
```
:::
:::

::: {.section}
[Triggered Source component]{#triggered-source-component} {#246}
---------------------------------------------------------

Whenever this component receives a message on inbox, it outputs a
certain message.

::: {.section}
### [Example Usage]{#id1} {#247}

To output \"wibble\" each time a line is entered to the console:

``` {.literal-block}
pipeline(
    ConsoleReader(),
    TriggeredSource("wibble"),
    ConsoleEchoer()
).run()
```
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[DataSource](/Components/pydoc/Kamaelia.Util.DataSource.html){.reference}.[DataSource](/Components/pydoc/Kamaelia.Util.DataSource.DataSource.html){.reference}
===============================================================================================================================================================================================================================================================================

::: {.section}
class DataSource([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DataSource}
--------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-DataSource.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-DataSource.Outboxes}
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
#### [\_\_init\_\_(self, messages)]{#symbol-DataSource.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-DataSource.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[DataSource](/Components/pydoc/Kamaelia.Util.DataSource.html){.reference}.[TriggeredSource](/Components/pydoc/Kamaelia.Util.DataSource.TriggeredSource.html){.reference}
=========================================================================================================================================================================================================================================================================================

::: {.section}
prefab: TriggeredSource {#symbol-TriggeredSource}
-----------------------
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
