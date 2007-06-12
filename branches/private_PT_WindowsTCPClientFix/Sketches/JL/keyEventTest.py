from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Kamaelia.Util.Console import ConsoleEchoer

Graphline( output = ConsoleEchoer(),
           keys = KeyEvent( key_events={ 49: (1,"numbers"),
                                         50: (2,"numbers"),
                                         51 : (3,"numbers"),
                                         97 : ("A", "letters"),
                                         98 : ("B", "letters"),
                                         99 : ("C", "letters"),
                                       },
                            outboxes={ "numbers" : "numbers between 1 and 3",
                                       "letters" : "letters between A and C",
                                     }
                          ),
           linkages = { ("keys","numbers"):("output","inbox"),
                        ("keys","letters"):("output","inbox")
                      }
         ).run()

#notes: provide an entry in key_events for relevant keys. 
# - keycode for escape key is 27.
# - where are variables K_1, K_a, etc supposed to come from?
# - link KeyEvent to the component that cares about key events
# 	- (nameOfKeyEvent, outboxName) : (nameOfOtherComponent, inboxName)
