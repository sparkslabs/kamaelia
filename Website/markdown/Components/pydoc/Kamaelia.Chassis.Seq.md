---
pagename: Components/pydoc/Kamaelia.Chassis.Seq
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Seq](/Components/pydoc/Kamaelia.Chassis.Seq.html){.reference}
=====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Seq](/Components/pydoc/Kamaelia.Chassis.Seq.Seq.html){.reference}**
:::

-   [Run components one after the other (in sequence)](#275){.reference}
    -   [Example Usage](#276){.reference}
    -   [Behaviour](#277){.reference}
:::

::: {.section}
Run components one after the other (in sequence) {#275}
================================================

A Seq component runs components one after the other in sequence, waiting
until one terminates before starting the next.

Strings can also be put in the sequence. They\'ll be printed to the
console

::: {.section}
[Example Usage]{#example-usage} {#276}
-------------------------------

Run several OneShot components running one after the other:

``` {.literal-block}
Pipeline( Seq( "BEGIN SEQUENCE",
               OneShot("Hello\n"),
               OneShot("Doctor\n"),
               OneShot("Name\n"),
               OneShot("Continue\n"),
               OneShot("Yesterday\n"),
               OneShot("Tomorrow\n"),
               "END SEQUENCE",
             ),
          ConsoleEchoer(),
        ).run()
```

Running this generates the following output:

``` {.literal-block}
BEGIN SEQUENCE
Hello
Doctor
Name
Continue
Yesterday
Tomorrow
END SEQUENCE
```
:::

::: {.section}
[Behaviour]{#behaviour} {#277}
-----------------------

Each component in the sequence is activated as a child component and is
wired up so that the \"inbox\" inbox and \"outbox\" outbox are forwarded
to the \"inbox\" inbox and \"outbox\" outbox of the Seq component
itself.

When the child component terminates it is replaced with the next in the
sequence.

If a string is listed instead of a component then it is printed on the
console and Seq immediately moves onto the next in the sequence.

Any messages sent out of the child component\'s \"signal\" outbox are
dropped - this is so that if you Pipeline a Seq component to another, it
does not cause it to terminate when the Seq component switches to a new
child.

This component ignores any messages sent to its \"control\" inbox.

When the end of the sequence is reached, a producerFinished() message is
sent out of the \"signal\" outbox and the component terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Seq](/Components/pydoc/Kamaelia.Chassis.Seq.html){.reference}.[Seq](/Components/pydoc/Kamaelia.Chassis.Seq.Seq.html){.reference}
========================================================================================================================================================================================================================================================

::: {.section}
class Seq([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Seq}
-------------------------------------------------------------------------------------------

Seq(\*sequence) -\> new Seq component.

Runs a set of components in sequence, one after the other. Their
\"inbox\" inbox and \"outbox\" outbox are forwarded to the \"inbox\"
inbox and \"outbox\" outbox of the Seq component.

Keyword arguments:

-   \*sequence \-- Components that will be run, in sequence. Can also
    include strings that will be output to the console.

::: {.section}
### [Inboxes]{#symbol-Seq.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Seq.Outboxes}
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
#### [\_\_init\_\_(self, \*sequence)]{#symbol-Seq.__init__}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Seq.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Seq.main}
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
