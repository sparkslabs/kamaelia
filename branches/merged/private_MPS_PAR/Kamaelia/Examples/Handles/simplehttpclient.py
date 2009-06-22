#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.background import background
from Axon.Handle import Handle
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
background = background().start()
import time
import Queue

p = Handle(SimpleHTTPClient()).activate()
p.put("http://google.com","inbox")
p.put("http://slashdot.org","inbox")
p.put("http://whatismyip.org","inbox")

def get_item(handle):
   while 1:
      try:
          item = handle.get("outbox")
          break
      except Queue.Empty:
          time.sleep(0.05)
   return item

google = get_item(p)
slashdot = get_item(p)
whatismyip = get_item(p)

print "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long. Also, our IP address is:", whatismyip

time.sleep(5)