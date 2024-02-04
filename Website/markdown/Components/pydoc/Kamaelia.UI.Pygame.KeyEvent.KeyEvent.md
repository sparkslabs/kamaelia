---
pagename: Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.KeyEvent
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.html){.reference}.[KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.KeyEvent.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.html){.reference}

------------------------------------------------------------------------

::: {.section}
class KeyEvent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-KeyEvent}
------------------------------------------------------------------------------------------------

KeyEvent(\[allkeys\]\[,key\_events\]\[,outboxes\]) -\> new KeyEvent
component.

Component that sends out messages in response to pygame keypress events.

Keyword arguments:

-   allkeys \-- if True, all keystrokes send messages out of \"allkeys\"
    outbox (default=False)
-   key\_events \-- dict mapping pygame keycodes to (msg,\"outboxname\")
    pairs (default=None)
-   outboxes \-- dict of \"outboxname\":\"description\" key:value pairs
    (default={})

::: {.section}
### [Inboxes]{#symbol-KeyEvent.Inboxes}

-   **control** : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   **callback** : Receive callbacks from Pygame Display
-   **inbox** : Receive events from Pygame Display
:::

::: {.section}
### [Outboxes]{#symbol-KeyEvent.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   **allkeys** : Outbox that receives \*every\* keystroke if enabled
-   **display\_signal** : Outbox used for communicating to the display
    surface
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
#### [\_\_init\_\_(self\[, allkeys\]\[, key\_events\]\[, key\_up\_events\]\[, outboxes\])]{#symbol-KeyEvent.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-KeyEvent.main}

Main loop.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-KeyEvent.waitBox}

Generator. yields 1 until data is ready on the named inbox.
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
