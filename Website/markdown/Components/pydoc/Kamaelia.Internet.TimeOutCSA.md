---
pagename: Components/pydoc/Kamaelia.Internet.TimeOutCSA
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[TimeOutCSA](/Components/pydoc/Kamaelia.Internet.TimeOutCSA.html){.reference}
======================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [ResettableSender](#125){.reference}
    -   [Example Usage](#126){.reference}
    -   [More detail](#127){.reference}
-   [ActivityMonitor](#128){.reference}
    -   [Example Usage](#129){.reference}
    -   [Usage](#130){.reference}
    -   [More detail](#131){.reference}
:::

::: {.section}
This module provides a set of components and convienience functions for
making a CSA time out. To use it, simply call the function
InactivityChassis with a timeout period and the CSA to wrap. This will
send a producerFinished signal to the CSA if it does not send a message
on its outbox or CreatorFeedback boxes before the timeout expires.

::: {.section}
[ResettableSender]{#resettablesender} {#125}
-------------------------------------

This component is a simple way of makinga timeout event occur. If it
receives nothing after 5 seconds, a \"NEXT\" message is sent.

::: {.section}
### [Example Usage]{#example-usage} {#126}

A tcp client that connects to a given host and port and prints and
expects to receive *something* at more frequent than 5 seconds
intervals. If it does not, it prints a rude message the first time this
happens:

``` {.literal-block}
Pipeline(
    TCPClient(HOST, PORT),
    ResettableSender(),
    PureTransformer(lambda x : "Oi, wake up. I have received nothing for 5 seconds!"),
    ConsoleEchoer(),
    ).run()
```
:::

::: {.section}
### [More detail]{#more-detail} {#127}

By default, ResettableSender is set up to send a timeout message
\"NEXT\" out of its \"outbox\" outbox within 5 seconds. However, if it
receives any message on its \"inbox\" inbox then the timer is reset.

Once the timeout has occurred this component terminates. It will
therefore only ever generate one \"NEXT\" message, even if multiple
timeouts occur.

Termination is silent - no messages to indicate shutdown are sent out of
the \"signal\" outbox. This component ignores any input on its
\"control\" inbox - including shutdown messages.
:::
:::

::: {.section}
[ActivityMonitor]{#activitymonitor} {#128}
-----------------------------------

ActivityMonitor monitors up to four streams of messages passing through
it and, in response, sends messages out of its \"observed\" outbox to
indicate that there has been activity.

This is intended to wrap a component such that it may be monitored by
another component.

::: {.section}
### [Example Usage]{#id1} {#129}

Type a line at the console, and your activity will be \'observed\' - a
\'RESET\' message will appear as well as the line you have typed:

``` {.literal-block}
Graphline(
   MONITOR = ActivityMonitor(),
   OUTPUT  = ConsoleEchoer(),
   INPUT   = ConsoleReader(),
   linkages = {
       ("INPUT",   "outbox") : ("MONITOR", "inbox"),
       ("MONITOR", "outbox") : ("OUTPUT", "inbox"),

       ("MONITOR", "observed") : ("OUTPUT", "inbox"),
   }
).run()
```
:::

::: {.section}
### [Usage]{#usage} {#130}

To use it, connect any of the three inboxes to outboxes on the component
to be monitored.

The messages that are sent to those inboxes will be forwarded to their
respective outbox. For example, suppose \"HELLO\" was received on
\'inbox2\'. self.message (\"RESET\" by default) will be sent on the
\'observed\' outbox and \"HELLO\" will be sent out on \'outbox2\'.

ActivityMonitor will shut down upon receiving a producerFinished or
shutdownCSA message on its control inbox.

Please note that this can\'t wrap adaptive components properly as of
yet.
:::

::: {.section}
### [More detail]{#id2} {#131}

Any message sent to the \"inbox\", \"inbox2\", \"inbox3\" or \"control\"
inboxes are immediately forwarded on out of the \"outbox\", \"outbox2\",
\"outbox3\" or \"signal\" outboxes respectively.

Whenever this happens, a \"RESET\" message (the default) is sent out of
the \"observed\" outbox.

For every batch of messages waiting at the three inboxes that get
forwarded on out of their respective outboxes, *only one* \"RESET\"
message will be sent. This should therefore only be used as a general
indication of activity, not as a means of counting every individual
message passing through this component.

Any message sent to the \"control\" inbox is also checked to see if it
is a shutdownCSA or producerFinished message. If it is one of these then
it will still be forwarded on out of the \"signal\" outbox, but will
also cause ActivityMonitor to immediately terminate.

Any messages waiting at any of the inboxes (including the \"control\"
inbox) at the time the shutdown triggering message is received will be
sent on before termination.
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
