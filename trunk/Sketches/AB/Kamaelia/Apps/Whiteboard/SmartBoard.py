#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
