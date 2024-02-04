---
pagename: Components/pydoc/Kamaelia.Device.DVB.Tuner
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.html){.reference}
========================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.Tuner.html){.reference}**
:::

-   [DVB-T (Digital Terrestrial TV) Tuner](#528){.reference}
    -   [Example Usage](#529){.reference}
    -   [How does it work?](#530){.reference}
        -   [Tuning parameters](#531){.reference}
:::

::: {.section}
DVB-T (Digital Terrestrial TV) Tuner {#528}
====================================

Tunes to the specified frequency, using the specified parameters, using
a DVB tuner device; then outputs packets from the received MPEG
transport stream as requested.

::: {.section}
[Example Usage]{#example-usage} {#529}
-------------------------------

Record entire received MPEG transport stream, from a particular
frequency and set of tuning parameters to file:

``` {.literal-block}
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline( OneShot( msg=["ADD", [0x2000] ] ),    # send the msg ["ADD", [0x2000]]
          Tuner(537.833330, feparams),
          SimpleFileWriter("dump.ts"),
        ).run()
```

Record just packets with packet ID (PID) 0 and 18:

``` {.literal-block}
Pipeline( OneShot( msg=["ADD", [0, 18] ] ),
          Tuner(537833330.0, feparams),
          SimpleFileWriter("dump.ts"),
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#530}
--------------------------------------

Tuner tunes, using the specified tuning parameters to a DVB-T
transmitted multiplex. You can also specify which DVB tuner card
(device) to use if there is more than one in your system.

To start with it outputs nothing. To start or stop outputting packets,
send messages to the \"inbox\" inbox of the form:

``` {.literal-block}
[ "ADD",    [pid, pid, ...] ]
[ "REMOVE", [pid, pid, ...] ]
```

These instruct Tuner to output packets from the received multiplex with
the specified packet IDs (PIDs).

Most DVB tuner devices understand a special packet ID of 0x2000 to
request the entire transport stream of all packets with all IDs.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.

::: {.section}
### [Tuning parameters]{#tuning-parameters} {#531}

The tuning parameters come from the dvb3.frontend library. Specify them
as a dictionary:

``` {.literal-block}
{
     "bandwidth"             : dvb3.frontend.BANDWIDTH_?_MHZ where ? is 6, 7 or 8
     "constellation"         : dvb3.frontend.QPSK, QAM_16 or QAM_64
     "hierarchy_information" : dvb3.frontend.HIERARCHY_? where ? is NONE, 1, 2 or 4
     "code_rate_HP"          : dvb3.frontend.FEC_X_Y where X/Y = 1/2, 2/3, 3/4, 5/6, 7/8
     "code_rate_LP"          : dvb3.frontend.FEC_X_Y where X/Y = 1/2, 2/3, 3/4, 5/6, 7/8
     "guard_interval"        : dvb3.frontend.GUARD_INTERVAL_1_? where ? is 32, 16, 8 or 4
     "transmission_mode"     : dvb3.frontend.TRANSMISSION_MODE_?K where ? is 2 or 8
     "inversion"             : dvb3.frontend.INVERSION_AUTO
}
```
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.html){.reference}.[Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.Tuner.html){.reference}
====================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Tuner([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-Tuner}
-----------------------------------------------------------------------------------------------------------------------------

Tuner(freq\[,feparams\]\[,card\]) -\> new Tuner component.

Tunes the DVB-T card to the given frequency with the given parameters.
Send (ADD, \[PID list\]) or (REMOVE, \[PID list\]) messages to its
\"inbox\" inbox to cuase it to output MPEG transport stream packets
(with the specified PIDs) from its \"outbox\" outbox.

Keyword arguments:

-   freq \-- Frequency to tune to in MHz
-   feparams \-- Dictionary of parameters for the tuner front end
    (default={})
-   card \-- Which DVB device to use (default=0)

::: {.section}
### [Inboxes]{#symbol-Tuner.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Tuner.Outboxes}
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
#### [\_\_init\_\_(self, freq\[, feparams\]\[, card\])]{#symbol-Tuner.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addPID(self, pid)]{#symbol-Tuner.addPID}

Adds the given PID to the transport stream that will be available in
\"/dev/dvb/adapter0/dvr0\"
:::

::: {.section}
#### [handleCommand(self, cmd, demuxers)]{#symbol-Tuner.handleCommand}
:::

::: {.section}
#### [main(self)]{#symbol-Tuner.main}
:::

::: {.section}
#### [notLocked(self)]{#symbol-Tuner.notLocked}

Returns True if the frontend is not yet locked. Returns False if it is
locked.
:::

::: {.section}
#### [shutdown(self)]{#symbol-Tuner.shutdown}
:::

::: {.section}
#### [tune\_DVB(self, frequency\[, feparams\])]{#symbol-Tuner.tune_DVB}
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
