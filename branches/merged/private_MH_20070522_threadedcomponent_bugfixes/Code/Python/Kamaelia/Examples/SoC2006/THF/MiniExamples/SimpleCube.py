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

from Kamaelia.Util.Graphline import Graphline
from Kamaelia.UI.OpenGL.SimpleCube import SimpleCube

Graphline(    
    CUBEC = SimpleCube(position=(0, 0,-12), rotation=(225,45,135), size=(1,1,1)).activate(),
    CUBER = SimpleCube(position=(4,0,-22), size=(2,2,2)).activate(),
    CUBEB = SimpleCube(position=(0,-4,-18), rotation=(0,180,20), size=(1,3,2)).activate(),
    linkages = {}
).run()
# Licensed to the BBC under a Contributor Agreement: THF
