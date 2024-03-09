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
"""\
======================================
Legacy stub for BasicMarshallComponent
======================================

The functionality of this component has been superceeded by the Marshaller and
DeMarshaller components in Kamaelia.Util.Marshalling. Please use these in
preference.

This component contains both marshalling and demarshalling facilities. It is
a thin wrapper combining a Marshalling and DeMarshalling component.



Example Usage
-------------

None at present.



How does it work?
-----------------

Behaviour is consistent with that of Kamaelia.Util.Marshalling, except that the
"inbox" inbox and "outbox" outbox are not used.

Marshall data by sending it to the "marshall" inbox. The marshalled data is
sent to the "marshalled" outbox.

Demarshall data by sending it to the "demarshall" inbox. The marshalled data is
sent to the "demarshalled" outbox.

"""

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

def BasicMarshallComponent(klass):
    return Graphline(marsh=Marshaller(klass),
                     demarsh=DeMarshaller(klass),
                     linkages = {
                       ("self", "marshall") : ("marsh","inbox"),
                       ("marsh", "outbox") : ("self","marshalled"),

                       ("self", "demarshall") : ("demarsh","inbox"),
                       ("demarsh", "outbox") : ("self","demarshalled"),

                       ("self","control") : ("marsh","control"),
                       ("marsh","signal") : ("demarsh","control"),
                       ("demarsh","signal") : ("self","signal"),
                     }
                    )

__kamaelia_prefabs__ = ( BasicMarshallComponent, )

#from Axon.Component import component, scheduler
#
#class BasicMarshallComponent(component):
#   Inboxes =["control", "demarshall", "marshall"] 
#   Outboxes=["signal", "demarshalled", "marshalled"]
#   def __init__(self,klass):
#      super(BasicMarshallComponent, self).__init__() # Accept default in/outboxes
#      self.klass = klass
#
#   def main(self):
#      while 1:
#         self.pause()
#         if self.dataReady("control"):
#            data = self.recv("control")
#            if isinstance(data, Axon.Ipc.producerFinished):  # Not ideal, should be Axon.Ipc.Shutdown
#               self.send(Axon.Ipc.producerFinished(), "signal")
#               return
#         if self.dataReady("marshall"):
#            data = self.recv("marshall")
#            self.send(str(data),"marshalled")
#         if self.dataReady("demarshall"):
#            data = self.recv("demarshall")
#            self.send(self.klass.fromString(data),"demarshalled")
#
#         yield 1
#
if __name__ == '__main__':
   print ("no test harness (NASTY)")
   print ("Sample Test Harness could probably make us of MimeDict as an example")

   print ("""
Probable usage:

from Kamaelia.Support.Data.MimeDict import MimeDict

class MimeDictMarshaller(Kamaelia.Util.MarshallComponent.MarshallComponent):
    def __init__(self,*argv,**argd):
        super(MimeDictMarshaller, self).__init__(MimeDict, *argv,**argd)

Create components after that thus:

mds = MimeDictMarshaller()

Or:
def MarshallerFactory(klass):
   class newclass(Kamaelia.Util.MarshallComponent.MarshallComponent):
      def __init__(self,*argv,**argd):
         super(newclass, self).__init__(klass, *argv,**argd)
   return newclass

MimeDictMarshaller=MarshallerFactory(MimeDict)

mds = MimeDictMarshaller()

""")

