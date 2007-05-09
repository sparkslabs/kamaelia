#!/usr/bin/env python

from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

Pipeline(ConsoleReader(">>> ", ""),SimpleHTTPClient(),ConsoleEchoer()).run()
