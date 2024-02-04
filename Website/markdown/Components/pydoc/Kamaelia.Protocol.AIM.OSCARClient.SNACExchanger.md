---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}.[SNACExchanger](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SNACExchanger([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SNACExchanger}
-----------------------------------------------------------------------------------------------------

SNACExchanger() -\> component that has methods specialized for sending
and receiving FLAPs over Channel 2 (FLAPs whose payloads are SNACs).

For a more thorough discussion on SNACs, see module level docs.

::: {.section}
### [Inboxes]{#symbol-SNACExchanger.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SNACExchanger.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-SNACExchanger.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [recvSnac(self)]{#symbol-SNACExchanger.recvSnac}

receives FLAPs containing SNACs and parses the SNAC data.
:::

::: {.section}
#### [sendSnac(self, fam, sub, body)]{#symbol-SNACExchanger.sendSnac}

constructs a SNAC by calling self.makeSnac and sends it out the
\"outbox\".

FIXME: It would be extremely helpful to have a predefined set of SNAC
constants or perhaps even classes to pass to this method. For example,
self.sendSnac(04, 06, data) is a lot less clear than something like
self.sendSnac(MESSAGE\_TO\_USER, data).
:::

::: {.section}
#### [waitSnac(self, fam, sub)]{#symbol-SNACExchanger.waitSnac}

Yields 1 until a SNAC of the requested family and subtype is received.
The last value yielded is the payload of the requested SNAC.

Usage::
:   for result in self.waitSnac(family, subtype): yield 1.

The body of the requested SNAC will be assigned to \"result\".
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
