#!/usr/bin/python
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
#

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Chooser_jlei import Chooser
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Axon.Ipc import producerFinished, shutdownMicroprocess

import os

path = "Slides"
extn = ".gif"
allfiles = os.listdir(path)
files = list()
K_esc = 27
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))

files.sort()

g = Graphline(
     CHOOSER = Chooser(items = files),
     IMAGE = Image(size=(800,600), position=(8,48)),
     NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
     PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
     FIRST = Button(caption="First", msg="FIRST",position=(256,8)),
     LAST = Button(caption="Last", msg="LAST",position=(320,8)),
     RANDOM = Button(caption="Random", msg="RANDOM", position=(500,8)), 
     #KeyEvent stuff
     keys = KeyEvent( key_events = {K_esc: (shutdownMicroprocess(), "outbox")}),
     output = ConsoleEchoer(),
     
     linkages = {
        ("NEXT","outbox") : ("CHOOSER","inbox"),
        ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
        ("FIRST","outbox") : ("CHOOSER","inbox"),
        ("LAST","outbox") : ("CHOOSER","inbox"),
	("RANDOM", "outbox") : ("CHOOSER", "inbox"),
        ("CHOOSER","outbox") : ("IMAGE","inbox"),
#	("keys", "outbox") : ("output", "inbox")
        ("keys", "outbox") : ("IMAGE", "control")
     }
)

g.run()

# 6 May 2007 -- escape message isn't being sent to Chooser inbox
# 14 May 2007 -- closes pygame window, but not cleanly.

