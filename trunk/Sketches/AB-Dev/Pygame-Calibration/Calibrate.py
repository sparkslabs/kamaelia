#!/usr/bin/env python
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

import Axon
import sys
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Calibrate(component):
    
    Inboxes =  { "inbox"   : "select calibration",
                 "coords"  : "accept co-ordinates",
               }
    Outboxes = { "outbox"  : "send out drawing commands",
                 "finaldata" : "send out final co-ordinates",
               }
                 
    def __init__(self):
        super(Calibrate,self).__init__()
        self.globalcount = 0
        self.topleft = 0
        self.topright = 0
        self.bottomleft = 0
        self.bottomright = 0
        self.calibstarted = 0
        
    def main(self):
        while 1:
            while (self.dataReady("inbox") & (self.globalcount == 0)):
                self.recv("inbox")
                self.calibstarted = 1
                data = [["CLEAR"]]
                self.send(data,"outbox")
                data = [["WRITE",'220','300','30','255','0','0',"Please touch each + as it appears to calibrate the display"]]
                self.send(data,"outbox")
                data = [["WRITE",'10','10','50','255','0','0',"+"]]
                self.send(data,"outbox")
            while (self.dataReady("coords") & (self.globalcount == 0) & (self.calibstarted == 1)):
                coords = self.recv("coords")
                self.globalcount = 1
            while (self.dataReady("coords") & (self.globalcount == 1)):
                self.topleft = self.recv("coords")
                data = [["CLEAR"]]
                self.send(data,"outbox")
                data = [["WRITE",'220','300','30','255','0','0',"Please touch each + as it appears to calibrate the display"]]
                self.send(data,"outbox")
                data = [["WRITE",'994','10','50','255','0','0',"+"]]
                self.send(data,"outbox")
                self.globalcount = 2
            while (self.dataReady("coords") & (self.globalcount == 2)):
                self.topright = self.recv("coords")
                data = [["CLEAR"]]
                self.send(data,"outbox")
                data = [["WRITE",'220','300','30','255','0','0',"Please touch each + as it appears to calibrate the display"]]
                self.send(data,"outbox")
                data = [["WRITE",'10','698','50','255','0','0',"+"]]
                self.send(data,"outbox")
                self.globalcount = 3
            while (self.dataReady("coords") & (self.globalcount == 3)):
                self.bottomleft = self.recv("coords")
                data = [["CLEAR"]]
                self.send(data,"outbox")
                data = [["WRITE",'220','300','30','255','0','0',"Please touch each + as it appears to calibrate the display"]]
                self.send(data,"outbox")
                data = [["WRITE",'994','698','50','255','0','0',"+"]]
                self.send(data,"outbox")
                self.globalcount = 4
            while (self.dataReady("coords") & (self.globalcount == 4)):
                self.bottomright = self.recv("coords")
                data = [["CLEAR"]]
                self.send(data,"outbox")
                self.globalcount = 5
                data = [["WRITE",'190','300','30','255','0','0',"Calibration complete. Now close the program and copy the conf file"]]
                self.send(data,"outbox")
                data = [self.topleft[0][4:6],self.topright[0][4:6],self.bottomleft[0][4:6],self.bottomright[0][4:6]]
                data = ",".join(self.topleft[0][4:6]) + "," + ",".join(self.topright[0][4:6]) + "," + ",".join(self.bottomleft[0][4:6]) + "," + ",".join(self.bottomright[0][4:6])
                data = ["pygame-calibration.conf",data]
                self.send(data,"finaldata")
            while (self.dataReady("inbox") & (self.globalcount == 5)):
                data = self.recv("inbox")
                print repr("Data written to " + data)
                self.globalcount = 6
                sys.exit(0)
            yield 1
            self.pause()
            