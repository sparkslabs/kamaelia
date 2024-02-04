---
pagename: Components/pydoc/Kamaelia.Util.OneShot
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[OneShot](/Components/pydoc/Kamaelia.Util.OneShot.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [OneShot](/Components/pydoc/Kamaelia.Util.OneShot.OneShot.html){.reference}**
-   **component
    [TriggeredOneShot](/Components/pydoc/Kamaelia.Util.OneShot.TriggeredOneShot.html){.reference}**
:::

-   [One-shot sending data](#210){.reference}
    -   [Example Usage](#211){.reference}
    -   [OneShot Behaviour](#212){.reference}
    -   [TriggeredOneShot Behaviour](#213){.reference}
:::

::: {.section}
One-shot sending data {#210}
=====================

OneShot and TriggeredOneShot send a single specified item to their
\"outbox\" outbox and immediately terminate.

TriggeredOneShot waits first for anything to arrive at its \"inbox\"
inbox, whereas OneShot acts as soon as it is activated.

::: {.section}
[Example Usage]{#example-usage} {#211}
-------------------------------

A way to create a component that writes data to a given filename, based
on (filename,data) messages sent to its \"next\" inbox:

``` {.literal-block}
Carousel( lambda filename, data :
            Pipeline( OneShot(data),
                      SimpleFileWriter(filename),
                    ),
        )
```

A graphline that opens a TCP connection to myserver.com port 1500, and
sends an a one off message:

``` {.literal-block}
Pipeline( OneShot("data to send to server"),
          TCPClient("myserver.com", 1500),
        ).run()
```

Shutting down a connection to myserver.com port 1500 as soon as a reply
is received from the server:

``` {.literal-block}
Graphline( NET   = TCPClient("myserver.com", 1500),
           SPLIT = TwoWaySplitter(),
           STOP  = TriggeredOneShot(producerFinished()),
           linkages = {
               ("", "inbox" )      : ("NET", "inbox"),
               ("NET", "outbox")   : ("SPLIT", "inbox"),
               ("SPLIT", "outbox") : ("", "outbox"),

               ("SPLIT", "outbox2") : ("STOP", "inbox"),
               ("STOP", "outbox")   : ("NET", "control"),
               ("", "control")      : ("NET", "control"),
               ("NET", "signal")    : ("SPLIT", "control"),
               ("SPLIT", "signal")  : ("", "signal"),
               ("SPLIT", "signal2"),: ("STOP", "control"),
           },
         )
```
:::

::: {.section}
[OneShot Behaviour]{#oneshot-behaviour} {#212}
---------------------------------------

At initialisation, specify the message to be sent by OneShot.

As soon as OneShot is activated, the specified message is sent out of
the \"outbox\" outbox. A producerFinished message is also sent out of
the \"signal\" outbox. The component then immediately terminates.
:::

::: {.section}
[TriggeredOneShot Behaviour]{#triggeredoneshot-behaviour} {#213}
---------------------------------------------------------

At initialisation, specify the message to be sent by TriggeredOneShot.

Send anything to the \"inbox\" inbox and TriggeredOneShot will
immediately send the specified message out of the \"outbox\" outbox. A
producerFinished message is also sent out of the \"signal\" outbox. The
component then immediately terminates.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[OneShot](/Components/pydoc/Kamaelia.Util.OneShot.html){.reference}.[OneShot](/Components/pydoc/Kamaelia.Util.OneShot.OneShot.html){.reference}
================================================================================================================================================================================================================================================================

::: {.section}
class OneShot([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-OneShot}
-----------------------------------------------------------------------------------------------

OneShot(msg) -\> new OneShot component.

Immediately sends the specified message and terminates.

Keyword arguments:

``` {.literal-block}
- msg  -- the message to send out
```

::: {.section}
### [Inboxes]{#symbol-OneShot.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-OneShot.Outboxes}

-   **outbox** : Item is sent out here
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
#### [\_\_init\_\_(self\[, msg\])]{#symbol-OneShot.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-OneShot.main}

Main loop
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[OneShot](/Components/pydoc/Kamaelia.Util.OneShot.html){.reference}.[TriggeredOneShot](/Components/pydoc/Kamaelia.Util.OneShot.TriggeredOneShot.html){.reference}
==================================================================================================================================================================================================================================================================================

::: {.section}
class TriggeredOneShot([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TriggeredOneShot}
--------------------------------------------------------------------------------------------------------

OneShot(msg) -\> new OneShot component.

Waits for anything to arrive at its \"inbox\" inbox, then immediately
sends the specified message and terminates.

Keyword arguments:

``` {.literal-block}
- msg  -- the message to send out
```

::: {.section}
### [Inboxes]{#symbol-TriggeredOneShot.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Anything, as trigger
:::

::: {.section}
### [Outboxes]{#symbol-TriggeredOneShot.Outboxes}

-   **outbox** : Item is sent out here
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
#### [\_\_init\_\_(self\[, msg\])]{#symbol-TriggeredOneShot.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-TriggeredOneShot.main}

Main loop
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
