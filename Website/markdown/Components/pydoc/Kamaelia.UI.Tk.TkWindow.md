---
pagename: Components/pydoc/Kamaelia.UI.Tk.TkWindow
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Tk](/Components/pydoc/Kamaelia.UI.Tk.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}
===========================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.TkWindow.html){.reference}**
-   **component
    [tkInvisibleWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow.html){.reference}**
:::

-   [Simple Tk Window base class](#359){.reference}
    -   [Example Usage](#360){.reference}
    -   [How does it work?](#361){.reference}
    -   [Development History](#362){.reference}
:::

::: {.section}
Simple Tk Window base class {#359}
===========================

A simple component providing a framework for having a Tk window as a
component.

TkInvisibleWindow is a simple implementation of an invisible (hidden) Tk
window, useful if you want none of the visible windows to be the Tk root
window.

::: {.section}
[Example Usage]{#example-usage} {#360}
-------------------------------

Three Tk windows, one with \"Hello world\" written in it::

:   

    class MyWindow(TkWindow):

    :   

        def \_\_init\_\_(self, title, text):
        :   self.title = title self.text = text
            super(MyWindow,self).\_\_init\_\_()

        def setupWindow(self):

        :   self.label = Tkinter.Label(self.window, text=self.text)

            self.window.title(self.title)

            self.label.grid(row=0, column=0,
            sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
            self.window.rowconfigure(0, weight=1)
            self.window.columnconfigure(0, weight=1)

    root = TkWindow().activate() \# first window created is the root
    win2 = MyWindow(\"MyWindow\",\"Hello world!\").activate()

    scheduler.run.runThreads(slowmo=0)
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#361}
--------------------------------------

This component provides basic integration for Tk. It creates and sets up
a Tk window widget, and then provides a kamaelia main loop that ensures
Tk\'s own event processing loop is regularly called.

self.window contains the Tk window widget.

To set up your own widgets and event handling bindings for the window,
reimplement the setupWindow() method.

NOTE: Do not bind the \"\<Destroy\>\" event as this is already handled.
Instead, reimplement the destroyHandler() method. This is guaranteed to
only be called if the destroy event is for this specific window.

The first window instantiated is the Tk \"root\" window. Note that
closing this window will result in Tk trying to close down. To avoid
this style of behaviour, create a TkInvisibleWindow as the root.

The existing main() method ensures Tk\'s event processing loop is
regularly called.

You can reimplement main(). However, you must ensure you include the
existing functionality: - regularly calling tkupdate() to ensure Tk gets
to process its own events - calls self.window.destroy() method to
destroy the window upon shutdown. - finishes if self.isDestroyed()
returns True

The existing main() method will cause the component to terminate if a
producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It sends the message on out of the \"signal\" outbox
and calls self.window.destroy() to ensure the window is destroyed.

NOTE: main() must not ask to be paused as it calls the Tk event loop. If
the Tk event loop is not called, then a Tk app will freeze and be unable
to respond to events.

NOTE: Event bindings are called from within Tk event handling. If, for
example, there are two (or more) TkWindow instances, then a given event
handler could be called whilst the thread of execution is actually
within the other TkWindow component\'s main() method. This is a bit
messy. It will not cause problems in a single threaded system, but may
be an issue once [Axon](/Docs/Axon/Axon.html){.reference}/Kamaelia is
able to distribute across multiple processors.
:::

::: {.section}
[Development History]{#development-history} {#362}
-------------------------------------------

Started as a first hash attempt at some components to incorporate
Tkinter into Kamaelia in cvs:/Sketches/tk/tkInterComponents.py

Turned out to be remarkably resilient so far, so migrated into the main
codebase.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Tk](/Components/pydoc/Kamaelia.UI.Tk.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.TkWindow.html){.reference}
===========================================================================================================================================================================================================================================================================================================================

::: {.section}
class TkWindow([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TkWindow}
------------------------------------------------------------------------------------------------

TkWindow() -\> new TkWindow component

A component providing a Tk window. The first TkWindow created will be
the \"root\" window.

Subclass to implement your own widgets and functionality on the window.

::: {.section}
### [Inboxes]{#symbol-TkWindow.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-TkWindow.Outboxes}
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
#### [\_\_destroyHandler(self, event)]{#symbol-TkWindow.__destroyHandler}

Handler for destroy event. Do not override.
:::

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-TkWindow.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [destroyHandler(self, event)]{#symbol-TkWindow.destroyHandler}

Stub method. Reimplement with your own functionality to respond to a tk
window destroy event.
:::

::: {.section}
#### [isDestroyed(self)]{#symbol-TkWindow.isDestroyed}

Returns true if this window has been destroyed
:::

::: {.section}
#### [main(self)]{#symbol-TkWindow.main}

Main loop. Stub method, reimplement with your own functionality.

Must regularly call self.tkupdate() to ensure tk event processing
happens.
:::

::: {.section}
#### [setupWindow(self)]{#symbol-TkWindow.setupWindow}

Populate the window with widgets, set its title, set up event bindings
etc\...

Do not bind the \"\<Destroy\>\" event, as this is already handled.

Stub method. Reimplement with your own functionality.
:::

::: {.section}
#### [tkupdate(self)]{#symbol-TkWindow.tkupdate}

Calls tk\'s event processing loop (if this is the root window).

To be called from within self.main().
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Tk](/Components/pydoc/Kamaelia.UI.Tk.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}.[tkInvisibleWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================

::: {.section}
class tkInvisibleWindow(TkWindow) {#symbol-tkInvisibleWindow}
---------------------------------

tkInvisibleWindow() -\> new tkInvisibleWindow component.

An invisible, empty tk window. Can use as a \'root\' window, thereby
ensuring closing any (visible) window doesn\'t terminate Tk (closing the
root does).

::: {.section}
### [Inboxes]{#symbol-tkInvisibleWindow.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-tkInvisibleWindow.Outboxes}
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
#### [setupWindow(self)]{#symbol-tkInvisibleWindow.setupWindow}

Sets up and hides the window.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.UI.Tk.TkWindow.TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.TkWindow.html){.reference} :

-   [\_\_destroyHandler](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html#symbol-TkWindow.__destroyHandler){.reference}(self,
    event)
-   [tkupdate](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html#symbol-TkWindow.tkupdate){.reference}(self)
-   [destroyHandler](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html#symbol-TkWindow.destroyHandler){.reference}(self,
    event)
-   [isDestroyed](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html#symbol-TkWindow.isDestroyed){.reference}(self)
-   [main](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html#symbol-TkWindow.main){.reference}(self)
-   [\_\_init\_\_](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html#symbol-TkWindow.__init__){.reference}(self)
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
