#!/usr/bin/python

import vorbissimple
import sys
import time

x=vorbissimple.vorbissimple()
f = open("../../../Kamaelia/Examples/SupportingMediaFiles/KDE_Startup_2.ogg", "rb")
print(sys.argv)
while 1:
   print("Loop start")
   try:
      print("Trying")
      data = x._getAudio()
      print("Success")
      if data:
         print("Success")
         sys.stderr.buffer.write(data)
         sys.stderr.flush()
   except vorbissimple.VSSRetry:            #   except "RETRY":
      print("Inside VSSRetry")
      #pass
   except vorbissimple.VSSNeedData:         #   except "NEEDDATA":
      print("Inside VSSNeedData")
      d = f.read(4096)

      if len(d)==0:
         print("FAILED TO GET DATA")
         break
      print("Got Data", len(d))
      print("Sending Data")
      x.sendBytesForDecode(d)
      print("Sent Data")

"Also This file for real"
