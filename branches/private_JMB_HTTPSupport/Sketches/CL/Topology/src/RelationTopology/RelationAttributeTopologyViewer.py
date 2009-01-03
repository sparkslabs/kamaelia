#!/usr/bin/env python

"""\
==================================================================
Draw Color Topology for relation definition received from RelationParser
==================================================================
"""

import sys

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline

from Util.RelationAttributeParsing import RelationAttributeParser
from Util.GenericTopologyViewer import GenericTopologyViewer

if len(sys.argv)==1:
    print "Please type the command you want to draw"
    # ConsoleReader->lines_to_tokenlists->TopologyViewer
    Pipeline(
        ConsoleReader(">>> "),
        lines_to_tokenlists(),
        GenericTopologyViewer(),
        ConsoleEchoer(),
    ).run()
else:
    # Data can be from DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader(),
        FILEREADER = ReadFileAdaptor(sys.argv[1]),
        PARSER = RelationAttributeParser(),
        TOKENS = lines_to_tokenlists(),
        VIEWER = GenericTopologyViewer(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("PARSER","inbox"),
        ("FILEREADER","outbox") : ("PARSER","inbox"),
        ("PARSER","outbox") : ("TOKENS","inbox"),
        ("TOKENS","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
        
    }
    ).run()
