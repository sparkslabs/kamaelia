---
pagename: Components/pydoc/Kamaelia.Util.Fanout
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Fanout](/Components/pydoc/Kamaelia.Util.Fanout.html){.reference}
==================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Fanout](/Components/pydoc/Kamaelia.Util.Fanout.Fanout.html){.reference}**
:::

-   [Sending an output to many places](#241){.reference}
    -   [Example Usage](#242){.reference}
    -   [How does it work?](#243){.reference}
:::

::: {.section}
Sending an output to many places {#241}
================================

This component copies data sent to its inbox to multiple, specified
outboxes. This allows you to \'fan out\' a data source to several
predetermined destinations.

::: {.section}
[Example Usage]{#example-usage} {#242}
-------------------------------

Output data source both to a file and to the console:

``` {.literal-block}
Graphline( source  = MyDataSource(...),
           split   = Fanout(["toConsole","toFile"]),
           file    = SimpleFileWriter(filename="outfile"),
           console = ConsoleEchoer(),
           linkages = {
             ("source","outbox")   : ("split","inbox"),
             ("split","toConsole") : ("console","inbox"),
             ("split","toFile")    : ("file","inbox"),
           }
         ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#243}
--------------------------------------

At initialization, specify a list of names for outboxes. Once the
component is activated, any data sent to its \"inbox\" inbox will be
replicated out to the list of outboxes you specified.

In effect, data sent to the \"inbox\" inbox is \'fanned out\' to the
specified set of destinations.

Nothing is sent to the \"outbox\" outbox.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it is sent on to the \"signal\" outbox and the
component terminates.

There is no corresponding \'Fanout\' of data flowing into the
\"control\" inbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Fanout](/Components/pydoc/Kamaelia.Util.Fanout.html){.reference}.[Fanout](/Components/pydoc/Kamaelia.Util.Fanout.Fanout.html){.reference}
===========================================================================================================================================================================================================================================================

::: {.section}
class Fanout([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Fanout}
----------------------------------------------------------------------------------------------

Fanout(boxnames) -\> new Fanout component.

A component that copies anything received on its \"inbox\" inbox to the
named list of outboxes.

Keyword arguments:

-   boxnames \-- list of names for the outboxes any input will be fanned
    out to.

::: {.section}
### [Inboxes]{#symbol-Fanout.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data to be fanned out
:::

::: {.section}
### [Outboxes]{#symbol-Fanout.Outboxes}

-   **outbox** : NOT USED
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
#### [\_\_init\_\_(self, boxnames)]{#symbol-Fanout.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Fanout.main}

Main loop.
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
