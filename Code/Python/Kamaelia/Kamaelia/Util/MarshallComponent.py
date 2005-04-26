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
"""
Basic Marshalling Component. - UNTESTED

The Basic Marshalling Component is given a simple class. It then expects to
be passed objects of that class, and then performs the following actions:
   * __str__ on an object
   * fromString on an object

The idea is that you would place this between your logic and a network
socket, which simply serialises and deserialises objects for transmission
over the wire. The initial data format this is designed to work with is the
MimeDict object.

For simplicity, this component expects to be given an entire object to
marshall/demarshall. This requires the user to deal with framing of objects.
It is expected that there will be a more complex marshaller that is capable
of taking (say) a generator or component as an argument for the fromString
static method.

Since this is a bidirectional component we have the following boxes:
   * control - on which we may receive a shutdown message
   * signal - one which we will send shutdown messages
   * demarshall - an inbox to which you send strings for demarshalling
   * marshall - an inbox to which you send objects for marshalling
   * demarshalled - an outbox which spits out demarshalled objects
   * marshalled = an outbox which spits out marshalled strings
"""

from Axon.Component import component, scheduler

class BasicMarshallComponent(component):
   Inboxes =["control", "demarshall", "marshall"] 
   Outboxes=["signal", "demarshalled", "marshalled"]
   def __init__(self,klass):
      self.__super.__init__() # Accept default in/outboxes
      self.klass = klass

   def main(self):
      while 1:
         self.pause()
         if self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, Axon.Ipc.producerFinished):  # Not ideal, should be Axon.Ipc.Shutdown
               self.send(Axon.Ipc.producerFinished(), "signal")
               return
         if self.dataReady("marshall"):
            data = self.recv("marshall")
            self.send(str(data),"marshalled")
         if self.dataReady("demarshall"):
            data = self.recv("demarshall")
            self.send(self.klass.fromString(data),"demarshalled")

         yield 1

if __name__ == '__main__':
   print "no test harness (NASTY)"
   print "Sample Test Harness could probably make us of MimeDict as an example"

   print """
Probable usage:

from Kamaelia.Data.MimeDict import MimeDict

class MimeDictMarshaller(Kamaelia.Util.MarshallComponent.MarshallComponent):
    def __init__(self,*argv,**argd):
        self.__super.__init__(MimeDict, *argv,**argd)

Create components after that thus:

mds = MimeDictMarshaller()

Or:
def MarshallerFactory(klass):
   class newclass(Kamaelia.Util.MarshallComponent.MarshallComponent):
      def __init__(self,*argv,**argd):
         self.__super.__init__(klass, *argv,**argd)
   return newclass

MimeDictMarshaller=MarshallerFactory(MimeDict)

mds = MimeDictMarshaller()

"""

