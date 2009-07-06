#!/usr/bin/python

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.OneShot import OneShot

import sys


if len(sys.argv) != 3:
    print
    print "Format of usage wrong, it should be this:"
    print
    print "    ",sys.argv[0], "host", "port"
    sys.exit(0)

host = sys.argv[1]
port = int(sys.argv[2])

if 1:
    Graphline(
        MAKESSL = OneShot(" make ssl "), # The actual message here is not necessary
        CONSOLE = ConsoleReader(),
        ECHO = ConsoleEchoer(),
        CONNECTION = TCPClient(host, port),
        linkages = {
            ("MAKESSL", "outbox"): ("CONNECTION", "makessl"),
            ("CONSOLE", "outbox"): ("CONNECTION", "inbox"),
            ("CONSOLE", "signal"): ("CONNECTION", "control"),
            ("CONNECTION", "outbox"): ("ECHO", "inbox"),
            ("CONNECTION", "signal"): ("ECHO", "control"),
        }
    ).run()
