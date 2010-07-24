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
import Axon
from Kamaelia.Util.Graphline import *
from KPI.Server.KPIServer import *
from KPI.Client.KPIClient import KPIClient
from KPI.DB import KPIDBI

class MyDataSource(Axon.Component.component):
   def main(self):
       index = 0
       while 1:
           data = str(index) + "-helloknr"
           self.send(data, "outbox")
           index = index + 1
           yield 1     


class MyDataSink(Axon.Component.component):
   def main(self):
       while 1:
           yield 1
           while self.dataReady("inbox"):
               print "datasink received:", self.recv("inbox")
           
       


#client simulation
kpidb = KPIDBI.getDB("mytree")
KPIServer(MyDataSource(), kpidb.getKPIKeys())
Graphline(
    c=KPIClient("user1", MyDataSink()),
    cc = clientconnector(kpidb),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).activate()


Graphline(
    c=KPIClient("user3", MyDataSink()),
    cc = clientconnector(kpidb),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).run()
