#!/usr/bin/env python

"""\
==================================================================
Draw Color Topology for relation definition received from RelationParser
==================================================================
"""

import sys

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

from Util.RelationAttributeParsing import RelationAttributeParser
from Util.GenericTopologyViewer import GenericTopologyViewer

if len(sys.argv)> 1:
    Pipeline(
        ReadFileAdaptor(sys.argv[1]),
        RelationAttributeParser(),
        lines_to_tokenlists(),
        GenericTopologyViewer(),
        ConsoleEchoer(),
    ).run()
