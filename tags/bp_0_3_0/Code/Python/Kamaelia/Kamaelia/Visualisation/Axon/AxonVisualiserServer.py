#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import Kamaelia.Visualisation.PhysicsGraph
#from Visualisation import TopologyViewerServer

_TopologyViewerServer = Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer

from PComponent import PComponent
from PPostbox import PPostbox
from AxonLaws import AxonLaws
from ExtraWindowFurniture import ExtraWindowFurniture

class AxonVisualiserServer(_TopologyViewerServer):

    def __init__(self, **dictArgs):
        particleTypes = { "component" : PComponent,
                          "inbox"     : PPostbox.Inbox,
                          "outbox"    : PPostbox.Outbox
                        }
                        
        super(AxonVisualiserServer,self).__init__( particleTypes = particleTypes,
                                                   laws = AxonLaws(),
                                                   simCyclesPerRedraw = 3,
                                                   extraDrawing = ExtraWindowFurniture(),
                                                   **dictArgs
                                                 )
