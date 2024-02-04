---
pagename: Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html){.reference}
===============================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler.html){.reference}**
:::

-   [Concrete Mail Core](#66){.reference}
    -   [Note](#67){.reference}
    -   [Example Usage](#68){.reference}
    -   [How does it work?](#69){.reference}
    -   [Configuration](#70){.reference}
:::

::: {.section}
Concrete Mail Core {#66}
==================

This code enforces the basic statemachine that SMTP expects, switching
between the various commands and finally results in forwarding on the
SMTP command to the appropriate SMTP server. By itself, this can be used
as a simple SMTP Proxy server.

This class is a subclass of MailHandler, and as such largely consists of
methods overriding methods from MailHandler which are designed to be
overridden.

Furthermore, it expects to forward any mail it accepts to another SMTP
mail server, as transparently as possible. Thus this concrete mail core
effectively forms the core of an SMTP proxy.

::: {.section}
[Note]{#note} {#67}
-------------

As it stands however, by default this mail proxy will *not* forward any
mails to the internal server. In order to change this, you would need to
subclass this server and replace the method \"shouldWeAcceptMail\" since
that defaults to returning False
:::

::: {.section}
[Example Usage]{#example-usage} {#68}
-------------------------------

As noted, you are not expected to use this ConcreteMailHandler directly,
but if you did, you would use it like this:

``` {.literal-block}
ServerCore(protocol=ConcreteMailHandler, port=1025)
```

At minimum, you would need to do this::

:   

    class SpamMeHandler(ConcreteMailHandler):

    :   

        def shouldWeAcceptMail(self):
        :   return True

    ServerCore(protocol=SpamMeHandler, port=1025)

You could alternatively do this::

:   

    class SpamMeMailServer(ServerCore):

    :   

        class protcol(ConcreteMailHandler):

        :   

            def shouldWeAcceptMail(self):
            :   return True

    ServerCore(port=1025)
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#69}
--------------------------------------

As noted this overrides all the methods relating to handling SMTP
commands, and enforces the state machine that SMTP requires. It\'s
particularly strict about this, in breach of Postel\'s law for two
reasons -

> -   It helps eradicate spam
> -   because most spam systems are generally lax these days and most
>     non-spam systems are generally strict

It was also primarily written in the context of a greylisting server.

Some core values it tracks with regard to a mail -

:   -   a list of recipients
    -   the (claimed) sender
    -   the (claimed) remote/client name
    -   the actual client & local port/ip addresses

Once the client has finished sending the data for an email, the proxy
forwards the mail to the local real SMTP server. Fundamentally this
happens by making a connection to the real server using the TCPClient
component, and then replaying all the lines the original server sent us
to the local server.

(ie an inbox\_log is built up with all data recieved from inbox
\"inbox\" and then the contents of this are replayed when being sent to
the local (real) SMTP mail server)
:::

::: {.section}
[Configuration]{#configuration} {#70}
-------------------------------

This class provides a large number of configuration options. You can
either change this through subclassing or by providing as named
arguments to the \_\_init\_\_ function. The options you have -

> -   servername - The name this server will choose to use to identify
>     itself
> -   serverid - The string this server will use to identify itself (in
>     terms of software in use)
> -   smtp\_ip - the ip address of the server you\'re proxying for/to
> -   smtp\_port - this is the port the server you\'re proxying for/to
>     is listening on

The following attributes get set when a client connects -

> -   peer - the IP address of the client
> -   peerport - the port which the peer is connected from
> -   local - the IP address the client has connected to
> -   localport - the port which they\'re connected to
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html){.reference}.[ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================================================

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
