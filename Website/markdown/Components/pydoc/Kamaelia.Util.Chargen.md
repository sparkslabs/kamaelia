---
pagename: Components/pydoc/Kamaelia.Util.Chargen
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chargen](/Components/pydoc/Kamaelia.Util.Chargen.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Chargen](/Components/pydoc/Kamaelia.Util.Chargen.Chargen.html){.reference}**
:::

-   [Simple Character Generator](#256){.reference}
    -   [Example Usage](#257){.reference}
    -   [How does it work?](#258){.reference}
:::

::: {.section}
Simple Character Generator {#256}
==========================

This component is intended as a simple \'stream of characters\'
generator.

At the moment, it continually sends the string \"Hello world\" as fast
as it can, indefinitely out of its \"outbox\" outbox.

::: {.section}
[Example Usage]{#example-usage} {#257}
-------------------------------

::

:   ``` {.first .doctest-block}
    >>> Pipeline( Chargen(), ConsoleEchoer() ).run()
    Hello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHel
    lo WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello
    WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello Wor
    ldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldH
    ello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHell
    ```

    \... you get the idea!
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#258}
--------------------------------------

This component, once activated repeatedly emits the string \"Hello
World\" from its \"outbox\" outbox. It is emitted as a single string. It
does this continuously forever. It is not rate limited in any way, and
so emits as fast as it can.

This component does not terminate, and ignores messages arriving at any
of its inboxes. It does not output anything from its \"signal\" outbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chargen](/Components/pydoc/Kamaelia.Util.Chargen.html){.reference}.[Chargen](/Components/pydoc/Kamaelia.Util.Chargen.Chargen.html){.reference}
================================================================================================================================================================================================================================================================

::: {.section}
class Chargen([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Chargen}
-----------------------------------------------------------------------------------------------

Chargen() -\> new Chargen component.

Component that emits a continuous stream of the string \"Hello World\"
from its \"outbox\" outbox as fast as it can.

::: {.section}
### [Inboxes]{#symbol-Chargen.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-Chargen.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
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
#### [main(self)]{#symbol-Chargen.main}

Main loop.
:::
:::

::: {.section}
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
