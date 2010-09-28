#!/usr/bin/python
"""
This is an example of how to badly re-use a pre-existing component/data
source.  In particular, this code will only work under very low loads, and
fail with a cryptic traceback under load. See the google group for details:

http://groups.google.com/group/kamaelia/msg/b74ce32469f24b26
"""

from Kamaelia.Apps.SA.Time import PeriodicTick
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

X = Pipeline(
      PeriodicTick(delay=0.5, tick_mesg="Yes"),
).activate()

def myProtocol(**argd):
    return X


FastRestartServer(protocol= myProtocol, port=1500).run()
