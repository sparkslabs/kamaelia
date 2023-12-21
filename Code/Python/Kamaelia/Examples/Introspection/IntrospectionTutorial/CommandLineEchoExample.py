#!/usr/bin/python
# -*- coding: utf-8 -*-

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

Pipeline(
    ConsoleReader(),
    ConsoleEchoer(),
).run()

