#!/usr/bin/python
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

import vorbissimple
import sys
import time

x=vorbissimple.vorbissimple()
f=open("/usr/local/backup/Music/PopularClassics/4/audio_01.ogg","r",0)
#f=open("/home/zathras/Documents/Media/Ogg/KR-Tomb-of-Horus.ogg","r",0)
time.sleep(0.01)

while 1:
   try:
      data = x._getAudio()
      sys.stdout.write(data)
      sys.stdout.flush()
   except "RETRY":
      pass
   except "NEEDDATA":
      d = f.read(4096)
      if d=="":
         break
      x.sendBytesForDecode(d)
