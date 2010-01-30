#!/usr/bin/python
'''
This file contains an example usage of Kamaelia.Apps.SA.Time.SingleTick
'''

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Apps.SA.Time import SingleTick

Pipeline(
    SingleTick(0.3),
    ConsoleEchoer(use_repr=True),
).run()

