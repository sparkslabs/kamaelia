---
pagename: Docs/Axon/Axon
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}
----------------------------------------
:::
:::

::: {.section}
Axon - the core concurrency system for Kamaelia
===============================================

::: {.container}
:::

-   [Base classes for building your own components](#0){.reference}
-   [Underlying concurrency system](#1){.reference}
-   [Services, statistics, Instrospection](#2){.reference}
-   [Exceptions, Messages and Misc](#3){.reference}
-   [Integration with other systems](#4){.reference}
-   [Internals for implementing inboxes, outboxes and
    linkages](#5){.reference}
-   [Debugging support](#6){.reference}
:::

::: {.section}
Axon is a component concurrency framework. With it you can create
software \"components\" that can run concurrently with each other.
Components have \"inboxes\" and \"outboxes\" through with they
communicate with other components.

A component may send a message to one of its outboxes. If a linkage has
been created from that outbox to another component\'s inbox; then that
message will arrive in the inbox of the other component. In this way,
components can send and receive data - allowing you to create systems by
linking many components together.

Each component is a microprocess - rather like a thread of execution. A
scheduler takes care of making sure all microprocesses (and therefore
all components) get regularly executed. It also looks after putting
microprocesses to sleep (when they ask to be) and waking them up (for
example, when something arrives in one of their inboxes).

::: {.section}
[Base classes for building your own components]{#base-classes-for-building-your-own-components} {#0}
-----------------------------------------------------------------------------------------------

-   **[Axon.Component](/Docs/Axon/Axon.Component.html){.reference}**
    -   defines the basic component. Subclass it to write your own
        components.
-   **[Axon.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.html){.reference}**
    -   like a basic component but with facilties to let you add and
        remove inboxes and outboxes during runtime.
-   **[Axon.ThreadedComponent](/Docs/Axon/Axon.ThreadedComponent.html){.reference}**
    -   like ordinary components, but which truly run in a separate
        thread - meaning they can perform blocking tasks (since they
        don\'t have to yield control to the scheduler for other
        components to continue executing)
:::

::: {.section}
[Underlying concurrency system]{#underlying-concurrency-system} {#1}
---------------------------------------------------------------

-   **[Axon.Microprocess](/Docs/Axon/Axon.Microprocess.html){.reference}**
    -   Turns a python generator into a schedulable microprocess -
        something that can be started, paused, reawoken and stopped.
        Subclass it to make your own.
-   **[Axon.Scheduler](/Docs/Axon/Axon.Scheduler.html){.reference}**
    -   Runs the microprocesses. Manages the starting, stopping, pausing
        and waking of them. Is also a microprocess itself!
:::

::: {.section}
[Services, statistics, Instrospection]{#services-statistics-instrospection} {#2}
---------------------------------------------------------------------------

-   **[Axon.CoordinatingAssistantTracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html){.reference}**
    -   provides mechanisms for components to advertising and discover
        services they can provide for each other.
    -   acts as a repository for collecting statistics from components
        in the system
-   **[Axon.Introspector](/Docs/Axon/Axon.Introspector.html){.reference}**
    -   outputs live topology data describing what components there are
        in a running axon system and how they are linked together.
:::

::: {.section}
[Exceptions, Messages and Misc]{#exceptions-messages-and-misc} {#3}
--------------------------------------------------------------

-   **[Axon.Axon](/Docs/Axon/Axon.Axon.html){.reference}**
    -   base metaclass for key Axon classes
-   **[Axon.AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}**
    -   classes defining various exceptions in Axon.
-   **[Axon.Ipc](/Docs/Axon/Axon.Ipc.html){.reference}**
    -   classes defining various IPC messages in Axon used for
        signalling shutdown, errors, notifications, etc\...
-   **[Axon.idGen](/Docs/Axon/Axon.idGen.html){.reference}**
    -   unique id value generation
-   **[Axon.util](/Docs/Axon/Axon.util.html){.reference}**
    -   various miscellaneous support utility methods
:::

::: {.section}
[Integration with other systems]{#integration-with-other-systems} {#4}
-----------------------------------------------------------------

-   **[Axon.background](/Docs/Axon/Axon.background.html){.reference}**
    -   use Axon components within other python programs by wrapping
        them in a scheduler running in a separate thread
-   **[Axon.Handle](/Docs/Axon/Axon.Handle.html){.reference}**
    -   a Handle for getting data into and out of the standard inboxes
        and outboxes of a component from a non Axon based piece of code.
        Useful in combination with
        [Axon.background](/Docs/Axon/Axon.background.html){.reference}
:::

::: {.section}
[Internals for implementing inboxes, outboxes and linkages]{#internals-for-implementing-inboxes-outboxes-and-linkages} {#5}
----------------------------------------------------------------------------------------------------------------------

-   **[Axon.Box](/Docs/Axon/Axon.Box.html){.reference}**
    -   The base implementation of inboxes and outboxes.
-   **[Axon.Postoffice](/Docs/Axon/Axon.Postoffice.html){.reference}**
    -   All components have one of these for creating, destroying and
        tracking linkages.
-   **[Axon.Linkage](/Docs/Axon/Axon.Linkage.html){.reference}**
    -   handles used to describe linkages from one postbox to another

What, no Postman? Optimisations made to Axon have dropped the Postman.
Inboxes and outboxes handle the delivery of messages themselves now.
:::

::: {.section}
[Debugging support]{#debugging-support} {#6}
---------------------------------------

-   **[Axon.debug](/Docs/Axon/Axon.debug.html){.reference}**
    -   defines a debugging output object.
-   **[Axon.debugConfigFile](/Docs/Axon/Axon.debugConfigFile.html){.reference}**
    -   defines a method for loading a debugging configuration file that
        determines what debugging output gets displayed and what gets
        filtered out.
-   **[Axon.debugConfigDefaults](/Docs/Axon/Axon.debugConfigDefaults.html){.reference}**
    -   defines a method that supplies a default debugging
        configuration.
:::
:::

------------------------------------------------------------------------

::: {.section}
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
