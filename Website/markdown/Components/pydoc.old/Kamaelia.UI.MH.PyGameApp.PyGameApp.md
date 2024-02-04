---
pagename: Components/pydoc.old/Kamaelia.UI.MH.PyGameApp.PyGameApp
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.MH.PyGameApp.PyGameApp
==================================

class PyGameApp(Axon.Component.component)
-----------------------------------------

PyGameApp(screensize\[,caption\]\[,transparency\]\[,position\]) -\> new
PyGameApp component.

Creates a PyGameApp component that obtains a pygame display surface and
provides an internal pygame event dispatch mechanism.

Subclass to implement your own pygame \"app\".

Keyword arguments: - screensize \-- (width,height) of the display area
(default = (800,600)) - caption \-- Caption for the pygame window
(default = \"Topology Viewer\") - fullscreen \-- True to start up in
fullscreen mode (default = False) - transparency \-- None, or (r,g,b)
colour to make transparent - position \-- None, or (left,top) position
for surface within pygame window

#### Inboxes

-   control : NOT USED
-   displaycontrol : Replies from PygameDisplay service
-   inbox : NOT USED
-   events : Event notifications from PygameDisplay service

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED
-   displaysignal : Requests to PygameDisplay service

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, screensize, caption, fullscreen, depth, transparency, position)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### \_dispatch(self)

Internal pygame event dispatcher.

For all events received, it calls all event handlers in sequence until
one returns True.

### addHandler(self, eventtype, handler)

Add an event handler, for a given PyGame event type.

The handler is passed the pygame event object as its argument when
called.

### events(self)

Generator. Receive events on \"events\" inbox and yield then one at a
time.

### go(self)

Call this to run the pygame app, without using an Axon scheduler.

> Returns when the app \'quits\'

### initialiseComponent(self)

### main(self)

Main loop. Do not override

### mainLoop(self)

Implement your runtime loop in this method here.

### quit(self, event)

Call this method/event handler to finish

### removeHandler(self, eventtype, handler)

Remove the specified pygame event handler from the specified event.

### waitBox(self, boxname)

Generator. Yields until data ready on the named inbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
