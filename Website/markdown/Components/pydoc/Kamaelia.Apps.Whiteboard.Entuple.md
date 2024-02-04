---
pagename: Components/pydoc/Kamaelia.Apps.Whiteboard.Entuple
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Whiteboard](/Components/pydoc/Kamaelia.Apps.Whiteboard.html){.reference}.[Entuple](/Components/pydoc/Kamaelia.Apps.Whiteboard.Entuple.html){.reference}
=========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [/](#53){.reference}
-   [Entuple data](#54){.reference}
    -   [Example Usage](#55){.reference}
    -   [How does it work?](#56){.reference}
:::

::: {.section}
::: {.section}
[/]{#id1} {#53}
---------
:::

::: {.section}
[Entuple data]{#entuple-data} {#54}
-----------------------------

Receives data on its \"inbox\" inbox; wraps that data inside a tuple,
and outputs that tuple from its \"outbox\" outbox.

::: {.section}
### [Example Usage]{#example-usage} {#55}

Taking console input and sandwiching it in a tuple between the strings
(\"You\" and \"said\") and (\"just\" and now\"):

``` {.literal-block}
Pipeline( ConsoleReader(),
          Entuple(prefix=["You","said"], postfix=["just","now"]),
          ConsoleEchoer(),
        ).run()
```

At runtime::

:   ``` {.first .last .doctest-block}
    >>> Hello there!
    ('You', 'said', 'Hello there!', 'just', 'now')
    ```
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#56}

At initialisation specify a list of items to be placed at the front
(prefix) and back (postfix) of the tuples that are output.

When an item of data is received at the \"inbox\" inbox; it is placed
inside a tuple, after the prefixes and before the postfixes. It is then
immediately sent out of the \"outbox\" outbox.

For example: if the prefix is \[1,2,3\] and the postfix is
\[\'a\',\'b\'\] and the item of data that arrives is \'flurble\' then
(1,2,3,\'flurble\',\'a\',\'b\') will be sent to the \"outbox\" outbox.

If Entuple receives a shutdownMicroprocess message on its \"control\"
inbox, it will pass it on out of the \"signal\" outbox. The component
will then terminate.
:::
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
