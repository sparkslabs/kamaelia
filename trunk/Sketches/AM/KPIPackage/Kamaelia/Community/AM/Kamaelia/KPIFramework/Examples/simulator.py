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
=========================================
Example Showing Usage of the KPIFramework
========================================
This is a simulator program shows two users connected to KPIServer.

How does it work ?
------------------
The Client and the Client Connector communicate through the KPIFramework. 
In this example, they are directly connected (without a network)
Prerequisite: The dbfile and sample users have to be created.
"""


import Axon
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import *

from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Server.KPIServer import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Client.KPIClient import KPIClient
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI
#from Kamaelia.Util.ConsoleEcho import consoleEchoer

class MyDataSource(Axon.Component.component):
    """ A text streaming source that generates sequence
    of numbered hello strings
    """
    def main(self):
        index = 0
        while 1:
            yield 1
            if index % 1000 == 0:
                data = str(index) + "-helloknr"
                self.send(data, "outbox")
                print "data source sent", data
            else:
                yield 1
            index = index + 1


class MyDataSink(Axon.Component.component):
    """ prints received text
    """    
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                print "datasink received:", self.recv("inbox")


""" client simulation """

"""Create KPIDB instance"""
kpidb = KPIDBI.getDB("mytree")
""" start the KPI server """
KPIServer(MyDataSource(), kpidb.getKPIKeys())


""" client representing user1 connects to the KPI server"""
Graphline(
    #c=KPIClient("user1", consoleEchoer()),
    c=KPIClient("user1", MyDataSink()),
    cc = clientconnector(),
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).activate()

""" client representing user3 connects to the KPI server """
Graphline(
    #c=KPIClient("user3", consoleEchoer()),
    c=KPIClient("user3", MyDataSink()),    
    cc = clientconnector(),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).run()
