#!/usr/bin/python

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.OneShot import OneShot

print """
This is a simple demonstration program that shows that it is possible to
build simple clients for manually connecting to SSL based sources - such
as HTTPS sources.

This program connects the the subversion server for Kamaelia on port
443 on sourceforge - ie on kamaelia.svn.sourceforge.net. When you are
connected you are connected through an encrypted connection, which means
you could type the following and get code back from the server:

GET /svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses HTTP/1.0
Host: kamaelia.svn.sourceforge.net

That's pretty much the purpose of this example program.
"""

Graphline(
    MAKESSL = OneShot(" make ssl "), # The actual message here is not necessary
    CONSOLE = ConsoleReader(),
    ECHO = ConsoleEchoer(),
    CONNECTION = TCPClient("kamaelia.svn.sourceforge.net", 443),
    linkages = {
        ("MAKESSL", "outbox"): ("CONNECTION", "makessl"),
        ("CONSOLE", "outbox"): ("CONNECTION", "inbox"),
        ("CONSOLE", "signal"): ("CONNECTION", "control"),
        ("CONNECTION", "outbox"): ("ECHO", "inbox"),
        ("CONNECTION", "signal"): ("ECHO", "control"),
    }
).run()
