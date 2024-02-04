---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Display
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Display](/Components/pydoc/Kamaelia.UI.Pygame.Display.html){.reference}
=====================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PygameDisplay](/Components/pydoc/Kamaelia.UI.Pygame.Display.PygameDisplay.html){.reference}**
:::

-   [Pygame Display Access](#392){.reference}
    -   [Example Usage](#393){.reference}
    -   [How does it work?](#394){.reference}
        -   [Surfaces](#395){.reference}
        -   [Listening to events](#396){.reference}
        -   [Video Overlays](#397){.reference}
        -   [Redraw requests](#398){.reference}
    -   [Implementation Details](#399){.reference}
:::

::: {.section}
Pygame Display Access {#392}
=====================

This component provides a pygame window. Other components can request to
be notified of events, or ask for a pygame surface or video overlay that
will be rendered onto the display.

Pygame Display is a service that registers with the Coordinating
Assistant Tracker (CAT).

::: {.section}
[Example Usage]{#example-usage} {#393}
-------------------------------

See the Button component or VideoOverlay component for examples of how
Pygame Display can be used.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#394}
--------------------------------------

Pygame Display is a service. obtain it by calling the
PygameDisplay.getDisplayService(\...) static method. Any existing
instance will be returned, otherwise a new one is automatically created.

Alternatively, if you wish to configure Pygame Display with options
other than the defaults, create your own instance, then register it as a
service by calling the PygameDisplay.setDisplayService(\...) static
method. NOTE that it is only advisable to do this at the top level of
your system, as other components may have already requested and created
a Pygame Display component!

pygame only supports one display window at a time, you must not make
more than one Pygame Display component.

Pygame Display listens for requests arriving at its \"notify\" inbox. A
request can be to: - create or destroy a surface, - listen or stop
listening to events (you must have already requested a surface) - move
an existing surface - create a video overlay - notify of ne to redraw

The requests are described in more detail below.

Once your component has been given the requested surface, it is free to
render onto it whenever it wishes. It should then immediately send a
\"REDRAW\" request to notify Pygame Display that the window needs
redrawing.

NOTE that you must set the alpha value of the surface before rendering
and restore its previous value before yielding. This is because Pygame
Display uses the alpha value to control the transparency with which it
renders the surface.

Overlays work differently: instead of being given something to render
to, you must provide, in your initial request, an outbox to which you
will send raw yuv (video) data, whenever you want to change the image on
the overlay.

Pygame Display instantiates a private, threaded component to listen for
pygame events. These are then forwarded onto Pygame Display.

Pygame Display\'s main loop continuously renders the surfaces and video
overlays onto the display, and dispatches any pygame events to
listeners. The rendering order is as follows: - background fill
(default=white) - surfaces (in the order they were requested and
created) - video overlays (in the order they were requested and created)

In summary, to use a surface, your component should: 1. Obtain and wire
up to the \"notify\" inbox of the Pygame Display service 2. Request a
surface 3. Render onto that surface in its main loop

And to use overlays, your component should: 1. Obtain and wire up to the
\"notify\" inbox of the Pygame Display service 2. Request an overlay,
providing an outbox 3. Send yuv data to the outbox

This component does not terminate. It ignores any messages arriving at
its \"control\" inbox and does not send anything out of its \"outbox\"
or \"signal\" outboxes.

::: {.section}
### [Surfaces]{#surfaces} {#395}

To request a surface, send a dictionary to the \"notify\" inbox. The
following keys are mandatory:

``` {.literal-block}
{
    "DISPLAYREQUEST" : True,               # this is a 'new surface' request
    "size" : (width,height),               # pixels size for the new surface
    "callback" : (component, "inboxname")  # to send the new surface object to
}
```

These keys are optional:

``` {.literal-block}
{
    "position" : (left,top)                # location of the new surface in the window (default=arbitrary)
    "alpha" : 0 to 255,                    # alpha of the surface (255=opaque) (default=255)
    "transparency" : (r,g,b),              # colour that will appear transparent (default=None)
    "events" : (component, "inboxname"),   # to send event notification to (default=None)
}
```

To deregister your surface, send a producerFinished(surface) message to
the \"notify\" inbox. Where \'surface\' is your surface. This will
remove your surface and deregister any events you were listening to.

To change the position your surface is rendered at, send a dictionary to
the \"notify\" inbox containing the folling keys:

``` {.literal-block}
{
    "CHANGEDISPLAYGEO" : True,             # this is a 'change geometry' request
    "surface" : surface,                   # the surface to affect
    "position" : (left,top)                # new location for the surface in the window
}
```

The \"surface\" and \"position\" keys are optional. However if either
are not specified then there will be no effect!
:::

::: {.section}
### [Listening to events]{#listening-to-events} {#396}

Once your component has obtained a surface, it can request to be
notified of specific pygame events.

To request to listen to a given event, send a dictionary to the
\"notify\" inbox, containing the following:

``` {.literal-block}
{
    "ADDLISTENEVENT" : pygame_eventtype,     # example: pygame.KEYDOWN
    "surface" : your_surface,
}
```

To unsubscribe from a given event, send a dictionary containing:

``` {.literal-block}
{
    "REMOVELISTENEVENT" : pygame_eventtype,
    "surface" : your_surface,
}
```

Events will be sent to the inbox specified in the \"events\" key of the
\"DISPLAYREQUEST\" message. They arrive as a list of pygame event
objects.

NOTE: If the event is MOUSEMOTION, MOUSEBUTTONUP or MOUSEBUTTONDOWN then
you will instead receive a replacement object, with the same attributes
as the pygame event, but with the \'pos\' attribute adjusted so that
(0,0) is the top left corner of *your* surface.
:::

::: {.section}
### [Video Overlays]{#video-overlays} {#397}

To request an overlay, send a dictionary to the \"notify\" inbox. The
following keys are mandatory:

``` {.literal-block}
{
    "OVERLAYREQUEST" : True,                      # this is a 'new overlay' request
    "size" : (width,height),                      # pixels size of the overlay
    "pixformat" : pygame_pixformat,               # example: pygame.IYUV_OVERLAY
}
```

These keys are optional:

``` {.literal-block}
{
    "position" : (left,top),                      # location of the overlay (default=(0,0))
    "yuv" : (ydata,udata,vdata),                  # first frame of yuv data
    "yuvservice" : (component,"outboxname"),      # source of future frames of yuv data
    "positionservice" : (component,"outboxname"), # source of changes to the overlay position
}
```

\"yuv\" enables you to provide the first frame of video data. It should
be 3 strings, containing the yuv data for a whole frame.

If you have supplied a (component,outbox) pair as a \"yuvservice\" then
any (y,u,v) data sent to that outbox will update the video overlay.
Again the data should be 3 strings, containing the yuv data for a *whole
frame*.

If you have supplied a \"positionservice\", then sending (x,y) pairs to
the outbox you specified will update the position of the overlay.

There is currently no mechanism to destroy an overlay.
:::

::: {.section}
### [Redraw requests]{#redraw-requests} {#398}

To notify Pygame Display that it needs to redraw the display, send a
dictionary containing the following keys to the \"notify\" inbox:

``` {.literal-block}
{
    "REDRAW" : True,             # this is a redraw request
    "surface" : surface          # surface that has been changed
}
```
:::
:::

::: {.section}
[Implementation Details]{#implementation-details} {#399}
-------------------------------------------------

You may notice that this module also contains a \_PygameEventSource
component. PygameDisplay uses this separate threaded component to notify
it when pygame events occur - so that it can sleep quiescently when it
has nothing to do.

Unfortunately event handling itself cannot be done in the thread since
pygame on many platforms (particularly win32) does not work properly if
event handling and display creation is not done in the main thread of
the program.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Display](/Components/pydoc/Kamaelia.UI.Pygame.Display.html){.reference}.[PygameDisplay](/Components/pydoc/Kamaelia.UI.Pygame.Display.PygameDisplay.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================

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
