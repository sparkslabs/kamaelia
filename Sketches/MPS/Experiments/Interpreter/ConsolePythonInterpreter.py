#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import *

from PythonInterpreter import InterpreterTransformer

Pipeline(
    ConsoleReader(),
    InterpreterTransformer(),
    ConsoleEchoer(),
).run()

