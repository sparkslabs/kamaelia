---
pagename: Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.FortuneCookieProtocol
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[FortuneCookieProtocol](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.html){.reference}.[FortuneCookieProtocol](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.FortuneCookieProtocol.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.html){.reference}

------------------------------------------------------------------------

::: {.section}
class FortuneCookieProtocol([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-FortuneCookieProtocol}
-------------------------------------------------------------------------------------------------------------

FortuneCookieProtocol(\[debug\]) -\> new FortuneCookieProtocol
component.

A protocol that spits out a random fortune cookie, then terminates.

Keyword arguments:

-   debug \-- Debugging output control (default=0)

::: {.section}
### [Inboxes]{#symbol-FortuneCookieProtocol.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-FortuneCookieProtocol.Outboxes}
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
#### [\_\_init\_\_(self\[, debug\])]{#symbol-FortuneCookieProtocol.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-FortuneCookieProtocol.initialiseComponent}

Initialises component. Sets up a ReadFileAdapter to read the result of
running \'fortune\'.
:::

::: {.section}
#### [mainBody(self)]{#symbol-FortuneCookieProtocol.mainBody}

Main body.

All the interesting work has been done by linking the file reader\'s
output to our output. Messages sent to control are unchecked and the
first message causes the component to exit.
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
