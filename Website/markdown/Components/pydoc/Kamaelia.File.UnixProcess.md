---
pagename: Components/pydoc/Kamaelia.File.UnixProcess
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.html){.reference}
============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.UnixProcess.html){.reference}**
:::

-   [UnixProcess](#709){.reference}
    -   [Example Usage](#710){.reference}
    -   [How to use it](#711){.reference}
    -   [Python and platform compatibility](#712){.reference}
:::

::: {.section}
UnixProcess {#709}
===========

Launch another unix process and communicate with it via its standard
input and output, by using the \"inbox\" and \"outbox\" of this
component.

::: {.section}
[Example Usage]{#example-usage} {#710}
-------------------------------

The purpose behind this component is to allow the following to occur:

``` {.literal-block}
Pipeline(
  dataSource(),
  UnixProcess("command", *args),
  dataSink(),
).run()
```
:::

::: {.section}
[How to use it]{#how-to-use-it} {#711}
-------------------------------

More specificaly, the longer term interface of this component will be:

UnixProcess:

-   inbox - data recieved here is sent to the program\'s stdin
-   outbox - data sent here is from the program\'s stdout
-   control - at some point we\'ll define a mechanism for describing
    control messages - these will largely map to SIG\* messages though.
    We also need to signal how we close our writing pipe. This can
    happen using the normal producerFinished message.
-   signal - this will be caused by things like SIGPIPE messages. What
    this will look like is yet to be defined. (Let\'s see what works
    first.
:::

::: {.section}
[Python and platform compatibility]{#python-and-platform-compatibility} {#712}
-----------------------------------------------------------------------

This code is only really tested on Linux.

Initially this will be python 2.4 only, but it would be nice to support
older versions of python (eg 2.2.2 - for Nokia mobiles).

For the moment I\'m going to send STDERR to dev null, however things
won\'t stay that way.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.html){.reference}.[UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.UnixProcess.html){.reference}
====================================================================================================================================================================================================================================================================================

::: {.section}
class UnixProcess([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-UnixProcess}
---------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-UnixProcess.Inboxes}

-   **control** : We receive shutdown messages here
-   **stdinready** : We\'re notified here when we can write to the
    sub-process
-   **inbox** : Strings containing data to send to the sub process
-   **stderrready** : We\'re notified here when we can read errors from
    the sub-process
-   **stdoutready** : We\'re notified here when we can read from the
    sub-process
:::

::: {.section}
### [Outboxes]{#symbol-UnixProcess.Outboxes}

-   **outbox** : data from the sub command is output here
-   **signal** : not used
-   **selectorsignal** : To send control messages to the selector
-   **selector** : We send messages to the selector here, requesting it
    tell us when file handles can be read from/written to
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
#### [\_\_init\_\_(self, command)]{#symbol-UnixProcess.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-UnixProcess.main}
:::

::: {.section}
#### [openSubprocess(self)]{#symbol-UnixProcess.openSubprocess}
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
