---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.ChatManager
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.html){.reference}.[ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.ChatManager.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ChatManager(SNACExchanger) {#symbol-ChatManager}
--------------------------------

ChatManager() -\> new ChatManager component.

::: {.section}
### [Inboxes]{#symbol-ChatManager.Inboxes}

-   **control** : NOT USED
-   **errors** : error messages
-   **inbox** : incoming FLAPs on channel 2
-   **talk** : outgoing messages
:::

::: {.section}
### [Outboxes]{#symbol-ChatManager.Outboxes}

-   **outbox** : outgoing FLAPs
-   **signal** : NOT USED
-   **heard** : echoes peer messages to this box.
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
#### [\_\_init\_\_(self)]{#symbol-ChatManager.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [cleanMessage(self, message)]{#symbol-ChatManager.cleanMessage}

strips HTML tags off messages
:::

::: {.section}
#### [main(self)]{#symbol-ChatManager.main}

Main loop.
:::

::: {.section}
#### [receiveMessage(self, body)]{#symbol-ChatManager.receiveMessage}

Extracts the sender and message text from SNAC body, and sends the tuple
(\"message\", sender, message) to \"heard\".
:::

::: {.section}
#### [sendMessage(self, buddyname, text)]{#symbol-ChatManager.sendMessage}

constructs SNAC (04, 06), the \"send message\" SNAC and sends it to
\"outbox\"
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
