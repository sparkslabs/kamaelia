---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.html){.reference}
==========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.AIMHarness.html){.reference}**
:::

-   [AIM Harness](#623){.reference}
    -   [Example Usage](#624){.reference}
    -   [How it works](#625){.reference}
    -   [Known issues](#626){.reference}
:::

::: {.section}
AIM Harness {#623}
===========

Provides a high-level Kamaelia interface to AIM.

For a Kamaelia interface at the FLAP and SNAC levels, see OSCARClient.py

::: {.section}
[Example Usage]{#example-usage} {#624}
-------------------------------

A simple command-line client with a truly horrible interface:

``` {.literal-block}
def tuplefy(data):
    data = data.split()
    if len(data) > 1:
        data = ("message", data[0], " ".join(data[1:]))
        return data

Pipeline(ConsoleReader(),
         PureTransformer(tuplefy),
         AIMHarness(),
         ConsoleEchoer()
        ).run()
```
:::

::: {.section}
[How it works]{#how-it-works} {#625}
-----------------------------

AIMHarness ties LoginHandler and ChatManager together. First it
initializes a LoginHandler, waits for it to send out a logged-in
OSCARClient, then wires up a ChatManager to the OSCARClient. It wires up
its \"inbox\" to ChatManager\'s \"talk\", and ChatManager\'s \"heard\"
to \"outbox\".

Once everything is up and functioning, the AIMHarness will stay running
to act as an intermediary to pass messages between the OSCARClient and
the ChatManager, but the AIMHarness will not act upon any of the
information other than to pass it.

To send an instant message to another user, send the command
(\"message\", recipient, text of the message) to its \"inbox\".

AIMHarness will send out the following notifications through its
\"outbox\":

  -----------------------------------------------------------------------
  NOTIFICATION                         EVENT
  ------------------------------------ ----------------------------------
  (\"buddy online\", {buddy            A buddy comes online
  information})                        

  (\"message\", sender, message text)  An instant message arrives for you
  -----------------------------------------------------------------------
:::

::: {.section}
[Known issues]{#known-issues} {#626}
-----------------------------

This component does not terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.html){.reference}.[AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.AIMHarness.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class AIMHarness([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-AIMHarness}
--------------------------------------------------------------------------------------------------

AIMHarness() -\> new AIMHarness component

Send (\"message\", recipient, message) commands to its \"inbox\" to send
instant messages. It will output (\"buddy online\", {name: buddyname})
and (\"message\", sender, message) tuples whenever a buddy comes online
or a new message arrives for you.

::: {.section}
### [Inboxes]{#symbol-AIMHarness.Inboxes}

-   **control** : NOT USED
-   **internal control** : links to signal outbox of various child
    components
-   **inbox** : tuple-based commands for ChatManager
-   **internal inbox** : links to various child components
:::

::: {.section}
### [Outboxes]{#symbol-AIMHarness.Outboxes}

-   **outbox** : tuple-based notifications from ChatManager
-   **signal** : NOT USED
-   **internal signal** : sends shutdown handling signals to various
    child components
-   **internal outbox** : outbox to various child components
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
#### [\_\_init\_\_(self, screenname, password)]{#symbol-AIMHarness.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-AIMHarness.main}

Waits for logged-in OSCARClient and links it up to ChatManager
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
