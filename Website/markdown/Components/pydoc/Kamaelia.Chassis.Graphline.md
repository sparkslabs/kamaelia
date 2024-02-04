---
pagename: Components/pydoc/Kamaelia.Chassis.Graphline
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}
=================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.Graphline.html){.reference}**
:::

-   [Wiring up components in a topology](#283){.reference}
    -   [Example Usage](#284){.reference}
    -   [Shutdown Examples](#285){.reference}
    -   [How does it work?](#286){.reference}
    -   [Shutdown Handling](#287){.reference}
-   [Test documentation](#288){.reference}
:::

::: {.section}
Wiring up components in a topology {#283}
==================================

The Graphline component wires up a set of components and encapsulates
them as a single component. They are wired up to each other using the
\'graph\' of linkages that you specify.

::: {.section}
[Example Usage]{#example-usage} {#284}
-------------------------------

Joining a PromtedFileReader and a rate control component to make a file
reader that reads at a given rate:

``` {.literal-block}
return Graphline(RC  = ByteRate_RequestControl(**rateargs),
                 RFA = PromptedFileReader(filename, readmode),
                 linkages = { ("RC",  "outbox")  : ("RFA", "inbox"),
                             ("RFA", "outbox")  : ("self", "outbox"),
                             ("RFA", "signal")  : ("RC",  "control"),
                             ("RC",  "signal")  : ("self", "signal"),
                             ("self", "control") : ("RFA", "control")
                             }
```

The references to \'self\' create linkages that passes through a named
inbox on the graphline to a named inbox of one of the child components.
Similarly a child\'s outbox is pass-through to a named outbox on the
graphline.
:::

::: {.section}
[Shutdown Examples]{#shutdown-examples} {#285}
---------------------------------------

In this example:

-   Pinger is a component that sends the messages from \"tosend\" after
    with a brief delay between messages. It sends the messages out of
    the stated outbox.
-   Waiter is a component that starts up, and then waits for any message
    sent to its inbox \"control\"
-   Whinger is a component that complains that it is running
    periodically, but will shutdown if it receives any message on its
    inbox \"control\"

As a result, this example creates 3 components inside a graphline that
wait for shutdown. The Pinger sends a message, which is duplicated to
all the subcomponents, at which point in time, they shutdown, causing
the system to shutdown:

``` {.literal-block}
Pipeline(
    Pinger(tosend=[Axon.Ipc.producerFinished()],box="signal"),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        TO_SHUTDOWN3 = Waiter(),
        linkages = {}
    ),
    Whinger(),
).run()
```

Note: the shutdown message propogates all the way through the system to
the whinger, which then also shuts down.

Full code for this is in
./Examples/UsingChassis/Graphline/DemoShutdown.py

You can also still have shutdown links between components. If you do,
then the Graphline doesn\'t interfere with them:

``` {.literal-block}
Pipeline(
    Pinger(tosend=[Axon.Ipc.producerFinished()],box="signal"),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        TO_SHUTDOWN3 = Waiter(),
        linkages = {
            ("TO_SHUTDOWN1","signal"):("TO_SHUTDOWN2","control"),
            ("TO_SHUTDOWN2","signal"):("TO_SHUTDOWN3","control"),
        }
    ),
    Whinger(),
).run()
```

Full code for this is in
./Examples/UsingChassis/Graphline/LinkedShutdown.py
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#286}
--------------------------------------

A Graphline component gives you a way of wiring up a system of
components and then encapsulating th ewhole as a single component, with
its own inboxes and outboxes.

The components you specify are registered as children of the Graphline
component. When you activate the component, all the child components are
activated, and the linkages you specified are created between them.

When specifying linkages, the component \'name\' is the string version
of the argument name you used to refer to the component. In the example
above, the components are therefore referred to as \"RC\" and \"RFA\".

If the name you specify is not one of the components you specify, then
it is assumed you must be referring to the Graphline component itself.
In the above example, \"self\" is used to make this clear. This gives
you a way of passing data in and out of the system of components you
have specified.

In these cases, it is assumed you wish to create a pass-through linkage
- you want the Graphline component to forward the named inbox to a
child\'s inbox, or to forward a child\'s outbox to a named outbox of the
Graphline. For example:

``` {.literal-block}
Graphline( child = MyComponent(...),
           linkages = { ...
                        ("self", "inbox") : ("child", "bar"),
                        ... }
         )
```

\... is interpreted as meaning you want to forward the \"inbox\" inbox
of the Graphline to the \"bar\" inbox of the component referred to as
\"child\". Similarly:

``` {.literal-block}
Graphline( child = MyComponent(...),
           linkages = { ...
                        ("child", "fwibble") : ("self", "outbox"),
                        ... }
         )
```

\...is interpreted as wishing to forward the \"fwibble\" outbox of the
component referred to as \"child\" to the \"outbox\" outbox of the
Graphline component.

Any inbox or outbox you name on the Graphline component is created if it
does not already exist. For example, you might want the Graphline to
have a \"video\" and an \"audio\" inbox:

``` {.literal-block}
Graphline( videoHandler = MyVideoComponent(),
           audioHandler = MyAudioComponent(),
           linkages = { ...
                        ("self", "video") : ("videoHandler", "inbox"),
                        ("self", "audio") : ("audioHandler", "inbox"),
                        ...
                      }
         )
```

The Graphline component will always have inboxes \"inbox\" and
\"control\" and outboxes \"outbox\" and \"signal\", even if you do not
specify any linkages to them.

During runtime, the Graphline component monitors the child components.
It will terminate if, and only if, *all* the child components have also
terminated.

NOTE that if your child components create additional components
themselves, the Graphline component will not know about them. It only
monitors the components it was originally told about.

Graphline does not GENERALLY intercept any of its inboxes or outboxes.
It ignores whatever traffic flows through them. If you have specified
linkages from them to components inside the graphline, then the data
automatically flows to/from them as you specified.
:::

::: {.section}
[Shutdown Handling]{#shutdown-handling} {#287}
---------------------------------------

There is however an exception: shutdown handling, where the difference
is light touch, which is this:

``` {.literal-block}
while not self.childrenDone():
     always pass on messages from our control to appropriate sub-component's control
     if message is shutdown, set shutdown flag

# then after loop

if no component-has-linkage-to-graphline's signal
     if shutdown flag set:
         pass on shutdownMicroprocess
     else:
         pass on producerFinished
```

If the user has wired up the graphline\'s control box to pass through to
one of their components, then that request is honoured, and the user
then becomes wholly responsible for shutdown.
:::

Test documentation {#288}
==================

Tests passed:

-   Children are activated as soon as the Graphline itself is activated,
    but no sooner. They get activated even if they have no linkages
    specified to them.
-   Children are activated as soon as the Graphline itself is activated,
    but no sooner. They get activated even if they have no linkages
    specified to them.
-   If a graphline\'s \"signal\" outbox is specified to be wired to a
    child component, the graphline will send any messages itself out of
    its \"signal\" outbox, before or after all children have terminated,
    even if a shutdownMicroprocess or producerFinished message was sent
    to its \"control\" inbox.
-   When all children have terminated. If no child is wired to the
    Graphline\'s \"signal\" outbox, the Graphline will send out its own
    message. The message sent will be a producerFinished message if a
    child is wired to the Graphline\'s \"control\" inbox, or if no
    shutdownMicroprocess message has been previously received on that
    inbox.
-   When all children have terminated. If no child is wired to the
    Graphline\'s \"signal\" outbox, the Graphline will send out its own
    message. If no child is wired to the Graphline\'s \"control\" inbox
    and a shutdownMicroprocess message has been previously received on
    that inbox, then the message sent out will be that
    shutdownMicroprocess message.
-   Instantiating with components as named arguments, and specifying an
    empty linkages argument succeeds
-   Instantiating a graphline, components specified as named arguments,
    eg. A=component() and B=component() become children of the graphline
    once activated and run.
-   Instantiating with no components as named arguments, and specifying
    an empty linkages argument succeeds
-   Instantiating with components as named arguments, but specifying no
    linkages argument results in a ValueError exception
-   A linkage from \"outbox\" to \"inbox\" between two named child
    components \"A\" and \"B\" can be specified by specifying a
    \"linkages\" argument containing a dictionary with an entry:
    (\"A\",\"outbox\"):(\"B\",\"inbox\"). Data sent to A\'s \"outbox\"
    will reach B\'s \"inbox\" and nowhere else.
-   If a graphline\'s \"control\" inbox and \"signal\" outbox are both
    specified to be wired to child components in the graphline, then
    graphline will not emit its own messages out of its \"signal\"
    outbox when it terminates (or at any other time)
-   If a graphline\'s \"control\" inbox and \"signal\" outbox are not
    specified to be wired to a child component in the graphline then, if
    a shutdownMicroprocess message is sent to the \"control\" inbox, it
    will be sent on out of the \"signal\" outbox once all children have
    terminated.
-   If a graphline\'s \"control\" inbox and \"signal\" outbox are not
    specified to be wired to a child component in the graphline then, if
    a any non shutdownMicroprocess message is sent to the \"control\"
    inbox, a producerFinished message will be sent on out of the
    \"signal\" outbox once all children have terminated.
-   If a graphline\'s \"control\" inbox is specified to be wired to a
    child component, but its \"signal\" outbox is not then, irrespective
    of what message (eg. shutdownMicroprocess) is sent to the
    \"control\" inbox, a producerFinished message will be sent on out of
    the \"signal\" outbox once all children have terminated.
-   If a graphline\'s \"control\" inbox is not specified to be wired to
    a child component in the graphline, then any message (including
    shutdown messages) flows to the \"control\" inbox of all children
    without linkages going to their \"control\" inbox only.
-   If a graphline\'s \"control\" inbox is specified to be wired to a
    child component in the graphline, then any message (including
    shutdown messages) flow along that linkage only.
-   Several linkages can be specified between components. They will all
    be created, and messages will be able to flow along them once the
    graphline is activated and run. Data will only flow along the
    specified linkages and will not leak anywhere else!
-   Instantiating a graphline with no arguments results in a ValueError
    exception
-   If a linkage is specified whose source is (X, \"inbox\") or (X,
    \"control\") where X is not the name given to one of the child
    components in the graphline, then the linkage created is a
    passthrough from that named inbox of the graphline to the specified
    destination child component in the graphline.
-   If a linkage is specified whose source is (X, Y) where X is not the
    name given to one of the child components in the graphline and Y is
    neither \"inbox\" nor \"control\", then an inbox with name Y is
    created and the linkage created is a passthrough from that named
    inbox of the graphline to the specified destination child component
    in the graphline.
-   If a linkage is specified whose destination is (X, \"outbox\") or
    (X, \"signal\") where X is not the name given to one of the child
    components in the graphline, then the linkage created is a
    passthrough from the specified source child component in the
    graphline to that named outbox of the graphline.
-   If a linkage is specified whose destination is (X, Y) where X is not
    the name given to one of the child components in the graphline and Y
    is neither \"outbox\" nor \"signal\", then an outbox with name Y is
    created and the linkage created is a passthrough from the specified
    source child component in the graphline to that named outbox of the
    graphline.
-   Graphline will terminate when all of its children have terminated,
    but not before.
-   Instantiating a graphline, components specified as named arguments,
    eg. A=component() and B=component() will not be children of the
    graphline before it is activated and run
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.Graphline.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class Graphline([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Graphline}
-------------------------------------------------------------------------------------------------

Graphline(linkages,\*\*components) -\> new Graphline component

Encapsulates the specified set of components and wires them up with the
specified linkages.

Keyword arguments:

-   linkages \-- dictionary mapping (\"componentname\",\"boxname\") to
    (\"componentname\",\"boxname\")
-   components \-- dictionary mapping names to component instances
    (default is nothing)

::: {.section}
### [Inboxes]{#symbol-Graphline.Inboxes}

-   **control** :
-   **inbox** :
:::

::: {.section}
### [Outboxes]{#symbol-Graphline.Outboxes}

-   **outbox** :
-   **signal** :
-   **\_cs** : For signaling to subcomponents shutdown
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
#### [\_\_init\_\_(self, linkages, \*\*components)]{#symbol-Graphline.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addExternalPostboxes(self)]{#symbol-Graphline.addExternalPostboxes}

Adds to self.Inboxes and self.Outboxes any postboxes mentioned in
self.layout that don\'t yet exist
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Graphline.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Graphline.main}

Main loop.
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
