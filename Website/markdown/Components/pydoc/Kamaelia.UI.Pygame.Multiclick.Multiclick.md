---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Multiclick.Multiclick
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Multiclick](/Components/pydoc/Kamaelia.UI.Pygame.Multiclick.html){.reference}.[Multiclick](/Components/pydoc/Kamaelia.UI.Pygame.Multiclick.Multiclick.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.Multiclick.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Multiclick([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Multiclick}
--------------------------------------------------------------------------------------------------

Multiclick(\...) -\> new Multiclick component.

Create a button widget in pygame, using the Pygame Display service.
Sends a message out of its outbox when clicked.

Keyword arguments (all optional):

-   caption \-- text (default=\"Button \<component id\>\")
-   position \-- (x,y) position of top left corner in pixels
-   margin \-- pixels margin between caption and button edge (default=8)
-   bgcolour \-- (r,g,b) fill colour (default=(224,224,224))
-   fgcolour \-- (r,g,b) text colour (default=(0,0,0))
-   msg \-- sent when clicked (default=(\"CLICK\",self.id)) of msgs is
    not specified
-   msgs \-- list of messages. msgs\[x\] is sent when button X is
    clicked (default=None)
-   transparent \-- draw background transparent if True (default=False)
-   size \-- (width,height) pixels size of the button (default=scaled to
    fit caption)

::: {.section}
### [Inboxes]{#symbol-Multiclick.Inboxes}

-   **control** : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   **callback** : Receive callbacks from Pygame Display
-   **inbox** : Receive events from Pygame Display
:::

::: {.section}
### [Outboxes]{#symbol-Multiclick.Outboxes}

-   **outbox** : button click events emitted here
-   **signal** : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   **display\_signal** : For sending signals to the Pygame Display
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
#### [\_\_init\_\_(self\[, caption\]\[, position\]\[, margin\]\[, bgcolour\]\[, fgcolour\]\[, msg\]\[, msgs\]\[, transparent\]\[, size\])]{#symbol-Multiclick.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [blitToSurface(self)]{#symbol-Multiclick.blitToSurface}

Clears the background and renders the text label onto the button
surface.
:::

::: {.section}
#### [buildCaption(self, text)]{#symbol-Multiclick.buildCaption}

Pre-render the text to go on the button label.
:::

::: {.section}
#### [main(self)]{#symbol-Multiclick.main}

Main loop.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-Multiclick.waitBox}

Generator. yields 1 until data ready on the named inbox.
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
