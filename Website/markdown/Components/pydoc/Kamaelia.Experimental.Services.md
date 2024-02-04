---
pagename: Components/pydoc/Kamaelia.Experimental.Services
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}
==============================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [RegisterService](/Components/pydoc/Kamaelia.Experimental.Services.RegisterService.html){.reference}**
-   **component
    [Subscribe](/Components/pydoc/Kamaelia.Experimental.Services.Subscribe.html){.reference}**
-   **component
    [ToService](/Components/pydoc/Kamaelia.Experimental.Services.ToService.html){.reference}**
:::

-   [Components to help build Services (EXPERIMENTAL)](#553){.reference}
    -   [Register Service](#554){.reference}
        -   [Example Usage:](#555){.reference}
        -   [How does it work?](#556){.reference}
    -   [Subscibe To Service](#557){.reference}
        -   [Example Usage:](#558){.reference}
        -   [How does it work?](#559){.reference}
    -   [Connect To Service](#560){.reference}
        -   [Example Usage](#561){.reference}
        -   [How does it work?](#562){.reference}
:::

::: {.section}
Components to help build Services (EXPERIMENTAL) {#553}
================================================

These components make it easier to build and use public services,
registered with the Coordinating Assistant Tracker.

Note: These components are EXPERIMENTAL and are likely to under go
substantial change

::: {.section}
[Register Service]{#register-service} {#554}
-------------------------------------

A function that registers specified inboxes on a component as named
services with the Coordinating Assistant Tracker (CAT). Returns the
component, so can be dropped in where you would ordinarily use a
component.

::: {.section}
### [Example Usage:]{#example-usage} {#555}

Create and activate MyComponent instance, registering its \"inbox\"
inbox with the CAT as a service called \"MyService\":

``` {.literal-block}
RegisterService( MyComponent(), {"MyService":"inbox"} ).activate()
```
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#556}

This method registers the component you provide with the CAT. It
register the inboxes on it that you specify using the names that you
specify.
:::
:::

::: {.section}
[Subscibe To Service]{#subscibe-to-service} {#557}
-------------------------------------------

A component that connects to a public service and sends a fixed format
message to it requesting to subscribe to a set of \'things\' it
provides.

::: {.section}
### [Example Usage:]{#id1} {#558}

Subscribe to a (fictional) \"TV Channels Service\", asking for three
channels. The tv channel data is then recorded:

``` {.literal-block}
pipeline(
    SubscribeTo( "TV Channels Service", ["BBC ONE", "BBC TWO", "ITV"] ),
    RecordChannels(),
    ).run()
```

The message sent to the \"TV Channels Service\" will be:

``` {.literal-block}
("ADD", ["BBC ONE", "BBC TWO", "ITV"], ( <theSubscribeToComponent>, "inbox" ) )
```
:::

::: {.section}
### [How does it work?]{#id2} {#559}

Describe more detail here
:::
:::

::: {.section}
[Connect To Service]{#connect-to-service} {#560}
-----------------------------------------

A component that connects to a public service. Any data you send to its
inbox gets sent to the service.

::: {.section}
### [Example Usage]{#id3} {#561}

``` {.literal-block}
pipeline( MyComponentThatSendMessagesToService(),
        ConnectTo("Name of service"),
        ).run()
```
:::

::: {.section}
### [How does it work?]{#id4} {#562}

Describe in more detail here.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}.[RegisterService](/Components/pydoc/Kamaelia.Experimental.Services.RegisterService.html){.reference}
===================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: RegisterService {#symbol-RegisterService}
-----------------------
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}.[Subscribe](/Components/pydoc/Kamaelia.Experimental.Services.Subscribe.html){.reference}
=======================================================================================================================================================================================================================================================================================================

::: {.section}
class Subscribe([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Subscribe}
-------------------------------------------------------------------------------------------------

Subscribes to a service, and forwards what it receives to its outbox.
Also forwards anything that arrives at its inbox to its outbox.

Unsubscribes when shutdown.

::: {.section}
### [Inboxes]{#symbol-Subscribe.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Subscribe.Outboxes}

-   **outbox** :
-   **signal** : shutdown signalling
-   **\_toService** : request to service
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
#### [\_\_init\_\_(self, servicename, \*requests)]{#symbol-Subscribe.__init__}

Subscribe to the specified service, wiring to it, then sending the
specified messages. Requests are of the form (\"ADD\", request,
destination)
:::

::: {.section}
#### [main(self)]{#symbol-Subscribe.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-Subscribe.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}.[ToService](/Components/pydoc/Kamaelia.Experimental.Services.ToService.html){.reference}
=======================================================================================================================================================================================================================================================================================================

::: {.section}
class ToService([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ToService}
-------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-ToService.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-ToService.Outboxes}
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
#### [\_\_init\_\_(self, toService)]{#symbol-ToService.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ToService.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ToService.shutdown}
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
