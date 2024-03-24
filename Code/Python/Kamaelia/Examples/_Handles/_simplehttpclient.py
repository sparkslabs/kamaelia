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

from Axon.background import background
from Axon.Handle import Handle
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
background = background().start()
import time
import queue

p = Handle(SimpleHTTPClient()).activate()
p.put("http://example.com","inbox")
# p.put("http://google.com","inbox")
# p.put("http://slashdot.org","inbox")
# p.put("http://whatismyip.org","inbox")

def get_item(handle):
   while 1:
      try:
          item = handle.get("outbox")
          break
      except queue.Empty:
          time.sleep(0.05)
   return item

example = get_item(p)

# google = get_item(p)
# slashdot = get_item(p)
# whatismyip = get_item(p)

print( "example is", len(example), "bytes long")
# print( "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long. Also, our IP address is:", whatismyip)

time.sleep(5)