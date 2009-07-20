#!/usr/bin/python
'''
This file contains an example of how to use Kamaelia.Apps.SA.Time.PeriodicTick
'''

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Apps.SA.Time import PeriodicTick

Pipeline(
    PeriodicTick(0.3),
    ConsoleEchoer(use_repr=True),
).run()

