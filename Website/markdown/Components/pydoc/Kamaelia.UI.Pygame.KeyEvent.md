---
pagename: Components/pydoc/Kamaelia.UI.Pygame.KeyEvent
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.html){.reference}
=======================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.KeyEvent.html){.reference}**
:::

-   [Pygame keypress event handler](#371){.reference}
    -   [Example Usage](#372){.reference}
    -   [How does it work?](#373){.reference}
:::

::: {.section}
Pygame keypress event handler {#371}
=============================

A component that registers with a Pygame Display service component to
receive key-up and key-down events from Pygame. You can set up this
component to send out different messages from different outboxes
depending on what key is pressed.

::: {.section}
[Example Usage]{#example-usage} {#372}
-------------------------------

Capture keypresses in pygame for numbers 1,2,3 and letters a,b,c:

``` {.literal-block}
fom pygame.locals import *

Graphline( output = ConsoleEchoer(),
           keys = KeyEvent( key_events={ K_1 : (1,"numbers"),
                                         K_2 : (2,"numbers"),
                                         K_3 : (3,"numbers"),
                                         K_a : ("A", "letters"),
                                         K_b : ("B", "letters"),
                                         K_c : ("C", "letters"),
                                       },
                            outboxes={ "numbers" : "numbers between 1 and 3",
                                       "letters" : "letters between A and C",
                                     }
                          ),
           linkages = { ("keys","numbers"):("output","inbox"),
                        ("keys","letters"):("output","inbox")
                      }
         ).run()
```

The symbols *K\_1*, *K\_2*, etc are keycodes defined in defined in
*pygame.locals*.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#373}
--------------------------------------

This component requests a zero sized display surface from the Pygame
Display service component and registers to receive events from pygame.

Whenever a KEYDOWN event is received, the pygame keycode is looked up in
the mapping you specified. If it is there, then the specified message is
sent out of the specified outbox.

In addition, if the allKeys flag was set to True during initialisation,
then any KEYDOWN or KEYUP event will result in a (\"DOWN\",keycode) or
(\"UP\",keycode) message being sent to the \"allkeys\" outbox.

If you have specified a message to send for a particular key, then both
that message and the \'all-keys\' message will be sent when the KEYDOWN
event occurs.

If this component receives a shutdownMicroprocess or producerFinished
message on its \"control\" inbox, then this will be forwarded out of its
\"signal\" outbox and the component will then terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.html){.reference}.[KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.KeyEvent.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================

::: {.section}
class KeyEvent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-KeyEvent}
------------------------------------------------------------------------------------------------

KeyEvent(\[allkeys\]\[,key\_events\]\[,outboxes\]) -\> new KeyEvent
component.

Component that sends out messages in response to pygame keypress events.

Keyword arguments:

-   allkeys \-- if True, all keystrokes send messages out of \"allkeys\"
    outbox (default=False)
-   key\_events \-- dict mapping pygame keycodes to (msg,\"outboxname\")
    pairs (default=None)
-   outboxes \-- dict of \"outboxname\":\"description\" key:value pairs
    (default={})

::: {.section}
### [Inboxes]{#symbol-KeyEvent.Inboxes}

-   **control** : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   **callback** : Receive callbacks from Pygame Display
-   **inbox** : Receive events from Pygame Display
:::

::: {.section}
### [Outboxes]{#symbol-KeyEvent.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   **allkeys** : Outbox that receives \*every\* keystroke if enabled
-   **display\_signal** : Outbox used for communicating to the display
    surface
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
#### [\_\_init\_\_(self\[, allkeys\]\[, key\_events\]\[, key\_up\_events\]\[, outboxes\])]{#symbol-KeyEvent.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-KeyEvent.main}

Main loop.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-KeyEvent.waitBox}

Generator. yields 1 until data is ready on the named inbox.
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
