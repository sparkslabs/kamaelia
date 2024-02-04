---
pagename: Docs/Axon/Axon.Ipc.notify
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[notify](/Docs/Axon/Axon.Ipc.notify.html){.reference}
------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class notify(ipc) {#symbol-notify}
-----------------

::: {.section}
notify(caller,payload) -\> new notify ipc message.

Message used to notify the system of an event. Subclass to implement
your own specific notification messages.

Keyword arguments:

-   caller \-- a reference to whoever/whatever issued this notification.
    Assigned to self.caller
-   payload \-- any relevant payload relating to the notification.
    Assigned to self.object
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, caller, payload)]{#symbol-notify.__init__}
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
