---
pagename: Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.GreyListingPolicy
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.html){.reference}.[GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.GreyListingPolicy.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.html){.reference}

------------------------------------------------------------------------

::: {.section}
class GreyListingPolicy([Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler.html){.reference}) {#symbol-GreyListingPolicy}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-GreyListingPolicy.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-GreyListingPolicy.Outboxes}
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
#### [isGreylisted(self, recipient)]{#symbol-GreyListingPolicy.isGreylisted}
:::

::: {.section}
#### [logResult(self)]{#symbol-GreyListingPolicy.logResult}
:::

::: {.section}
#### [sentFromAllowedIPAddress(self)]{#symbol-GreyListingPolicy.sentFromAllowedIPAddress}
:::

::: {.section}
#### [sentFromAllowedNetwork(self)]{#symbol-GreyListingPolicy.sentFromAllowedNetwork}
:::

::: {.section}
#### [sentToADomainWeForwardFor(self)]{#symbol-GreyListingPolicy.sentToADomainWeForwardFor}
:::

::: {.section}
#### [shouldWeAcceptMail(self)]{#symbol-GreyListingPolicy.shouldWeAcceptMail}
:::

::: {.section}
#### [whiteListed(self, recipient)]{#symbol-GreyListingPolicy.whiteListed}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler.html){.reference} :

-   [getline\_fromsmtpserver](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.getline_fromsmtpserver){.reference}(self)
-   [handleVrfy](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleVrfy){.reference}(self,
    command)
-   [handleQuit](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleQuit){.reference}(self,
    command)
-   [handleMail](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleMail){.reference}(self,
    command)
-   [\_\_init\_\_](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.__init__){.reference}(self,
    \*\*argv)
-   [handleNoop](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleNoop){.reference}(self,
    command)
-   [handleRset](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleRset){.reference}(self,
    command)
-   [handleData](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleData){.reference}(self,
    command)
-   [deferMail](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.deferMail){.reference}(self)
-   [handleDisconnect](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleDisconnect){.reference}(self)
-   [handleRcpt](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleRcpt){.reference}(self,
    command)
-   [handleEhlo](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleEhlo){.reference}(self,
    command)
-   [RelayError](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.RelayError){.reference}(self)
-   [handleHelo](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleHelo){.reference}(self,
    command)
-   [handleConnect](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleConnect){.reference}(self)
-   [error](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.error){.reference}(self,
    message)
-   [handleHelp](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.handleHelp){.reference}(self,
    command)
-   [connectToRealSMTPServer](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.connectToRealSMTPServer){.reference}(self)
-   [acceptMail](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html#symbol-ConcreteMailHandler.acceptMail){.reference}(self)
:::

::: {.section}
#### Methods inherited from [Kamaelia.Apps.Grey.MailHandler.MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.MailHandler.html){.reference} :

-   [noteToDebugLog](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.noteToDebugLog){.reference}(self,
    line)
-   [noteToLog](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.noteToLog){.reference}(self,
    line)
-   [lastline](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.lastline){.reference}(self)
-   [main](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.main){.reference}(self)
-   [getline](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.getline){.reference}(self)
-   [handleCommand](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.handleCommand){.reference}(self,
    command)
-   [netPrint](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.netPrint){.reference}(self,
    \*args)
-   [logging\_recv\_connection](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.logging_recv_connection){.reference}(self)
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
