---
pagename: Components/pydoc.old/Kamaelia.UI.Tk.TkWindow.TkWindow
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Tk.TkWindow.TkWindow
================================

class TkWindow(Axon.Component.component)
----------------------------------------

TkWindow() -\> new TkWindow component

A component providing a Tk window. The first TkWindow created will be
the \"root\" window.

Subclass to implement your own widgets and functionality on the window.

#### Inboxes

-   control : Secondary inbox often used for signals. The closest
    analogy is unix signals
-   inbox : Default inbox for bulk data. Used in a pipeline much like
    stdin

#### Outboxes

-   outbox : Default data out outbox, used in a pipeline much like
    stdout
-   signal : The default signal based outbox - kinda like stderr, but
    more for sending singal type signals

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_TkWindow\_\_destroyHandler(self, event)

Handler for destroy event. Do not override.

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### destroyHandler(self, event)

Stub method. Reimplement with your own functionality to respond to a tk
window destroy event.

### isDestroyed(self)

Returns true if this window has been destroyed

### main(self)

Main loop. Stub method, reimplement with your own functionality.

Must regularly call self.tkupdate() to ensure tk event processing
happens.

### setupWindow(self)

Populate the window with widgets, set its title, set up event bindings
etc\...

Do not bind the \"\<Destroy\>\" event, as this is already handled.

Stub method. Reimplement with your own functionality.

### tkupdate(self)

Calls tk\'s event processing loop (if this is the root window).

To be called from within self.main().

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
