#!/usr/bin/python

import sys
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Console import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.ER.ERVisualiserServer import ERVisualiser
from Kamaelia.Experimental.ERParsing import ERParser,ERModel2Visualiser

Backplane("TOPOLOGY").activate()

Pipeline(
    ConsoleReader(">>> "),
    PublishTo("TOPOLOGY"),
).activate()

if len(sys.argv)> 1:
    Pipeline(
        ReadFileAdaptor(sys.argv[1]),
        ERParser(),
        ERModel2Visualiser(),
        PublishTo("TOPOLOGY"),
    ).activate()

Pipeline(
    SubscribeTo("TOPOLOGY"),
    lines_to_tokenlists(),
    ERVisualiser(screensize = (1024,768), fullscreen = True),
    ConsoleEchoer(),

).run()



