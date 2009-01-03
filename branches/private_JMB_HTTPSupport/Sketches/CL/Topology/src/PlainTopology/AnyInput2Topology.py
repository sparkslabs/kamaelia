#!/usr/bin/env python

"""\
===================================================
Draw Topology from either Console Command or a file
===================================================

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

import sys

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Chassis.Pipeline import Pipeline

if len(sys.argv)==1:
    print "Please type the command you want to draw"
    # ConsoleReader->lines_to_tokenlists->TopologyViewer
    Pipeline(
        ConsoleReader(">>> "),
        lines_to_tokenlists(),
        TopologyViewer(),
    ).run()
else:
    # ReadFileAdaptor->lines_to_tokenlists->TopologyViewer
    Pipeline(
        ReadFileAdaptor(filename=sys.argv[1], readmode="line"),
        lines_to_tokenlists(),
        #ConsoleEchoer()
        TopologyViewer(),
        ConsoleEchoer(),
    ).run()    


