---
pagename: Components/pydoc/Kamaelia.UI.Tk.TkWindow.TkWindow
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Tk](/Components/pydoc/Kamaelia.UI.Tk.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.TkWindow.html){.reference}
===========================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}

------------------------------------------------------------------------

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
