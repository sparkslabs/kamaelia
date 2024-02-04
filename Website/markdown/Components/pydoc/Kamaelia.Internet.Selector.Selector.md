---
pagename: Components/pydoc/Kamaelia.Internet.Selector.Selector
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Selector](/Components/pydoc/Kamaelia.Internet.Selector.html){.reference}.[Selector](/Components/pydoc/Kamaelia.Internet.Selector.Selector.html){.reference}
=====================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.Selector.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Selector([Axon.ThreadedComponent.threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}) {#symbol-Selector}
----------------------------------------------------------------------------------------------------------------------------------------------------------

Selector() -\> new Selector component

Use Selector.getSelectorService(\...) in preference as it returns an
existing instance, or automatically creates a new one.

::: {.section}
### [Inboxes]{#symbol-Selector.Inboxes}

-   **control** : Recieving a
    [Axon.Ipc.shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference}()
    message here causes shutdown
-   **inbox** : Not used at present
-   **notify** : Used to be notified about things to select
:::

::: {.section}
### [Outboxes]{#symbol-Selector.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-Selector.__init__}
:::

::: {.section}
#### [addLinks(self, replyService, selectable, meta, selectables, boxBase)]{#symbol-Selector.addLinks}

Adds a file descriptor (selectable).

Creates a corresponding outbox, with name based on boxBase; links it to
the component that wants to be notified; adds the file descriptor to the
set of selectables; and records the box and linkage info in meta.
:::

::: {.section}
#### [handleNotify(self, meta, readers, writers, exceptionals)]{#symbol-Selector.handleNotify}

Process requests to add and remove file descriptors (selectables) that
arrive at the \"notify\" inbox.
:::

::: {.section}
#### [main(self)]{#symbol-Selector.main}

Main loop
:::

::: {.section}
#### [removeLinks(self, selectable, meta, selectables)]{#symbol-Selector.removeLinks}

Removes a file descriptor (selectable).

Removes the corresponding entry from meta and selectables; unlinks from
the component to be notified; and deletes the corresponding outbox.
:::

::: {.section}
#### [stop(self)]{#symbol-Selector.stop}
:::

::: {.section}
#### [trackedBy(self, tracker)]{#symbol-Selector.trackedBy}
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
