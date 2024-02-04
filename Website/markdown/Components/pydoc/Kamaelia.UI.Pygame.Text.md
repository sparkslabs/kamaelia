---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Text
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Text](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}
===============================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TextDisplayer](/Components/pydoc/Kamaelia.UI.Pygame.Text.TextDisplayer.html){.reference}**
-   **component
    [Textbox](/Components/pydoc/Kamaelia.UI.Pygame.Text.Textbox.html){.reference}**
:::

-   [Pygame components for text input and display](#374){.reference}
    -   [Example Usage](#375){.reference}
    -   [How does it work?](#376){.reference}
    -   [Known issues](#377){.reference}
:::

::: {.section}
Pygame components for text input and display {#374}
============================================

TextDisplayer displays any data it receives on a Pygame surface. Every
new piece of data is displayed on its own line, and lines wrap
automatically.

Textbox displays user input while the user types, and sends its string
buffer to its \'outbox\' when it receives a \' \'.

::: {.section}
[Example Usage]{#example-usage} {#375}
-------------------------------

To take user input in Textbox and display it in TextDisplayer:

``` {.literal-block}
Pipeline(Textbox(size = (800, 300),
                 position = (0,0)),
         TextDisplayer(size = (800, 300),
                       position = (0,340))
         ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#376}
--------------------------------------

TextDisplayer requests a display from the Pygame Display service and
requests that Pygame Display send all keypresses to it. Every time
TextDisplayer receives a keypress, it updates its string buffer and the
display.

If it receives a newline, or if text must wrap, it moves the existing
text upwards and blits the new line onto the bottom.
:::

::: {.section}
[Known issues]{#known-issues} {#377}
-----------------------------

The line wrapping length is specified by the width of the display
divided by the width of the letter \'a\' in the displayed font, so lines
may wrap too far off the edge of the screen if the user types very
narrow text (i.e. just spaces with no other charachters), or too far
inside the edge of the screen (usually).
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Text](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}.[TextDisplayer](/Components/pydoc/Kamaelia.UI.Pygame.Text.TextDisplayer.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================

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

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Text](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}.[Textbox](/Components/pydoc/Kamaelia.UI.Pygame.Text.Textbox.html){.reference}
=============================================================================================================================================================================================================================================================================================================================

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
