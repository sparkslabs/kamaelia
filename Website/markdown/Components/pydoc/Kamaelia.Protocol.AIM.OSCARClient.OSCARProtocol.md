---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARProtocol
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}.[OSCARProtocol](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARProtocol.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}

------------------------------------------------------------------------

::: {.section}
class OSCARProtocol([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-OSCARProtocol}
-----------------------------------------------------------------------------------------------------

OSCARProtocol() -\> new OSCARProtocol component.

Provides a Kamaelia interface to the lowest level of OSCAR protocol, the
FLAP level.

For more information on FLAPs, see module level docs.

::: {.section}
### [Inboxes]{#symbol-OSCARProtocol.Inboxes}

-   **control** : shutdown handling
-   **inbox** : receives binary data from the AIM server
-   **talk** : receives messages in the format (channel, FLAP payload)
:::

::: {.section}
### [Outboxes]{#symbol-OSCARProtocol.Outboxes}

-   **outbox** : sends binary data to the AIM server.
-   **signal** : shutdown handling
-   **heard** : resends messages from \'outbox\' in the form (channel,
    FLAP payload)
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
#### [\_\_init\_\_(self)]{#symbol-OSCARProtocol.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkBoxes(self)]{#symbol-OSCARProtocol.checkBoxes}

checks for data in all our boxes, and if there is data, then call the
appropriate function to handle it.
:::

::: {.section}
#### [handlecontrol(self)]{#symbol-OSCARProtocol.handlecontrol}
:::

::: {.section}
#### [handleinbox(self)]{#symbol-OSCARProtocol.handleinbox}

receives data coming in through the wire, reformats it into a
Python-friendly form, and retransmits it to its \"heard\" outbox.
:::

::: {.section}
#### [handletalk(self)]{#symbol-OSCARProtocol.handletalk}

checks that incoming messages from the \"talk\" inbox are in a (channel,
flap data) tuple. If not, exceptions are raised. If so,
OSCARProtocol.sendFLAP is called.
:::

::: {.section}
#### [main(self)]{#symbol-OSCARProtocol.main}

main loop
:::

::: {.section}
#### [sendFLAP(self, data\[, channel\])]{#symbol-OSCARProtocol.sendFLAP}

constructs FLAPs and sends them
:::
:::

::: {.section}
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
