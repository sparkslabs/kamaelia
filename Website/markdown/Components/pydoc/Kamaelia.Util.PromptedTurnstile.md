---
pagename: Components/pydoc/Kamaelia.Util.PromptedTurnstile
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.html){.reference}
========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.PromptedTurnstile.html){.reference}**
:::

-   [Buffering of data items until requested one at a
    time](#217){.reference}
    -   [Example Usage](#218){.reference}
    -   [Behaviour](#219){.reference}
:::

::: {.section}
Buffering of data items until requested one at a time {#217}
=====================================================

PromptedTurnstile buffers items received, then sends them out one at a
time in response to requests, first-in first-out style.

This is useful for controlling or limiting the rate of flow of data.

::: {.section}
[Example Usage]{#example-usage} {#218}
-------------------------------

Displaying a script from a file, one line at a time, when a pygame
button is clicked:

``` {.literal-block}
Graphline(
    SOURCE = RateControlledFileReader("script.txt",readmode="lines", ...),
    GATE   = PromptedTurnstile(),
    SINK   = ConsoleEchoer(),
    NEXT   = Button(label="Click for next line of script"),
    linkages = {
        ("SOURCE", "outbox") : ("GATE", "inbox"),
        ("GATE",   "outbox") : ("SINK", "inbox"),
        ("NEXT",   "outbox") : ("GATE", "next"),

        ("SOURCE", "signal") : ("GATE", "control"),
        ("GATE",   "signal") : ("SINK", "control"),
        ("SINK",   "signal") : ("NEXT", "control"),
        }
    )
```
:::

::: {.section}
[Behaviour]{#behaviour} {#219}
-----------------------

Send items to the \"inbox\" inbox where they will queue up. Then each
time you send anything to the \"next\" inbox; one item will be taken
from the queue and forwarded out of the \"outbox\" outbox.

Think of it like a turnstile gate with people queuing up for it. Each
message sent to the \"next\" inbox is a signal to let one person through
the turnstile.

This component supports sending data out of its outbox to a size limited
inbox. If the size limited inbox is full, this component will pause
until it is able to send out the data. Data will not be consumed from
the inbox if this component is waiting to send to the outbox.

If there is a backlog of \"next\" requests (because there is nothing
left in the buffer) those items will be sent out as soon as they arrive.
There is no need to send another \"next\" request.

Send a producerFinished message to the \"control\" inbox to tell
PromptedTurnstile that there will be no more data. When prompted
turnstile then receives a \"next\" request and has nothing left queued,
it will send a producerFinised() message to its \"signal\" outbox and
immediately terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox.
It is immediately sent on out of the \"signal\" outbox and the component
then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.html){.reference}.[PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.PromptedTurnstile.html){.reference}
==================================================================================================================================================================================================================================================================================================================

::: {.section}
class PromptedTurnstile([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PromptedTurnstile}
---------------------------------------------------------------------------------------------------------

PromptedTurnstile() -\> new PromptedTurnstile component.

Buffers all items sent to its \"inbox\" inbox, and only sends them out,
one at a time when requested.

::: {.section}
### [Inboxes]{#symbol-PromptedTurnstile.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
-   **next** : Requests to send out items
:::

::: {.section}
### [Outboxes]{#symbol-PromptedTurnstile.Outboxes}

-   **outbox** : Data items
-   **signal** : Shutdown signalling
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
#### [checkShutdown(self)]{#symbol-PromptedTurnstile.checkShutdown}
:::

::: {.section}
#### [main(self)]{#symbol-PromptedTurnstile.main}
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
