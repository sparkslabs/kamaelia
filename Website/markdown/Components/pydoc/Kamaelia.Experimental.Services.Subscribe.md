---
pagename: Components/pydoc/Kamaelia.Experimental.Services.Subscribe
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}.[Subscribe](/Components/pydoc/Kamaelia.Experimental.Services.Subscribe.html){.reference}
=======================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Subscribe([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Subscribe}
-------------------------------------------------------------------------------------------------

Subscribes to a service, and forwards what it receives to its outbox.
Also forwards anything that arrives at its inbox to its outbox.

Unsubscribes when shutdown.

::: {.section}
### [Inboxes]{#symbol-Subscribe.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Subscribe.Outboxes}

-   **outbox** :
-   **signal** : shutdown signalling
-   **\_toService** : request to service
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
#### [\_\_init\_\_(self, servicename, \*requests)]{#symbol-Subscribe.__init__}

Subscribe to the specified service, wiring to it, then sending the
specified messages. Requests are of the form (\"ADD\", request,
destination)
:::

::: {.section}
#### [main(self)]{#symbol-Subscribe.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-Subscribe.shutdown}
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
