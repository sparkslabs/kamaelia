#!/usr/bin/python

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
