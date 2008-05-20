#!/usr/bin/env python

"""\
==================================================================
Draw Topology for relation definition received from RelationParser
==================================================================
"""

import sys

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

from Util.RelationParsing import RelationParser

if len(sys.argv)> 1:
    Pipeline(
        ReadFileAdaptor(sys.argv[1]),
        RelationParser(),
        lines_to_tokenlists(),
        TopologyViewer(),
        ConsoleEchoer(),
    ).run()
