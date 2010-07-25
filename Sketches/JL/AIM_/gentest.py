#!/usr/bin/env python
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
