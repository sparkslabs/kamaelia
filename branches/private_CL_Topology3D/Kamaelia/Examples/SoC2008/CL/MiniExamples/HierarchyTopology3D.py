#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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


from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
from Kamaelia.Chassis.Graphline import Graphline

from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D import TopologyViewer3D


# Data can be from both DataSource and console inputs
print "Please type the command you want to draw"
Graphline(
    CONSOLEREADER = ConsoleReader(">>> "),
    DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos teapot',
                             'ADD NODE 2Node 2Node randompos -',
                             'ADD NODE 3Node 3Node randompos sphere', 'ADD NODE 4Node 4Node randompos -',
                             'ADD NODE 5Node 5Node randompos sphere', 'ADD NODE 6Node 6Node randompos -',
                             'ADD NODE 7Node 7Node randompos sphere',
                             'ADD LINK 1Node 2Node',
                             'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                             'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node',
                             'ADD NODE 1Node:1Node 1Node:1Node randompos -', 'ADD NODE 1Node:2Node 1Node:2Node randompos -',
                             'ADD NODE 1Node:3Node 1Node:3Node randompos -', 'ADD NODE 1Node:4Node 1Node:4Node randompos -',
                             'ADD LINK 1Node:1Node 1Node:2Node', 'ADD LINK 1Node:2Node 1Node:3Node',
                             'ADD LINK 1Node:3Node 1Node:4Node', 'ADD LINK 1Node:4Node 1Node:1Node',
                             'ADD NODE 1Node:1Node:1Node 1Node:1Node:1Node randompos -',
                             'ADD NODE 1Node:1Node:2Node 1Node:1Node:2Node randompos -',
                             'ADD LINK 1Node:1Node:1Node 1Node:1Node:2Node',
                             'ADD NODE 5Node:1Node 5Node:1Node randompos sphere',
                             'ADD NODE 5Node:2Node 5Node:2Node randompos sphere',
                             'ADD LINK 5Node:1Node 5Node:2Node'
                             ]),
    TOKENS = lines_to_tokenlists(),
    VIEWER = TopologyViewer3D(),
    CONSOLEECHOER = ConsoleEchoer(),
linkages = {
    ("CONSOLEREADER","outbox") : ("TOKENS","inbox"),
    ("DATASOURCE","outbox") : ("TOKENS","inbox"),
    ("TOKENS","outbox")   : ("VIEWER","inbox"),
    ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()