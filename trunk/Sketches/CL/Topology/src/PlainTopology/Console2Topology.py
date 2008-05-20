#!/usr/bin/env python

"""\
==================================
Draw Topology from Console Command
==================================

Example Usage
-------------
1. Add one node
ADD NODE TCPClient TCPClient auto -
ADD NODE VorbisDecode VorbisDecode auto -
2. add one link
ADD LINK TCPClient VorbisDecode
3. Delete one node/ link/ all 
DEL NODE TCPClient
ADD LINK TCPClient VorbisDecode
DEL ALL
"""

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Chassis.Pipeline import Pipeline


# ConsoleReader->lines_to_tokenlists->TopologyViewer
Pipeline(
    ConsoleReader(">>> "),
    lines_to_tokenlists(),
    TopologyViewer(),
    ConsoleEchoer(),
).run()