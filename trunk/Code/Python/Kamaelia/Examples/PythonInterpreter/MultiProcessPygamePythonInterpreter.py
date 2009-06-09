#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

from Kamaelia.Experimental.PythonInterpreter import InterpreterTransformer

from Axon.experimental.Process import ProcessPipelineComponent

ProcessPipelineComponent(
    Textbox(size = (800, 300), position = (100,380)),
    InterpreterTransformer(),
    TextDisplayer(size = (800, 300), position = (100,40)),
).run()
