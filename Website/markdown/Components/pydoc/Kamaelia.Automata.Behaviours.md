---
pagename: Components/pydoc/Kamaelia.Automata.Behaviours
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}
======================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [bouncingFloat](/Components/pydoc/Kamaelia.Automata.Behaviours.bouncingFloat.html){.reference}**
-   **component
    [cartesianPingPong](/Components/pydoc/Kamaelia.Automata.Behaviours.cartesianPingPong.html){.reference}**
-   **component
    [continuousIdentity](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousIdentity.html){.reference}**
-   **component
    [continuousOne](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousOne.html){.reference}**
-   **component
    [continuousZero](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousZero.html){.reference}**
-   **component
    [loopingCounter](/Components/pydoc/Kamaelia.Automata.Behaviours.loopingCounter.html){.reference}**
:::

-   [Simple behaviours](#77){.reference}
    -   [Example Usage](#78){.reference}
    -   [More detail](#79){.reference}
:::

::: {.section}
Simple behaviours {#77}
=================

A collection of components that send to their \"outbox\" outbox, values
according to simple behaviours - such as constant value, bouncing,
looping etc.

::: {.section}
[Example Usage]{#example-usage} {#78}
-------------------------------

Generate values that bounce up and down between 0 and 1 in steps of
0.05:

``` {.literal-block}
bouncingFloat(scale_speed=0.05*10)
```

Generate (x,y) coordinates, starting at (50,50) that bounce within a
200x100 box with a 10 unit inside margin:

``` {.literal-block}
cartesianPingPong(point=(50,50), width=200, height=100, border=10)
```

Generate the angles for the seconds hand on an analog watch:

``` {.literal-block}
loopingCounter(increment=360/60, modulo=360)
```

Constantly generate the number 7:

``` {.literal-block}
continuousIdentity(original=7)
```

Constantly generate the string \"hello\":

``` {.literal-block}
continuousIdentity(original="hello")
```

Constantly generate the value 0:

``` {.literal-block}
continuousZero()
```

Constantly generate the value 1:

``` {.literal-block}
continuousOne()
```
:::

::: {.section}
[More detail]{#more-detail} {#79}
---------------------------

All components start emitting values as soon as they are activated. They
then emit values as fast as they can (there is no throttling/rate
control).

All components will terminate if they receive the string \"shutdown\" on
their \"control\" inbox. They also then send \"shutdown\" to their
\"signal\" outbox.

All components will pause and stop emitting values if they receive the
string \"pause\" on their \"control\" inbox. They will resume from where
they left off if they receive the string \"unpause\" on the same inbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[bouncingFloat](/Components/pydoc/Kamaelia.Automata.Behaviours.bouncingFloat.html){.reference}
=====================================================================================================================================================================================================================================================================================================

::: {.section}
class bouncingFloat([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-bouncingFloat}
-----------------------------------------------------------------------------------------------------

bouncingFloat(scale\_speed) -\> new bouncingFloat component

A component that emits a value that constantly bounces between 0 and 1.

scale\_speed scales the rate at which the value changes. 1.0 = tenths,
0.5 = twentieths, etc.

::: {.section}
### [Inboxes]{#symbol-bouncingFloat.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-bouncingFloat.Outboxes}
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
#### [\_\_init\_\_(self, scale\_speed)]{#symbol-bouncingFloat.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-bouncingFloat.main}

Main loop
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[cartesianPingPong](/Components/pydoc/Kamaelia.Automata.Behaviours.cartesianPingPong.html){.reference}
=============================================================================================================================================================================================================================================================================================================

::: {.section}
class cartesianPingPong([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-cartesianPingPong}
---------------------------------------------------------------------------------------------------------

cartesianPingPong(point,width,height,border) -\> new cartesianPingPong
component

A component that emits (x,y) values that bounce around within the
specified bounds.

Keyword arguments:

-   point \-- starting (x,y) coordinates
-   width, height \-- bounds of the area
-   border \-- distance in from bounds at which bouncing happens

::: {.section}
### [Inboxes]{#symbol-cartesianPingPong.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-cartesianPingPong.Outboxes}
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
#### [\_\_init\_\_(self, point, width, height, border)]{#symbol-cartesianPingPong.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-cartesianPingPong.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[continuousIdentity](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousIdentity.html){.reference}
===============================================================================================================================================================================================================================================================================================================

::: {.section}
class continuousIdentity([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-continuousIdentity}
----------------------------------------------------------------------------------------------------------

continuousIdentity(original) -\> new continuousIdentity component

A component that constantly emits the original value.

::: {.section}
### [Inboxes]{#symbol-continuousIdentity.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-continuousIdentity.Outboxes}
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
#### [\_\_init\_\_(self, original, \*args)]{#symbol-continuousIdentity.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-continuousIdentity.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[continuousOne](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousOne.html){.reference}
=====================================================================================================================================================================================================================================================================================================

::: {.section}
class continuousOne([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-continuousOne}
-----------------------------------------------------------------------------------------------------

continuousOne() -\> new continuousOne component

A component that constantly emits the value 1.

::: {.section}
### [Inboxes]{#symbol-continuousOne.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-continuousOne.Outboxes}
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
#### [\_\_init\_\_(self, \*args)]{#symbol-continuousOne.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-continuousOne.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[continuousZero](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousZero.html){.reference}
=======================================================================================================================================================================================================================================================================================================

::: {.section}
class continuousZero([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-continuousZero}
------------------------------------------------------------------------------------------------------

continuousZero() -\> new continuousZero component

A component that constantly emits the value 0.

::: {.section}
### [Inboxes]{#symbol-continuousZero.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-continuousZero.Outboxes}
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
#### [\_\_init\_\_(self, \*args)]{#symbol-continuousZero.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-continuousZero.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}.[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}.[loopingCounter](/Components/pydoc/Kamaelia.Automata.Behaviours.loopingCounter.html){.reference}
=======================================================================================================================================================================================================================================================================================================

::: {.section}
class loopingCounter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-loopingCounter}
------------------------------------------------------------------------------------------------------

loopingCounter(increment\[,modulo\]) -\> new loopingCounter component

Emits an always incrementing value, that wraps back to zero when it
reaches the specified limit.

Keyword arguments: - increment \-- increment step size - modulo \--
counter wrap back to zero before reaching this value (default=360)

::: {.section}
### [Inboxes]{#symbol-loopingCounter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-loopingCounter.Outboxes}
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
#### [\_\_init\_\_(self, increment\[, modulo\])]{#symbol-loopingCounter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-loopingCounter.main}

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
