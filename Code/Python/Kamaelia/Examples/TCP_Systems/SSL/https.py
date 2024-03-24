#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.OneShot import OneShot

print( """
This is a simple demonstration program that shows that it is possible to
build simple clients for manually connecting to SSL based sources - such
as HTTPS sources.

This program connects the the subversion server for Kamaelia on port
443 on sourceforge - ie on kamaelia.svn.sourceforge.net. When you are
connected you are connected through an encrypted connection, which means
you could type the following and get code back from the server:

GET /Home.html HTTP/1.0
Host: kamaelia.org

That's pretty much the purpose of this example program.
""")

Graphline(
    MAKESSL = OneShot(" make ssl "), # The actual message here is not necessary
    CONSOLE = ConsoleReader(),
    ECHO = ConsoleEchoer(),
    CONNECTION = TCPClient("kamaelia.org", 443),
    linkages = {
        ("MAKESSL", "outbox"): ("CONNECTION", "makessl"),
        ("CONSOLE", "outbox"): ("CONNECTION", "inbox"),
        ("CONSOLE", "signal"): ("CONNECTION", "control"),
        ("CONNECTION", "outbox"): ("ECHO", "inbox"),
        ("CONNECTION", "signal"): ("ECHO", "control"),
    }
).run()
