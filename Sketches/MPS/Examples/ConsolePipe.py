#!/usr/bin/python

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.UnixProcess import UnixProcess
from Kamaelia.Chassis.Pipeline import Pipeline

Pipeline(
    ConsoleReader(),
    UnixProcess("/home/zathras/tmp/rules_test.py"),
    ConsoleEchoer(),
).run()