---
pagename: Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[MagnaDoodle](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.html){.reference}
=============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [MagnaDoodle](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.MagnaDoodle.html){.reference}**
:::

-   [Simple Pygame drawing board](#381){.reference}
:::

::: {.section}
Simple Pygame drawing board {#381}
===========================

A simple drawing board for the pygame display service.

Use your left mouse button to draw to the board and the right to erase
your artwork.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[MagnaDoodle](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.html){.reference}.[MagnaDoodle](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.MagnaDoodle.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class MagnaDoodle([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-MagnaDoodle}
---------------------------------------------------------------------------------------------------

MagnaDoodle(\...) -\> A new MagnaDoodle component.

A simple drawing board for the pygame display service.

(this component and its documentation is heaviliy based on
[Kamaelia.UI.Pygame.Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.html){.reference})

Keyword arguments:

-   position \-- (x,y) position of top left corner in pixels
-   margin \-- pixels margin between caption and button edge (default=8)
-   bgcolour \-- (r,g,b) fill colour (default=(224,224,224))
-   fgcolour \-- (r,g,b) text colour (default=(0,0,0))
-   transparent \-- draw background transparent if True (default=False)
-   size \-- None or (w,h) in pixels (default=None)

::: {.section}
### [Inboxes]{#symbol-MagnaDoodle.Inboxes}

-   **control** : For shutdown messages
-   **callback** : Receive callbacks from PygameDisplay
-   **inbox** : Receive events from PygameDisplay
:::

::: {.section}
### [Outboxes]{#symbol-MagnaDoodle.Outboxes}

-   **outbox** : not used
-   **signal** : For shutdown messages
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
#### [\_\_init\_\_(self\[, caption\]\[, position\]\[, margin\]\[, bgcolour\]\[, fgcolour\]\[, msg\]\[, transparent\]\[, size\])]{#symbol-MagnaDoodle.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [blitToSurface(self)]{#symbol-MagnaDoodle.blitToSurface}
:::

::: {.section}
#### [drawBG(self)]{#symbol-MagnaDoodle.drawBG}
:::

::: {.section}
#### [main(self)]{#symbol-MagnaDoodle.main}

Main loop.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-MagnaDoodle.waitBox}

Generator. yields 1 until data ready on the named inbox.
:::
:::

::: {.section}
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
