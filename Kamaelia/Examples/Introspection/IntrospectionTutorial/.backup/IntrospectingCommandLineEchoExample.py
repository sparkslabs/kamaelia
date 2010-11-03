#!/usr/bin/python
# -*- coding: utf-8 -*-

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import *

# ------- START OF CODE FRAGMENT NEEDED TO CONNECT TO INTROSPECTOR ----
# Remember to start Kamaelia/Tools/AxonVisualiser before doing this.
# cd Kamaelia/Tools
# ./AxonVisualiser.py --port=1600
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient

Pipeline(
    Introspector(),
    TCPClient("127.0.0.1", 1600),
).activate()
# ------- END OF CODE FRAGMENT NEEDED TO CONNECT TO INTROSPECTOR ----

Pipeline(
    ConsoleReader(),
    ConsoleEchoer(),
).run()

