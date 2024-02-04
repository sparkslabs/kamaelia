---
pagename: Components/pydoc/Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Tk](/Components/pydoc/Kamaelia.UI.Tk.html){.reference}.[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}.[tkInvisibleWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}

------------------------------------------------------------------------

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
