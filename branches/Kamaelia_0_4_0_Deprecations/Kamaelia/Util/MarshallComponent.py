#!/usr/bin/env python2.3
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

None. Please use Kamaelia.Util.Marshalling in preference.



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

__kamaelia_prefab__ = ( BasicMarshallComponent, )

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
   print "no test harness (NASTY)"
   print "Sample Test Harness could probably make us of MimeDict as an example"

   print """
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

"""

