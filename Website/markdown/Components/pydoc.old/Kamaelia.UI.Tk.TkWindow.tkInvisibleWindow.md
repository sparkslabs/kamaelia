---
pagename: Components/pydoc.old/Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow
=========================================

class tkInvisibleWindow(Kamaelia.UI.Tk.TkWindow.TkWindow)
---------------------------------------------------------

tkInvisibleWindow() -\> new tkInvisibleWindow component.

An invisible, empty tk window. Can use as a \'root\' window, thereby
ensuring closing any (visible) window doesn\'t terminate Tk (closing the
root does).

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

### setupWindow(self)

Sets up and hides the window.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
