---
pagename: Components/pydoc/Kamaelia.Util.Console
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Console](/Components/pydoc/Kamaelia.Util.Console.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ConsoleEchoer](/Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer.html){.reference}**
-   **component
    [ConsoleReader](/Components/pydoc/Kamaelia.Util.Console.ConsoleReader.html){.reference}**
:::

-   [Console Input/Output](#149){.reference}
    -   [Example Usage](#150){.reference}
    -   [How does it work?](#151){.reference}
:::

::: {.section}
Console Input/Output {#149}
====================

The ConsoleEchoer component outputs whatever it receives to the console.

The ConsoleReader component outputs whatever is typed at the console, a
line at a time.

::: {.section}
[Example Usage]{#example-usage} {#150}
-------------------------------

Whatever it typed is echoed back, a line at a time:

``` {.literal-block}
Pipeline( ConsoleReader(),
          ConsoleEchoer()
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#151}
--------------------------------------

ConsoleReader is a threaded component. It provides a \'prompt\' at which
you can type. Your input is taken, a line a a time, and output to its
\"outbox\" outbox, with the specified end-of-line character(s) suffixed
onto it.

The ConsoleReader component ignores any input on its \"inbox\" and
\"control\" inboxes. It does not output anything from its \"signal\"
outbox.

The ConsoleReader component does not terminate.

The ConsoleEchoer component receives data on its \"inbox\" inbox.
Anything it receives this way is displayed on standard output. All items
are passed through the str() builtin function to convert them to strings
suitable for display.

However, if the \'use\_repr\' argument is set to True during
initialization, then repr() will be used instead of str(). Similarly if
a \"tag\" is provided it\'s prepended before the data.

If the \'forwarder\' argument is set to True during initialisation, then
whatever is received is not only displayed, but also set on to the
\"outbox\" outbox (unchanged).

If a producerFinished or shutdownMicroprocess message is received on the
ConsoleEchoer component\'s \"control\" inbox, then it is sent on to the
\"signal\" outbox and the component then terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Console](/Components/pydoc/Kamaelia.Util.Console.html){.reference}.[ConsoleEchoer](/Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer.html){.reference}
============================================================================================================================================================================================================================================================================

::: {.section}
class ConsoleEchoer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ConsoleEchoer}
-----------------------------------------------------------------------------------------------------

ConsoleEchoer(\[forwarder\]\[,use\_repr\]\[,tag\]) -\> new ConsoleEchoer
component.

A component that outputs anything it is sent to standard output (the
console).

Keyword arguments:

-   forwarder \-- incoming data is also forwarded to \"outbox\" outbox
    if True (default=False)
-   use\_repr \-- use repr() instead of str() if True (default=False)
-   tag \-- Pre-pend this text tag before the data to emit

::: {.section}
### [Inboxes]{#symbol-ConsoleEchoer.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Stuff that will be echoed to standard output
:::

::: {.section}
### [Outboxes]{#symbol-ConsoleEchoer.Outboxes}

-   **outbox** : Stuff forwarded from \'inbox\' inbox (if enabled)
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
#### [\_\_init\_\_(self\[, forwarder\]\[, use\_repr\]\[, tag\])]{#symbol-ConsoleEchoer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-ConsoleEchoer.main}

Main loop body.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ConsoleEchoer.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Console](/Components/pydoc/Kamaelia.Util.Console.html){.reference}.[ConsoleReader](/Components/pydoc/Kamaelia.Util.Console.ConsoleReader.html){.reference}
============================================================================================================================================================================================================================================================================

::: {.section}
class ConsoleReader([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-ConsoleReader}
-------------------------------------------------------------------------------------------------------------------------------------

ConsoleReader(\[prompt\]\[,eol\]) -\> new ConsoleReader component.

Component that provides a console for typing in stuff. Each line is
output from the \"outbox\" outbox one at a time.

Keyword arguments:

-   prompt \-- Command prompt (default=\"\>\>\> \")
-   eol \-- End of line character(s) to put on end of every line
    outputted (default is newline)

::: {.section}
### [Inboxes]{#symbol-ConsoleReader.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-ConsoleReader.Outboxes}

-   **outbox** : Lines that were typed at the console
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
#### [\_\_init\_\_(self\[, prompt\]\[, eol\])]{#symbol-ConsoleReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-ConsoleReader.main}

Main thread loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ConsoleReader.shutdown}
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
