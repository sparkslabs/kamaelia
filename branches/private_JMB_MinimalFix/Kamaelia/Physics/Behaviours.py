#!/usr/bin/python
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

from Axon.Component import component
send_one_component = component

##################################################
#
# Collection of generators representing various behaviours available when
# measured.
#
#
class bouncingFloat(send_one_component):
   def __init__(self,scale_speed):
      super(bouncingFloat, self).__init__()
      self.scale_speed = scale_speed
   def main(self):
      scale = 1.0
      direction = 1
      while 1:
         scale = scale + (0.1 * self.scale_speed * direction)
         if scale >1.0:
            scale = 1.05
            direction = direction * -1
         if scale <0.1:
            scale = 0.05
            direction = direction * -1
         self.send(scale, "outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
            if data == "togglepause":
               self.pause()
            if data == "unpause":
               pass # Simply being sent this message unpauses us
         yield 1

class cartesianPingPong(send_one_component):
   def __init__(self,point, width,height,border):
      super(cartesianPingPong, self).__init__()
      self.point = point
      self.width = width
      self.height = height
      self.border = border
   def main(self):
      delta_y = 10
      delta_x = 10
      while 1 :
         self.point[0] = self.point[0]+delta_x
         self.point[1] = self.point[1]+delta_y
         if self.point[0] > self.width-self.border: delta_x = -10
         if self.point[0] < self.border: delta_x = 10
         if self.point[1] > self.height-self.border: delta_y = -10
         if self.point[1] < self.border: delta_y = 10
         self.send([x for x in self.point], "outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
            if data == "togglepause":
               self.pause()
            if data == "unpause":
               pass # Simply being sent this message unpauses us
         yield 1

class loopingCounter(send_one_component):
   def __init__(self,increment,modulo=360):
      super(loopingCounter, self).__init__()
      self.increment = increment
      self.modulo = modulo
   def main(self):
      total = 0
      while 1:
         total = (total + self.increment) % self.modulo
         self.send(total, "outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
            if data == "togglepause":
               self.pause()
         yield 1

class continuousIdentity(send_one_component):
   def __init__(self, original,*args):
      super(continuousIdentity, self).__init__()
      self.original = original
   def main(self):
      while 1:
         self.send(self.original, "outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
            if data == "unpause":
               pass # Simply being sent this message unpauses us
         yield 1

class continuousZero(send_one_component):
   def __init__(self, *args):
      super(continuousZero, self).__init__()
   def main(self):
      while 1:
         self.send(0, "outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
            if data == "unpause":
               pass # Simply being sent this message unpauses us
         yield 1

class continuousOne(send_one_component):
   def __init__(self, *args):
      super(continuousOne, self).__init__()
   def main(self):
      while 1:
         self.send(1, "outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
            if data == "unpause":
               pass # Simply being sent this message unpauses us
         yield 1


