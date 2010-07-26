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
from Axon.Ipc import producerFinished, shutdownMicroprocess

try:
    import usb.core
    import usb.util
except Exception, e:
    print("SMART Board controls require PyUSB")

class SmartBoard(Axon.Component.component):
    
    colours = { "black" :  (0,0,0), 
            "red" :    (192,0,0),
            "green" :  (0,192,0),
            "blue": (0,0,255),
          }
    Outboxes = { "colour" : "colour selected",
            "erase" : "eraser selected",
            "toTicker" : "data to ticker",
          }
          
    def __init__(self):
        super(SmartBoard,self).__init__()
        
    def main(self):
        yield 1
        try:
            dev = usb.core.find(idVendor=0x0b8c,idProduct=0x0001)
            if dev is None:
                self.send("CLRTKR", "toTicker")
                self.send("SMART Board not detected", "toTicker")
            else:
                datain = [0xe1,0x05,0x10,0x00] # Example
                recval = datain[2]
                if (recval == 0x00):
                    # No tool selected
                    self.send(colours["black"],"colour")
                elif (recval == 0x01):
                    # Blue pen
                    self.send(colours["blue"],"colour")
                elif (recval == 0x02):
                    # Green pen
                    self.send(colours["green"],"colour")
                elif (recval == 0x04):
                    # Eraser
                    self.send("erase","erase")
                elif (recval == 0x08):
                    # Red pen
                    self.send(colours["red"],"colour")
                elif (recval == 0x10):
                    # Black pen
                    self.send(colours["black"],"colour")
        except Exception, e:
            pass
