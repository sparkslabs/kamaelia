#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Util.PureTransformer import PureTransformer

from PythonInterpreter import InterpreterTransformer

def NetInterpreter(*args, **argv):
    return Pipeline(
                PureTransformer(lambda x: str(x).rstrip()),
                InterpreterTransformer(),
                PureTransformer(lambda x: str(x)+"\r\n>>> "),
           )

ServerCore(protocol=NetInterpreter, port=1236).run()
