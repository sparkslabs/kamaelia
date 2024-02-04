---
pagename: Components/pydoc/Kamaelia.Apps.Grey.MailHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html){.reference}
===============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.MailHandler.html){.reference}**
:::

-   [Abstract SMTP Mailer Core](#57){.reference}
    -   [Example Usage](#58){.reference}
    -   [Note](#59){.reference}
    -   [How does it work?](#60){.reference}
    -   [Configuration](#61){.reference}
    -   [Methods you are expected to override](#62){.reference}
:::

::: {.section}
Abstract SMTP Mailer Core {#57}
=========================

This component effectively forms the skeleton of an SMTP server. It
expects an SMTP client to connect and send various SMTP requests to it.
This basic SMTP Mailer Core however, does not actually do anything in
response to any of the SMTP commands it expects.

Each SMTP command is actually given a dummy callback which more
customised SMTP protocol handlers are expected to override. Beyond this,
this component is expected to be used as a protocol handler for
ServerCore.

Fundamentally, this component handles the command/response structure of
SMTP fairly directly, but expects the brains of the protocol to be
implemented by a more intelligent subclass.

::: {.section}
[Example Usage]{#example-usage} {#58}
-------------------------------

Whilst this will work to a minimal extent:

``` {.literal-block}
ServerCore(protocol=MailHandler, port=1025)
```

This will not actually form a very interesting SMTP, nor SMTP compliant,
server since whilst it will tell you commands it doesn\'t understand, it
will not do anything interesting.

You are as noted expected to subclass MailHandler. For a better example
of how to subclass MailHandler you are suggested to look at
Kamaelia.Apps.ConcreteMailHandler.ConcreteMailHandler
:::

::: {.section}
[Note]{#note} {#59}
-------------

This component is not complete - you are expected to subclass it to
finish it off as you need. Specifically it does not implement the
following:

> -   It does not enforce \"this command followed by that command\"
> -   It does not actually do anything with any DATA a client sends you
> -   It neither performs local mail delivery nor proxying - you\'d need
>     to implement this yourself.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#60}
--------------------------------------

The component is expected to be connected to a client TCP connection by
ServerCore, such that messages from the network arrive on inbox
\"inbox\", and outgoing messages get sent to outbox \"outbox\"

The component will terminate if any of these is true:

> -   The client breaks the connection
> -   One of the methods sets self.breakConnection to True.
> -   If a \"socketShutdown\" message arrives on inbox \"control\"

The main() method divides the connection into effectively two main
states:

> -   accepting random commands prior to getting a DATA command
> -   accepting the email during a DATA command

SMTP commands are specifically dispatched to a particular handler for
that command. In this component none of the handlers do anything
interesting.
:::

::: {.section}
[Configuration]{#configuration} {#61}
-------------------------------

The abstract mailer supports some basic config settings:

> -   logfile - path/filename where requests should get logged
> -   debuglogfile - path/filename to where the debug log file should
>     do.
:::

::: {.section}
[Methods you are expected to override]{#methods-you-are-expected-to-override} {#62}
-----------------------------------------------------------------------------

Whilst you are probably better off subclassing ConcreteMailHandler, you
will probably need to override the following methods in a subclass if
you subclass MailHandler directly.

> -   handleConnect(self)
> -   handleHelo(self,command)
> -   handleEhlo(self,command)
> -   handleMail(self,command)
> -   handleRcpt(self,command)
> -   handleData(self,command)
> -   handleQuit(self,command)
> -   handleRset(self,command)
> -   handleNoop(self,command)
> -   handleVrfy(self,command)
> -   handleHelp(self,command)
> -   logResult(self)
> -   handleDisconnect(self)
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html){.reference}.[MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.MailHandler.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class MailHandler([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-MailHandler}
---------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-MailHandler.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-MailHandler.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-MailHandler.__init__}
:::

::: {.section}
#### [getline(self)]{#symbol-MailHandler.getline}
:::

::: {.section}
#### [handleCommand(self, command)]{#symbol-MailHandler.handleCommand}
:::

::: {.section}
#### [handleConnect(self)]{#symbol-MailHandler.handleConnect}
:::

::: {.section}
#### [handleData(self, command)]{#symbol-MailHandler.handleData}
:::

::: {.section}
#### [handleDisconnect(self)]{#symbol-MailHandler.handleDisconnect}
:::

::: {.section}
#### [handleEhlo(self, command)]{#symbol-MailHandler.handleEhlo}
:::

::: {.section}
#### [handleHelo(self, command)]{#symbol-MailHandler.handleHelo}
:::

::: {.section}
#### [handleHelp(self, command)]{#symbol-MailHandler.handleHelp}
:::

::: {.section}
#### [handleMail(self, command)]{#symbol-MailHandler.handleMail}
:::

::: {.section}
#### [handleNoop(self, command)]{#symbol-MailHandler.handleNoop}
:::

::: {.section}
#### [handleQuit(self, command)]{#symbol-MailHandler.handleQuit}
:::

::: {.section}
#### [handleRcpt(self, command)]{#symbol-MailHandler.handleRcpt}
:::

::: {.section}
#### [handleRset(self, command)]{#symbol-MailHandler.handleRset}
:::

::: {.section}
#### [handleVrfy(self, command)]{#symbol-MailHandler.handleVrfy}
:::

::: {.section}
#### [lastline(self)]{#symbol-MailHandler.lastline}
:::

::: {.section}
#### [logResult(self)]{#symbol-MailHandler.logResult}
:::

::: {.section}
#### [logging\_recv\_connection(self)]{#symbol-MailHandler.logging_recv_connection}
:::

::: {.section}
#### [main(self)]{#symbol-MailHandler.main}
:::

::: {.section}
#### [netPrint(self, \*args)]{#symbol-MailHandler.netPrint}
:::

::: {.section}
#### [noteToDebugLog(self, line)]{#symbol-MailHandler.noteToDebugLog}
:::

::: {.section}
#### [noteToLog(self, line)]{#symbol-MailHandler.noteToLog}
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
