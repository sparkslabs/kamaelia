---
pagename: Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.html){.reference}
===========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.GreyListingPolicy.html){.reference}**
:::

-   [Greylisting Policy For/Subclass Of Concrete Mail
    Handler](#63){.reference}
    -   [Example Usage](#64){.reference}
    -   [How does it work?](#65){.reference}
:::

::: {.section}
Greylisting Policy For/Subclass Of Concrete Mail Handler {#63}
========================================================

This component implements a greylisting SMTP proxy protocol, by
subclassing ConcreteMailHandler and overriding the appropriate methods
(primarily the shouldWeAcceptMail method).

For more detail, please see <http://www.kamaelia.org/KamaeliaGrey>

::: {.section}
[Example Usage]{#example-usage} {#64}
-------------------------------

You use this as follows (at minimum):

``` {.literal-block}
ServerCore(protocol=GreyListingPolicy, port=25)
```

If you want to have a hardcoded/configured greylisting server you could
do this:

``` {.literal-block}
class GreyLister(ServerCore):
    class protocol(GreyListingPolicy):
        allowed_senders = []
        allowed_sender_nets = []
        allowed_domains = [ ]

GreyLister(port=25)
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#65}
--------------------------------------

Primarily it override the method shouldWeAcceptMail, and implements the
following logic:

``` {.literal-block}
if self.sentFromAllowedIPAddress():  return True # Allowed hosts can always send to anywhere through us
if self.sentFromAllowedNetwork():    return True # People on truste networks can always do the same
if self.sentToADomainWeForwardFor():
    try:
        for recipient in self.recipients:
            if self.whiteListed(recipient):
                return True
            if not self.isGreylisted(recipient):
                return False
    except Exception, e:
        pass
    return True # Anyone can always send to hosts we own
```

Clearly AllowedIPAddress, AllowedNetwork, whiteListed, and
DomainWeForwardFor are fairly clear concepts, so for more details on
those please look at the implementation.

isGreylisted by comparison is slightly more complex. Fundamentally this
works on the basis of saying this:

> -   have we seen the triple (ip, sender, recipient) before ?
> -   if we have, then allow the message through
> -   otherwise, defer the message

Now there is a little more subtlty here, based on the following
conditions:

> -   If greylisted, and not been there too long, allow through
> -   If grey too long, refuse (restarting the greylisting for that
>     combo)
> -   If not seen this triplet before, defer and note triplet
> -   If triplet retrying waaay too soon, reset their timer & defer
> -   If triplet retrying too soon generally speaking just defer
> -   If triplet hasn\'t been seen in aaaages, defer
> -   Otherwise, allow through & greylist them
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.html){.reference}.[GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.GreyListingPolicy.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================

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
