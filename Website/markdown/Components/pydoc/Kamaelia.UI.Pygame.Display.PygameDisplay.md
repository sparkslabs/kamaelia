---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Display.PygameDisplay
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Display](/Components/pydoc/Kamaelia.UI.Pygame.Display.html){.reference}.[PygameDisplay](/Components/pydoc/Kamaelia.UI.Pygame.Display.PygameDisplay.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Pygame.Display.html){.reference}

------------------------------------------------------------------------

::: {.section}
class PygameDisplay([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-PygameDisplay}
---------------------------------------------------------------------------------------------------------------------------------------------------------

PygameDisplay(\...) -\> new PygameDisplay component

Use PygameDisplay.getDisplayService(\...) in preference as it returns an
existing instance, or automatically creates a new one.

Or create your own and register it with setDisplayService(\...)

Keyword arguments (all optional):

-   width \-- pixels width (default=800)
-   height \-- pixels height (default=600)
-   background\_colour \-- (r,g,b) background colour
    (default=(255,255,255))
-   fullscreen \-- set to True to start up fullscreen, not windowed
    (default=False)

::: {.section}
### [Inboxes]{#symbol-PygameDisplay.Inboxes}

-   **control** : NOT USED
-   **events** : Receive events from source of pygame events
-   **inbox** : Default inbox, not currently used
-   **notify** : Receive requests for surfaces, overlays and events
:::

::: {.section}
### [Outboxes]{#symbol-PygameDisplay.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-PygameDisplay.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [handleDisplayRequest(self)]{#symbol-PygameDisplay.handleDisplayRequest}

Check \"notify\" inbox for requests for surfaces, events and overlays
and process them.
:::

::: {.section}
#### [handleEvents(self)]{#symbol-PygameDisplay.handleEvents}
:::

::: {.section}
#### [main(self)]{#symbol-PygameDisplay.main}

Main loop.
:::

::: {.section}
#### [surfacePosition(self, surface)]{#symbol-PygameDisplay.surfacePosition}

Returns a suggested position for a surface. No guarantees its any good!
:::

::: {.section}
#### [updateDisplay(self, display)]{#symbol-PygameDisplay.updateDisplay}

Render all surfaces and overlays onto the specified display surface.

Also dispatches events to event handlers.
:::

::: {.section}
#### [updateOverlays(self)]{#symbol-PygameDisplay.updateOverlays}
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
