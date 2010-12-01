#!/usr/bin/python
# -*- coding: utf-8 -*-

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import *

Pipeline(
    ConsoleReader(),
    ConsoleEchoer(),
).run()

