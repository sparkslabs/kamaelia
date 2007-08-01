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
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.OpenGL.Label import Label
Graphline(
    Label1 = Label(caption="That", size=(2,2,1), sidecolour=(0,200,0), position=(-3,0,-10)),
    Label2 = Label(caption="Boy", bgcolour=(200,100,0), position=(3,0,-10)),
    Label3 = Label(caption="Needs", margin=15, position=(-1,0,-10), rotation=(30,0,10)),
    Label4 = Label(caption="Therapy!", fontsize=20, size=(1.3,0.3,1), position=(1,0,-10)),
    ECHO = ConsoleEchoer(),
    linkages = {
        ("Label1", "outbox") : ("ECHO", "inbox"),
        ("Label2", "outbox") : ("ECHO", "inbox"),
        ("Label3", "outbox") : ("ECHO", "inbox"),
        ("Label4", "outbox") : ("ECHO", "inbox"),            
    }
).run()
# Licensed to the BBC under a Contributor Agreement: THF
