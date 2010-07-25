# -*- coding: utf-8 -*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
