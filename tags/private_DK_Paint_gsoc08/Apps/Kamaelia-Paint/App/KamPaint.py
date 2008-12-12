#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

from pygame.locals import *
from Axon.experimental.Process import ProcessGraphline

from Kamaelia.Chassis.Seq import Seq

from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.Apps.Paint.ToolBox import ToolBox
from Kamaelia.Apps.Paint.Core import DisplayConfig
from Kamaelia.Apps.Paint.Core import Paint

ProcessGraphline(
     COLOURS = Seq(
          DisplayConfig(width=270, height=600),
          ToolBox(size=(270, 600)),
          ),

     WINDOW1 = Seq(
               DisplayConfig(width=555, height=520),
               Paint(bgcolour=(100,100,172),position=(10,10), size = (500,500), transparent = False),
                ),
      linkages = {
          ("COLOURS", "outbox") : ("WINDOW1", "inbox"),
      }
).run()
# Licensed to the BBC under a Contributor Agreement: THF/DK
