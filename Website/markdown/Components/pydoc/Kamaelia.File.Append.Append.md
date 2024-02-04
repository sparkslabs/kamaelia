---
pagename: Components/pydoc/Kamaelia.File.Append.Append
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Append](/Components/pydoc/Kamaelia.File.Append.html){.reference}.[Append](/Components/pydoc/Kamaelia.File.Append.Append.html){.reference}
===========================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.Append.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Append([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Append}
----------------------------------------------------------------------------------------------

Appender() -\> component that incrementally append data to the end of a
file (think logging)

Uses the following keyword argyments:

``` {.literal-block}
* filename - File to append to (required)
* forwarder - copy to outbox (default: True)
* blat_file - write empty file (default: False)
* hold_open - keep file open (default: True)
```

::: {.section}
### [Inboxes]{#symbol-Append.Inboxes}

-   **control** : Send any message here to shut this component down
-   **inbox** : data to append to the end of the file.
:::

::: {.section}
### [Outboxes]{#symbol-Append.Outboxes}

-   **outbox** : a copy of the message is forwarded here
-   **signal** : passes on the message used to shutdown the component
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Append.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Append.main}
:::

::: {.section}
#### [stop(self)]{#symbol-Append.stop}
:::

::: {.section}
#### [writeChunk(self, chunk)]{#symbol-Append.writeChunk}
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
