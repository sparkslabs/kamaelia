---
pagename: Components/pydoc/Kamaelia.Chassis.Pipeline
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference}
===============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.Pipeline.html){.reference}**
:::

-   [Wiring up components in a Pipeline](#264){.reference}
    -   [Example Usage](#265){.reference}
    -   [How does it work?](#266){.reference}
-   [Test documentation](#267){.reference}
:::

::: {.section}
Wiring up components in a Pipeline {#264}
==================================

The Pipeline component wires up a set of components in a linear chain (a
Pipeline) and encapsulates them as a single component.

::: {.section}
[Example Usage]{#example-usage} {#265}
-------------------------------

A simple pipeline of 4 components:

``` {.literal-block}
Pipeline(MyDataSource(...),
         MyFirstStageOfProcessing(...),
         MySecondStageOfProcessing(...),
         MyDestination(...),
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#266}
--------------------------------------

A Pipeline component gives you a way of wiring up a system of components
in a chain and then encapsulating the whole as a single component. The
inboxes of this component pass through to the inboxes of the first
component in the Pipeline, and the outboxes of the last component pass
through to the outboxes of the Pipeline component.

The components you specify are registered as children of the Pipeline
component. When Pipeline is activate, all children are wired up and
activated.

For the components in the Pipeline, \"outbox\" outboxes are wired to
\"inbox\" inboxes, and \"signal\" outboxes are wired to \"control\"
inboxes. They are wired up in the order in which you specify them - data
will flow through the chain from first component to last.

The \"inbox\" and \"control\" inboxes of the Pipeline component are
wired to pass-through to the \"inbox\" and \"control\" inboxes
(respectively) of the first component in the Pipeline chain.

The \"outbox\" and \"signal\" outboxes of the last component in the
Pipeline chain are wired to pass-through to the \"outbox\" and
\"signal\" outboxes (respectively) of the Pipeline component.

During runtime, the Pipeline component monitors the child components. It
will terminate if, and only if, *all* the child components have also
terminated.

NOTE that if your child components create additional components
themselves, the Pipeline component will not know about them. It only
monitors the components it was originally told about.

Pipeline does not intercept any of its inboxes or outboxes. It ignores
whatever traffic flows through them.
:::

Test documentation {#267}
==================

Tests passed:

-   Children are activated as soon as the Pipeline itself is activated,
    but no sooner.
-   Pipeline wires up children so one child\'s \"outbox\" outbox feeds
    to the next\'s \"inbox\" inbox.
-   Pipeline wires up children so one child\'s \"signal\" outbox feeds
    to the next\'s \"control\" inbox.
-   Pipeline wires up the first child\'s \"inbox\" and \"control\"
    inboxes to receive from the pipeline\'s \"inbox\" and \"control\"
    inboxes.
-   Pipeline wires up the last child\'s \"outbox\" and \"signal\"
    outboxes to send out of the pipeline\'s \"outbox\" and \"signal\"
    outboxes.
-   test\_PipelineTerminatesOnlyWhenAllChildrenHaveTerminated
    (\_\_main\_\_.Test\_Pipeline)
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.Pipeline.html){.reference}
=================================================================================================================================================================================================================================================================================

::: {.section}
class Pipeline([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Pipeline}
------------------------------------------------------------------------------------------------

Pipeline(\*components) -\> new Pipeline component.

Encapsulates the specified set of components and wires them up in a
chain (a Pipeline) in the order you provided them.

Keyword arguments:

-   components \-- the components you want, in the order you want them
    wired up

::: {.section}
### [Inboxes]{#symbol-Pipeline.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Pipeline.Outboxes}
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
#### [\_\_init\_\_(self, \*components, \*\*argv)]{#symbol-Pipeline.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Pipeline.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Pipeline.main}

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
