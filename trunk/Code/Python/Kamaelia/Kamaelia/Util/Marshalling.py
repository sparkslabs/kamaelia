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
Basic Marshalling Components

The Marshalling/DeMarshalling Component is given a simple class. It then expects
to be passed objects of that class, and then performs the following actions:
   * marshall on an object
   * demarshall on an object

The idea is that you would place this between your logic and a network
socket, which simply serialises and deserialises objects for transmission
over the wire. The initial data format this is designed to work with is the
MimeDict object.

For simplicity, this component expects to be given an entire object to
marshall/demarshall. This requires the user to deal with framing of objects.
It is expected that there will be a more complex marshaller that is capable
of taking (say) a generator or component as an argument for the fromString
static method.

"""

from Axon.Component import component, scheduler
from Axon.Ipc import shutdownMicroprocess, producerFinished


class Marshaller(component):
    """Marshalls (serialises) data presented on the inbox.
       Use this component by providing an object with a marshall method
       that will convert (serialise) the data to a string
    """
    Inboxes  = { "inbox"   : "data to be marshalled",
                 "control" : ""
               }
    Outboxes = { "outbox" : "marshalled data",
                 "signal" : ""
               }

    def __init__(self, klass):
        """Initialisation.
           klass is an object with method klass.marshall( <item to be marshalled> )
        """
        super(Marshaller, self).__init__()
        self.klass = klass

    def main(self):
        done = False
        while not done:

            yield 1
            self.pause()

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send( self.klass.marshall(data), "outbox")

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True



                
class DeMarshaller(component):
    """DeMarshalls (serialises) data presented on the inbox.
       Use this component by providing an object with a demarshall method
       that will convert (deserialise) the data from a string to its original form
    """
    Inboxes  = { "inbox"   : "data to be demarshalled",
                 "control" : ""
               }
    Outboxes = { "outbox" : "demarshalled data",
                 "signal" : ""
               }

    def __init__(self, klass):
        """Initialisation.
           klass is an object with method klass.demarshall( <item to be demarshalled> )
        """
        super(DeMarshaller, self).__init__()
        self.klass = klass

    def main(self):
        done = False
        while not done:

            yield 1
            self.pause()

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send( self.klass.demarshall(data), "outbox")

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True




if __name__ == '__main__':
    pass
