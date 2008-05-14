#!/usr/bin/env python

"""\
==========================================================
Draw Topology from a file which contains drawing commands
==========================================================

Example Usage
-------------
File2Topology.py yourFile
or python File2Topology.py yourFile

Commands that can be used in yourFile
---------------------------------------
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
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Chassis.Pipeline import Pipeline

#from Kamaelia.Util.Console import ConsoleEchoer

# To see if the file name is included in the arguments
if len(sys.argv)==1:
    print "Bingo! not enough inputs: please type the file name you want to draw as well"
else:
    # ReadFileAdaptor->lines_to_tokenlists->TopologyViewer
    Pipeline(
        ReadFileAdaptor(filename=sys.argv[1], readmode="line"),
        lines_to_tokenlists(),
        #ConsoleEchoer()
        TopologyViewer(),
    ).run()    