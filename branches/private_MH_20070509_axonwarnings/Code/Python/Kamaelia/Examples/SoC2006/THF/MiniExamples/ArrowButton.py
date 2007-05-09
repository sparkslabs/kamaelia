#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Kamaelia.UI.OpenGL.ArrowButton import ArrowButton
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline

Graphline(
    button1 = ArrowButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
    button2 = ArrowButton(size=(2,2,1), position=(5,0,-15), rotation=(0,0,90), msg="BRAIN"),
    echo = ConsoleEchoer(),
    linkages = {
        ("button1", "outbox") : ("echo", "inbox"),
        ("button2", "outbox") : ("echo", "inbox")
    }
).run()

# Licensed to the BBC under a Contributor Agreement: THF
