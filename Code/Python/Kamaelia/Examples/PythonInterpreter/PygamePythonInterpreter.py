#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

from PythonInterpreter import InterpreterTransformer

Pipeline(
    Textbox(size = (800, 300), position = (100,380)),
    InterpreterTransformer(),
    TextDisplayer(size = (800, 300), position = (100,40)),
).run()
