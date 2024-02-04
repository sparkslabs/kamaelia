---
pagename: Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol.html){.reference}
========================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol.AudioCookieProtocol.html){.reference}**
:::

-   [Simple \"Audio fortune cookie\" Protocol Handler](#603){.reference}
    -   [Example Usage](#604){.reference}
    -   [How does it work?](#605){.reference}
:::

::: {.section}
Simple \"Audio fortune cookie\" Protocol Handler {#603}
================================================

A simple protocol handler that simply sends the contents of a randomly
chosen audio file to the client.

::: {.section}
[Example Usage]{#example-usage} {#604}
-------------------------------

::

:   ``` {.first .last .doctest-block}
    >>> SimpleServer(protocol=AudioCookieProtocol, port=1500).run()
    ```

On Linux client:
:   \> netcat \<server ip\> 1500 \| aplay -
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#605}
--------------------------------------

AudioCookieProtocol creates a ReadFileAdapter and configures it to read
the standard output result of running the afortune.pl script, at a fixed
rate of 95.2kbit/s.

afortune.pl randomly selects a file and returns its contents.

The ReadFileAdapter\'s \"outbox\" outbox is directly wired to pass
through to the \"outbox\" outbox of AudioCookieProtocol.

This component does not terminate.

No EOF/termination indication is given once the end of the file is
reached.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol.html){.reference}.[AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol.AudioCookieProtocol.html){.reference}
============================================================================================================================================================================================================================================================================================================================================

::: {.section}
class AudioCookieProtocol([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-AudioCookieProtocol}
-----------------------------------------------------------------------------------------------------------

AudioCookieProtocol(\[debug\]) -\> new AudioCookieProtocol component.

A protocol that spits out raw audio data from a randomly selected audio
file.

Keyword arguments:

-   debug \-- Debugging output control (default=0)

::: {.section}
### [Inboxes]{#symbol-AudioCookieProtocol.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-AudioCookieProtocol.Outboxes}

-   **outbox** : Raw audio data
-   **signal** : producerFinished() at end of data
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
#### [\_\_init\_\_(self\[, debug\])]{#symbol-AudioCookieProtocol.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-AudioCookieProtocol.initialiseComponent}

Initialises component. Sets up a ReadFileAdapter to read in the contents
of an audio file at 95.2kbit/s and wires it to fire the contents out
:::

::: {.section}
#### [mainBody(self)]{#symbol-AudioCookieProtocol.mainBody}

Main body - sits and waits, as ReadFileAdapter is getting on with the
work for us
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
