---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Text.TextDisplayer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Text](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}.[TextDisplayer](/Components/pydoc/Kamaelia.UI.Pygame.Text.TextDisplayer.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TextDisplayer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TextDisplayer}
-----------------------------------------------------------------------------------------------------

TextDisplayer(\...) -\> new TextDisplayer Pygame component.

Keyword arguments:

-   

    size \-- (w, h) size of the TextDisplayer surface, in pixels.

    :   Default (500, 300).

-   text\_height \-- font size. Default 18.

-   

    bgcolour \-- tuple containing RGB values for the background color.

    :   Default is a pale yellow.

-   

    fgcolour \-- tuple containing RGB values for the text color.

    :   Default is black.

-   

    position \-- tuple containing x,y coordinates of the surface\'s

    :   upper left corner in relation to the Pygame window. Default
        (0,0)

::: {.section}
### [Inboxes]{#symbol-TextDisplayer.Inboxes}

-   **control** : shutdown handling
-   **\_quitevents** : user-generated quit events
-   **\_surface** : for PygameDisplay to send surfaces to
-   **inbox** : for incoming lines of text
:::

::: {.section}
### [Outboxes]{#symbol-TextDisplayer.Outboxes}

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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-TextDisplayer.__init__}

Initialises
:::

::: {.section}
#### [initPygame(self, \*\*argd)]{#symbol-TextDisplayer.initPygame}

requests a display surface from the PygameDisplay service, fills the
color in, and copies it
:::

::: {.section}
#### [main(self)]{#symbol-TextDisplayer.main}

Main loop
:::

::: {.section}
#### [needShutdown(self)]{#symbol-TextDisplayer.needShutdown}

Checks for control messages
:::

::: {.section}
#### [update(self, text)]{#symbol-TextDisplayer.update}

Updates text to the bottom of the screen while scrolling old text
upwards. Delegates most of the work to updateLine
:::

::: {.section}
#### [updateLine(self, line)]{#symbol-TextDisplayer.updateLine}

Updates one line of text to bottom of screen, scrolling old text
upwards.
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
