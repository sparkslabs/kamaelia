#!/usr/bin/python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import vorbissimple
import sys
import time

x=vorbissimple.vorbissimple()
f=open("/home/zathras/Documents/Media/Ogg/PopularClassics/2/audio_01.ogg","r",0)
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
