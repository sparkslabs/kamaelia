---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.LoginHandler.LoginHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[LoginHandler](/Components/pydoc/Kamaelia.Protocol.AIM.LoginHandler.html){.reference}.[LoginHandler](/Components/pydoc/Kamaelia.Protocol.AIM.LoginHandler.LoginHandler.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.AIM.LoginHandler.html){.reference}

------------------------------------------------------------------------

::: {.section}
class LoginHandler([Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger.html){.reference}) {#symbol-LoginHandler}
---------------------------------------------------------------------------------------------------------------------------------------------------------

LoginHandler(screenname, password, \[versionNumber\]) -\> new
LoginHandler component

Once started, LoginHandler logs in to AIM and sends the primed
connection out of its \"signal\" outbox.

Keyword arguments:

-   versionNumber \-- the version of OSCAR protocol we are using.
    Default 1.

::: {.section}
### [Inboxes]{#symbol-LoginHandler.Inboxes}

-   **control** : NOT USED
-   **\_clock** : Receives timout messages
-   **inbox** : Receives messages from the server
:::

::: {.section}
### [Outboxes]{#symbol-LoginHandler.Outboxes}

-   **outbox** : Send messages to the server
-   **signal** : Also sends messages to the server
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
#### [\_\_init\_\_(self, screenname, password\[, versionNumber\])]{#symbol-LoginHandler.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [activateConnection(self)]{#symbol-LoginHandler.activateConnection}

Send some parameters up to the server, then signal that we\'re ready to
begin receiving data.
:::

::: {.section}
#### [connectAuth(self)]{#symbol-LoginHandler.connectAuth}

Connects to the AIM authorization server, says hi, and waits for
acknowledgement.
:::

::: {.section}
#### [extractBOSandCookie(self, reply)]{#symbol-LoginHandler.extractBOSandCookie}

Extracts BOS server, port, and auth cookie from server reply.
:::

::: {.section}
#### [getBOSandCookie(self)]{#symbol-LoginHandler.getBOSandCookie}

Gets BOS and auth cookie.
:::

::: {.section}
#### [getCookie(self)]{#symbol-LoginHandler.getCookie}

Requests and waits for MD5 key.
:::

::: {.section}
#### [getRateLimits(self)]{#symbol-LoginHandler.getRateLimits}

Request rate limits, wait for reply, and send acknowledgement to the
server.
:::

::: {.section}
#### [getRights(self)]{#symbol-LoginHandler.getRights}

. Get the server\'s reply on rights and limitations
:::

::: {.section}
#### [main(self)]{#symbol-LoginHandler.main}

Gets BOS and auth cookie, negotiates protocol, and then passes the
connection + any non-login-related messages out.
:::

::: {.section}
#### [negotiateProtocol(self)]{#symbol-LoginHandler.negotiateProtocol}

Negotiates protocol.
:::

::: {.section}
#### [parseRateInfo(self, data, numClasses)]{#symbol-LoginHandler.parseRateInfo}

Does something useful with the information about rate classes that the
server sends us and returns the acknowledgement we are supposed to send
back to the server.
:::

::: {.section}
#### [passTheReins(self)]{#symbol-LoginHandler.passTheReins}

Unlink the internal OSCARClient and send it to \"signal\". Also collect
any unused messages from OSCARClient and send them out through
\"signal\".
:::

::: {.section}
#### [reconnect(self, server, port, cookie)]{#symbol-LoginHandler.reconnect}

Discards old connection to authorization server, connects to BOS, says
hi, and waits for acknowledgement.
:::

::: {.section}
#### [requestRights(self)]{#symbol-LoginHandler.requestRights}

Request that the server tell us our rights and limitations for the
services that were accepted.
:::

::: {.section}
#### [setServiceVersions(self)]{#symbol-LoginHandler.setServiceVersions}

Waits for supported services list from server, requests service
versions, and waits for server acknowledgement of accepted service
versions.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger.html){.reference} :

-   [waitSnac](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html#symbol-SNACExchanger.waitSnac){.reference}(self,
    fam, sub)
-   [sendSnac](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html#symbol-SNACExchanger.sendSnac){.reference}(self,
    fam, sub, body)
-   [recvSnac](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html#symbol-SNACExchanger.recvSnac){.reference}(self)
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
