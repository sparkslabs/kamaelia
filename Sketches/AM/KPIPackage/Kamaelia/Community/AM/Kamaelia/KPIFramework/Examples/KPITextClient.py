#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#

"""
====================================
KPI Client that recieves and prints text data
====================================

How does it work?
-----------------
The KPITextClient establishes TCP connection with the
KPITextServer. Upon successful authentication,
receives session key and uses session key decrypt the
encrypted stream. The decrypted stream is printed by
MyDataSink component
"""

import Axon
from Kamaelia.Util.Graphline import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Server.KPIServer import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Client.KPIClient import KPIClient
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient

#from Kamaelia.Util.ConsoleEcho import consoleEchoer


class MyDataSink(Axon.Component.component):
    """ prints received text
    """     
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                print "datasink received:", self.recv("inbox")

import sys
if __name__=="__main__":
    if len(sys.argv) != 4:
        print "Usage:", sys.argv[0], "kpiserver port usercfg"
        print "default values used: kpiserver=localhost, port=1256 and usercfg = user3"
        server = "localhost"
        port = 1256
        usercfg = "user3"
    else:
        server = sys.argv[1]
        port = int(sys.argv[2])
        usercfg = sys.argv[3]

    Graphline(
        #c=KPIClient(usercfg, consoleEchoer()),
        c=KPIClient(usercfg, MyDataSink()),
        cc = _TCPClient(server,port),
        linkages = {
            ("c","outbox") : ("cc","inbox"),
            ("cc","outbox") : ("c","inbox"),
        }
    ).run()
