#!/usr/bin/python

from Kamaelia.Util.Console import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Reading import SimpleReader
from Kamaelia.Util.RateFilter import MessageRateLimit

Pipeline(
    SimpleReader("/etc/fstab"),
    ConsoleEchoer(),
).run()


Pipeline(
    SimpleReader("/etc/fstab"),
    MessageRateLimit(2,1,hardlimit=0),
    ConsoleEchoer(),
).run()

Pipeline(
    SimpleReader("/etc/fstab"),
    MessageRateLimit(0.5,1,hardlimit=1),
    ConsoleEchoer(),
).run()

