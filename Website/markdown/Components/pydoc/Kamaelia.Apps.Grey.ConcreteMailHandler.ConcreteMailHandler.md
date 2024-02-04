---
pagename: Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html){.reference}.[ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ConcreteMailHandler([Kamaelia.Apps.Grey.MailHandler.MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.MailHandler.html){.reference}) {#symbol-ConcreteMailHandler}
------------------------------------------------------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-ConcreteMailHandler.Inboxes}

-   **control** : Shutdown & control messages regarding client side
    socket handling
-   **tcp\_inbox** : This is where we get respones from the real SMTP
    server
-   **tcp\_control** : This is where we get shutdown information from
    the real SMTP server
-   **inbox** : Data from the client connecting to the server comes in
    here
:::

::: {.section}
### [Outboxes]{#symbol-ConcreteMailHandler.Outboxes}

-   **outbox** : Data sent here goes back the the client connecting to
    the server
-   **signal** : Shutdown & control messages regarding client side
    socket handling
-   **tcp\_outbox** : Data sent here is sent to the real SMTP server
-   **tcp\_signal** : We send messages here to shutdown the connection
    to the real SMTP connection
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
#### [RelayError(self)]{#symbol-ConcreteMailHandler.RelayError}
:::

::: {.section}
#### [\_\_init\_\_(self, \*\*argv)]{#symbol-ConcreteMailHandler.__init__}
:::

::: {.section}
#### [acceptMail(self)]{#symbol-ConcreteMailHandler.acceptMail}
:::

::: {.section}
#### [connectToRealSMTPServer(self)]{#symbol-ConcreteMailHandler.connectToRealSMTPServer}
:::

::: {.section}
#### [deferMail(self)]{#symbol-ConcreteMailHandler.deferMail}
:::

::: {.section}
#### [error(self, message)]{#symbol-ConcreteMailHandler.error}
:::

::: {.section}
#### [getline\_fromsmtpserver(self)]{#symbol-ConcreteMailHandler.getline_fromsmtpserver}
:::

::: {.section}
#### [handleConnect(self)]{#symbol-ConcreteMailHandler.handleConnect}
:::

::: {.section}
#### [handleData(self, command)]{#symbol-ConcreteMailHandler.handleData}
:::

::: {.section}
#### [handleDisconnect(self)]{#symbol-ConcreteMailHandler.handleDisconnect}
:::

::: {.section}
#### [handleEhlo(self, command)]{#symbol-ConcreteMailHandler.handleEhlo}
:::

::: {.section}
#### [handleHelo(self, command)]{#symbol-ConcreteMailHandler.handleHelo}
:::

::: {.section}
#### [handleHelp(self, command)]{#symbol-ConcreteMailHandler.handleHelp}
:::

::: {.section}
#### [handleMail(self, command)]{#symbol-ConcreteMailHandler.handleMail}
:::

::: {.section}
#### [handleNoop(self, command)]{#symbol-ConcreteMailHandler.handleNoop}
:::

::: {.section}
#### [handleQuit(self, command)]{#symbol-ConcreteMailHandler.handleQuit}
:::

::: {.section}
#### [handleRcpt(self, command)]{#symbol-ConcreteMailHandler.handleRcpt}
:::

::: {.section}
#### [handleRset(self, command)]{#symbol-ConcreteMailHandler.handleRset}
:::

::: {.section}
#### [handleVrfy(self, command)]{#symbol-ConcreteMailHandler.handleVrfy}
:::

::: {.section}
#### [shouldWeAcceptMail(self)]{#symbol-ConcreteMailHandler.shouldWeAcceptMail}
:::
:::

::: {.section}
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
-   [logResult](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html#symbol-MailHandler.logResult){.reference}(self)
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
