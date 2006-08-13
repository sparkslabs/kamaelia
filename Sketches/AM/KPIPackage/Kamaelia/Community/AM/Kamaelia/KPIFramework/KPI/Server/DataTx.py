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
The Data Transmitter packetises the data. The data being transmitted could be
encrypted data packets or key packets encrypted with common keys. The DataTx
adds a header specifying key type and packet length
"""

import Axon
import struct

class DataTx(Axon.Component.component):
    Inboxes = {"inbox" : "data to be encrypted",
               "keyIn" : "key updates"}

    def __init__(self):
        super(DataTx,self).__init__()

    def main(self):
        KEY = 0x20
        DATA = 0x30
        while 1:
            while self.dataReady("keyIn"):
                data = self.recv("keyIn")
                header = struct.pack("!2L", KEY, len(data))
                packet = header + data
                print "DataTx", packet
                self.send(packet, "outbox")
            yield 1

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                header = struct.pack("!2L", DATA, len(data))
                packet = header + data
                print "DataTx", packet
                self.send(packet, "outbox")
            yield 1
