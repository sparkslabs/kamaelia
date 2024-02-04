---
pagename: Components/pydoc.old/Kamaelia.UI.PygameDisplay.PygameDisplay
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.PygameDisplay.PygameDisplay
=======================================

class PygameDisplay(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent)
-----------------------------------------------------------------------

PygameDisplay(\...) -\> new PygameDisplay component

Use PygameDisplay.getDisplayService(\...) in preference as it returns an
existing instance, or automatically creates a new one.

Or create your own and register it with setDisplayService(\...)

Keyword arguments (all optional): - width \-- pixels width (default=800)
- height \-- pixels height (default=600) - background\_colour \--
(r,g,b) background colour (default=(255,255,255)) - fullscreen \-- set
to True to start up fullscreen, not windowed (default=False)

#### Inboxes

-   control : NOT USED
-   inbox : Default inbox, not currently used
-   notify : Receive requests for surfaces, overlays and events

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### handleDisplayRequest(self)

Check \"notify\" inbox for requests for surfaces, events and overlays
and process them.

### main(self)

Main loop.

### surfacePosition(self, surface)

Returns a suggested position for a surface. No guarantees its any good!

### updateDisplay(self, display)

Render all surfaces and overlays onto the specified display surface.

Also dispatches events to event handlers.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
