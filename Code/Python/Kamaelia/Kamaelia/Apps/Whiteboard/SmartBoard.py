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

# NOTE: This is a purely experimental component. It intends to gain control over SMART boards and hence pass on
# details of when a particular colour of pen, or the eraser has been picked up from the board. Whilst the output
# of the board has been watched to identify the hex codes corresponding to each pen, the facility to connect to
# the board and read these messages does not currently work. This component if not commented further as the chances
# are several of the trial methods are likely to be totally useless.

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess # Experimental component - loop not yet implemented

try:
    import usb.core
    import usb.util
except Exception:
    print("SMART Board controls require PyUSB")
    # Tested with version 1.0.0-a0

class SmartBoard(Axon.Component.component):
    
    colours = { "black" :  (0,0,0), 
                "red" :    (192,0,0),
                "green" :  (0,192,0),
                "blue": (0,0,255),
              }
    Inboxes = { "inbox" : "Unused",
                "control" : "",
              }
    Outboxes = { "outbox" : "Unused",
                 "signal" : "",
                 "colour" : "colour selected",
                 "erase" : "eraser selected",
                 "toTicker" : "data to ticker",
                }

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1
        
    def main(self):
        # Loop not added yet as it doesn't work

        # idVendor and idProduct found by watching dmesg when plugging in SMART board
        # These should be the same for all boards of the type being tested
        dev = usb.core.find(idVendor=0x0b8c,idProduct=0x0001)
        interface = dev.get_interface_altsetting()
        if dev.is_kernel_driver_active(interface.bInterfaceNumber):
            print("Detaching kernel driver")
            dev.detach_kernel_driver(interface.bInterfaceNumber)


        dev.set_configuration(1)

        for cfg in dev:
            print("Config")
            print (cfg.bConfigurationValue)
            for i in cfg:
                print("Interface")
                print (i.bInterfaceNumber)
                for e in i:
                    print ("Endpoint")
                    print (e.bEndpointAddress)
                    print (usb.util.endpoint_direction(e.bEndpointAddress))

        # get an endpoint instance
        epin = usb.util.find_descriptor(
        dev.get_interface_altsetting(),   # first interface
        # match the first IN endpoint
        custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_IN
        )
        assert epin is not None
        # get an endpoint instance
        epout = usb.util.find_descriptor(
        dev.get_interface_altsetting(),   # first interface
        # match the first OUT endpoint
        custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT
        )

        assert epout is not None
        print(epin)
        print(epout)
        # write the data
        # These are all numbers guessed having watched the SMART board's diagnostic utility output when plugging in the board.
        epout.write([0xd2,0x02,0x04,0x00,0xd4,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        epout.write([0xd2,0x02,0x10,0x10,0xd0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        epout.write([0xd2,0x02,0x04,0x00,0xd4,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        epout.write([0xc3,0x80,0x01,0x00,0x03,0x41,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        print(epin.read(32))
        epout.write([0xd2,0x02,0x80,0x80,0xd0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        print(epin.read(32))
        print(epin.read(32))
        epout.write([0xf0,0x0e,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        print(epin.read(32))
        epout.write([0xf0,0x0e,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        print(epin.read(32))
        epout.write([0xf0,0x0e,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        print(epin.read(32))



        if dev is None:
            self.send(chr(0) + "CLRTKR", "toTicker")
            self.send("SMART Board not detected", "toTicker")
        else:
            self.send(chr(0) + "CLRTKR", "toTicker")
            self.send("SMART Board initialised", "toTicker")
            datain = [0xe1,0x05,0x10,0x00] # Example
            recval = datain[2]
            if (recval == 0x00):
                # No tool selected
                self.send(self.colours["black"],"colour")
                self.send(chr(0) + "CLRTKR", "toTicker")
                self.send("SMART: No tools selected, assuming black pen", "toTicker")
            elif (recval == 0x01):
                # Blue pen
                self.send(self.colours["blue"],"colour")
                self.send(chr(0) + "CLRTKR", "toTicker")
                self.send("SMART: Blue pen selected", "toTicker")
            elif (recval == 0x02):
                # Green pen
                self.send(self.colours["green"],"colour")
                self.send(chr(0) + "CLRTKR", "toTicker")
                self.send("SMART: Green pen selected", "toTicker")
            elif (recval == 0x04):
                # Eraser
                self.send("erase","erase")
                self.send(chr(0) + "CLRTKR", "toTicker")
                self.send("SMART: Eraser selected", "toTicker")
            elif (recval == 0x08):
                # Red pen
                self.send(self.colours["red"],"colour")
                self.send(chr(0) + "CLRTKR", "toTicker")
                self.send("SMART: Red pen selected", "toTicker")
            elif (recval == 0x10):
                # Black pen
                self.send(self.colours["black"],"colour")
                self.send(chr(0) + "CLRTKR", "toTicker")
                self.send("SMART: Black pen selected", "toTicker")

        yield 1