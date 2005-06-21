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

import Axon

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Util.Chooser import Chooser


import os

path = "/home/matteh/Kamaelia presentation"
extn = ".png"
files = os.listdir(path)
files = [ os.path.join(path,fname) for fname in files if fname[-len(extn):]==extn ]

chooser = Chooser(items = files).activate()
image = Image(size=(780,540), position=(8,48)).activate()

bnext  = Button(caption="Next", msg="NEXT", position=(72,8)).activate()
bprev  = Button(caption="Previous", msg="PREV",position=(8,8)).activate()
bfirst = Button(caption="First", msg="FIRST",position=(256,8)).activate()
blast  = Button(caption="Last", msg="LAST",position=(320,8)).activate()

bnext.link(  (bnext, "outbox"),  (chooser, "inbox") )
bprev.link(  (bprev, "outbox"),  (chooser, "inbox") )
bfirst.link( (bfirst, "outbox"), (chooser, "inbox") )
blast.link(  (blast, "outbox"),  (chooser, "inbox") )

chooser.link( (chooser, "outbox"), (image, "inbox") )

Axon.Scheduler.scheduler.run.runThreads()  