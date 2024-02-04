---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.AIMHarness
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.html){.reference}.[AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.AIMHarness.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.html){.reference}

------------------------------------------------------------------------

::: {.section}
class AIMHarness([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-AIMHarness}
--------------------------------------------------------------------------------------------------

AIMHarness() -\> new AIMHarness component

Send (\"message\", recipient, message) commands to its \"inbox\" to send
instant messages. It will output (\"buddy online\", {name: buddyname})
and (\"message\", sender, message) tuples whenever a buddy comes online
or a new message arrives for you.

::: {.section}
### [Inboxes]{#symbol-AIMHarness.Inboxes}

-   **control** : NOT USED
-   **internal control** : links to signal outbox of various child
    components
-   **inbox** : tuple-based commands for ChatManager
-   **internal inbox** : links to various child components
:::

::: {.section}
### [Outboxes]{#symbol-AIMHarness.Outboxes}

-   **outbox** : tuple-based notifications from ChatManager
-   **signal** : NOT USED
-   **internal signal** : sends shutdown handling signals to various
    child components
-   **internal outbox** : outbox to various child components
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
#### [\_\_init\_\_(self, screenname, password)]{#symbol-AIMHarness.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-AIMHarness.main}

Waits for logged-in OSCARClient and links it up to ChatManager
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
