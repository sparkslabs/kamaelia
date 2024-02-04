---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Text.Textbox
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Text](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}.[Textbox](/Components/pydoc/Kamaelia.UI.Pygame.Text.Textbox.html){.reference}
=============================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Textbox(TextDisplayer) {#symbol-Textbox}
----------------------------

Textbox(\...) -\> New Pygame Textbox component

Keyword Arguments:

-   Textbox inherits its keyword arguments from TextDisplayer. Please
    see TextDisplayer docs.

Reads keyboard input and updates it on the screen. Flushes string buffer
and sends it to outbox when a newline is encountered.

::: {.section}
### [Inboxes]{#symbol-Textbox.Inboxes}

-   **control** : shutdown handling
-   **\_quitevents** : user-generated quit events
-   **\_events** : key events
-   **\_surface** : for PygameDisplay to send surfaces to
-   **inbox** : for incoming lines of text
:::

::: {.section}
### [Outboxes]{#symbol-Textbox.Outboxes}

-   **outbox** : not used
-   **signal** : propagates out shutdown signals
-   **\_pygame** : for sending requests to PygameDisplay
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
#### [main(self)]{#symbol-Textbox.main}

Requests a surface from PygameDisplay and registers to listen for events
Then enters the main loop, which checks for Pygame events and updates
them to the screen.
:::

::: {.section}
#### [setText(self, text)]{#symbol-Textbox.setText}

erases the screen and updates it with text
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.UI.Pygame.Text.TextDisplayer](/Components/pydoc/Kamaelia.UI.Pygame.Text.TextDisplayer.html){.reference} :

-   [updateLine](/Components/pydoc/Kamaelia.UI.Pygame.Text.html#symbol-TextDisplayer.updateLine){.reference}(self,
    line)
-   [update](/Components/pydoc/Kamaelia.UI.Pygame.Text.html#symbol-TextDisplayer.update){.reference}(self,
    text)
-   [needShutdown](/Components/pydoc/Kamaelia.UI.Pygame.Text.html#symbol-TextDisplayer.needShutdown){.reference}(self)
-   [initPygame](/Components/pydoc/Kamaelia.UI.Pygame.Text.html#symbol-TextDisplayer.initPygame){.reference}(self,
    \*\*argd)
-   [\_\_init\_\_](/Components/pydoc/Kamaelia.UI.Pygame.Text.html#symbol-TextDisplayer.__init__){.reference}(self,
    \*\*argd)
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
