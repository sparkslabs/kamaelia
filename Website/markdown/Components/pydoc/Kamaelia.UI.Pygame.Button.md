---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Button
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.html){.reference}
===================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.Button.html){.reference}**
:::

-   [Pygame Button Widget](#378){.reference}
    -   [Example Usage](#379){.reference}
    -   [How does it work?](#380){.reference}
:::

::: {.section}
Pygame Button Widget {#378}
====================

A button widget for pygame display surfaces. Sends a message when
clicked.

Uses the Pygame Display service.

::: {.section}
[Example Usage]{#example-usage} {#379}
-------------------------------

Three buttons that output messages to the console:

``` {.literal-block}
button1 = Button(caption="Press SPACE or click",key=K_SPACE).activate()
button2 = Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0)).activate()
button3 = Button(caption="Mary...",msg="Mary had a little lamb", position=(200,100)).activate()

ce = ConsoleEchoer().activate()
button1.link( (button1,"outbox"), (ce,"inbox") )
button2.link( (button2,"outbox"), (ce,"inbox") )
button3.link( (button3,"outbox"), (ce,"inbox") )
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#380}
--------------------------------------

The component requests a display surface from the Pygame Display service
component. This is used as the surface of the button. It also binds
event listeners to the service, as appropriate.

Arguments to the constructor configure the appearance and behaviour of
the button component:

-   If an output \"msg\" is not specified, the default is a tuple
    (\"CLICK\", id) where id is the self.id attribute of the component.
-   A pygame keycode can be specified that will also trigger the button
    as if it had been clicked
-   you can set the text label, colour, margin size and position of the
    button
-   the button can have a transparent background
-   you can specify a size as width,height. If specified, the margin
    size is ignored and the text label will be centred within the button

If a producerFinished or shutdownMicroprocess message is received on its
\"control\" inbox. It is passed on out of its \"signal\" outbox and the
component terminates.

Upon termination, this component does *not* unbind itself from the
Pygame Display service. It does not deregister event handlers and does
not relinquish the display surface it requested.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.html){.reference}.[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.Button.html){.reference}
=================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Button([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Button}
----------------------------------------------------------------------------------------------

Button(\...) -\> new Button component.

Create a button widget in pygame, using the Pygame Display service.
Sends a message out of its outbox when clicked.

Keyword arguments (all optional):

-   caption \-- text (default=\"Button \<component id\>\")
-   position \-- (x,y) position of top left corner in pixels
-   margin \-- pixels margin between caption and button edge (default=8)
-   bgcolour \-- (r,g,b) fill colour (default=(224,224,224))
-   fgcolour \-- (r,g,b) text colour (default=(0,0,0))
-   msg \-- sent when clicked (default=(\"CLICK\",self.id))
-   key \-- if not None, pygame keycode to trigger click (default=None)
-   transparent \-- draw background transparent if True (default=False)
-   size \-- None or (w,h) in pixels (default=None)

::: {.section}
### [Inboxes]{#symbol-Button.Inboxes}

-   **control** : For shutdown messages
-   **callback** : Receive callbacks from Pygame Display
-   **inbox** : Receive events from Pygame Display
:::

::: {.section}
### [Outboxes]{#symbol-Button.Outboxes}

-   **outbox** : button click events emitted here
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
#### [\_\_init\_\_(self\[, caption\]\[, position\]\[, margin\]\[, bgcolour\]\[, fgcolour\]\[, msg\]\[, key\]\[, transparent\]\[, size\])]{#symbol-Button.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [blitToSurface(self)]{#symbol-Button.blitToSurface}

Clears the background and renders the text label onto the button
surface.
:::

::: {.section}
#### [buildCaption(self, text)]{#symbol-Button.buildCaption}

Pre-render the text to go on the button label.
:::

::: {.section}
#### [main(self)]{#symbol-Button.main}

Main loop.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-Button.waitBox}

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
