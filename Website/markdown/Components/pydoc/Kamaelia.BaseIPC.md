---
pagename: Components/pydoc/Kamaelia.BaseIPC
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[BaseIPC](/Components/pydoc/Kamaelia.BaseIPC.html){.reference}
======================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [For example](#289){.reference}
:::

::: {.section}
Base IPC class. Subclass it to create your own IPC classes.

When doing so, make sure you set the following:

-   Its doc string, so a string explanation can be generated for an
    instance of your subclass.
-   \'Parameters\' class attribute to a list of named parameters you
    accept at creation, prefixing optional parameters with \"?\", e.g.
    \"?depth\"

::: {.section}
[For example]{#for-example} {#289}
---------------------------

A custom IPC class to report a theft taking place!

``` {.literal-block}
class Theft(Kamaelia.BaseIPC.IPC):
    """Something has been stolen!"""

    Parameters = ["?who","what"]
```

So what happens when we use it?

``` {.literal-block}
>>> ipc = Theft(who="Sam", what="sweeties")
>>> ipc.__doc__
'Something has been stolen!'
>>> ipc.who
'Sam'
>>> ipc.what
'sweeties'
```
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
