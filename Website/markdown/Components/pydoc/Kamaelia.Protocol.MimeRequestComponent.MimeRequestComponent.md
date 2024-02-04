---
pagename: Components/pydoc/Kamaelia.Protocol.MimeRequestComponent.MimeRequestComponent
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[MimeRequestComponent](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent.html){.reference}.[MimeRequestComponent](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent.MimeRequestComponent.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent.html){.reference}

------------------------------------------------------------------------

::: {.section}
class MimeRequestComponent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-MimeRequestComponent}
------------------------------------------------------------------------------------------------------------

Component that accepts raw data, parses it into consituent parts of a
MIME request. Attempts no interpretation of the request however.

::: {.section}
### [Inboxes]{#symbol-MimeRequestComponent.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-MimeRequestComponent.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-MimeRequestComponent.__init__}
:::

::: {.section}
#### [checkEndOfHeader(self)]{#symbol-MimeRequestComponent.checkEndOfHeader}
:::

::: {.section}
#### [getALine(self)]{#symbol-MimeRequestComponent.getALine}

Sets the *CURRENT* line arguments
:::

::: {.section}
#### [getData(self)]{#symbol-MimeRequestComponent.getData}
:::

::: {.section}
#### [getRequestLine(self)]{#symbol-MimeRequestComponent.getRequestLine}

Sets the *REQUEST* line arguments
:::

::: {.section}
#### [handleDataAquisition(self)]{#symbol-MimeRequestComponent.handleDataAquisition}

This is currently clunky and effectively implements a state machine.
Should consider rewriting as a generator
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-MimeRequestComponent.initialiseComponent}
:::

::: {.section}
#### [mainBody(self)]{#symbol-MimeRequestComponent.mainBody}
:::

::: {.section}
#### [nextLine(self)]{#symbol-MimeRequestComponent.nextLine}
:::

::: {.section}
#### [readHeader(self)]{#symbol-MimeRequestComponent.readHeader}
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
