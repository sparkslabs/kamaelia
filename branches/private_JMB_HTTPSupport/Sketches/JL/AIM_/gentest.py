#!/usr/bin/env python
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from gen import *
import sys
sys.path.append('..')
from likefile import *

g = \
Graphline(auth = AuthCookieGetter(),
          oscar = OSCARClient('login.oscar.aol.com', 5190),
          cons = ConsoleEchoer(),
          linkages = {("auth", "outbox") : ("oscar", "inbox"),
                      ("oscar", "outbox") : ("auth", "inbox"),
                      ("auth", "signal") : ("oscar", "control"),
                      ("auth", "_cookie") : ("self", "outbox"),
                      }
          ) 

background = schedulerThread(slowmo=0.01).start()
h = LikeFile(g)
h.activate()
cookie = h.get()
print cookie
