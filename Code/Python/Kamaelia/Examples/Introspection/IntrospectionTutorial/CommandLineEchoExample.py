#!/usr/bin/python
# -*- coding: utf-8 -*-

# Checked: 2024/03/24

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

Pipeline(
    ConsoleReader(),
    ConsoleEchoer(),
).run()

