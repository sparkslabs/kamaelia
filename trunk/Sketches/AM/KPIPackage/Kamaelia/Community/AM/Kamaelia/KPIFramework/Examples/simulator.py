#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
"""
Simulator program shows two users connected to KPIServer
"""


import Axon
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import *

from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Server.KPIServer import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Client.KPIClient import KPIClient
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI
#from Kamaelia.Util.ConsoleEcho import consoleEchoer

#A text streaming source
class MyDataSource(Axon.Component.component):
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


#prints received text 
class MyDataSink(Axon.Component.component):
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                print "datasink received:", self.recv("inbox")

#client simulation
kpidb = KPIDBI.getDB("mytree")

#start the KPI server
KPIServer(MyDataSource(), kpidb.getKPIKeys())


#client representing user1 connects to the KPI server
Graphline(
    #c=KPIClient("user1", consoleEchoer()),
    c=KPIClient("user1", MyDataSink()),
    cc = clientconnector(),
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).activate()

#client representing user3 connects to the KPI server
Graphline(
    #c=KPIClient("user3", consoleEchoer()),
    c=KPIClient("user3", MyDataSink()),    
    cc = clientconnector(),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).run()
