#!/usr/bin/python
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

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX TODO
#
# Wrapper for SubtitleFilter, probably a useful component in its own right that
# could be moved out of here, perhaps make Kamaelia.DVB for it?
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

from Axon.Component import component
from SubtitleFilter import SubtitleFilter2

class SubtitleFilterComponent(component):
   """Pretty much a general filter component using the SubtitleFilter2 class as
   the filtering process.  See that for details. 
   """
   def __init__(self):
      super(SubtitleFilterComponent, self).__init__() # Take default in/out boxes
      self.filt = SubtitleFilter2()
      
   def mainBody(self):
      if self.dataReady():
         mes = self.recv()
         outmes = self.filt.filter(mes)
         if outmes != "":
            self.send(outmes)
      if self.dataReady("control"):
         mes = self.recv("control")
         if isinstance(mes, producerFinished):
            self.send(mes, "signal")
            return 0
      return 1
            
   def closeDownComponent(self):
      outmes = self.filt.filter("")
      if outmes != "":
         self.send(outmes)
