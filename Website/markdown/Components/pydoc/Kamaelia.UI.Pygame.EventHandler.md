---
pagename: Components/pydoc/Kamaelia.UI.Pygame.EventHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[EventHandler](/Components/pydoc/Kamaelia.UI.Pygame.EventHandler.html){.reference}
===============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Pygame event handling](#364){.reference}
    -   [Example Usage](#365){.reference}
    -   [How does it work?](#366){.reference}
:::

::: {.section}
Pygame event handling {#364}
=====================

A simple framework for handling pygame events. Reimplement the
appropriate stub method to handle a given event.

::: {.section}
[Example Usage]{#example-usage} {#365}
-------------------------------

Detecting key presses and mouse button depressions and releases::

:   

    class MyEventHandler(EventHandler):

    :   

        def \_\_init\_\_(self, target):
        :   super(MyEventHandler,self).\_\_init\_\_() self.target =
            target

        def keydown(self, key, mod, where):
        :   print \"Keypress \'\"+key+\"\' detected by \"+where

        def mousebuttondown(self, pos, button, where):
        :   print \"Mouse button depressed\"

        def mousebuttonup(self, pos, button, where):
        :   print \"Mouse button released\"
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#366}
--------------------------------------

Implement your event handler by subclassing EventHandler and
reimplementing the stub methods for the particular events you wish to
handle.

The code that reads the events from pygame should pass them one at a
time to EventHandler by calling the dispatch(\...) method.

The optional \'trace\' argument to the initialiser, when non-zero,
causes the existing stub handlers to print messages to standard out,
notifying you that the given event has taken place.
:::
:::

------------------------------------------------------------------------

::: {.section}
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
