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
"""
==========================================
Simple Marshalling/demarshalling framework
==========================================

A pair of components for marshalling and demarshalling data respectively. You
supply a class containing methods to marshall and demarshall the data in the
way you want.

The idea is that you would place this between your logic and a network
socket to transform the data to and from a form suitable for transport.



Example usage
-------------

Marshalling and demarshalling a stream of integers::

    class SerialiseInt:

        def marshall(int):
            return str(int)
        marshall = staticmethod(marshall)
    
        def demarshall(string):
            return int(string)
        demarshall = staticmethod(demarshall)

    Pipeline( producer(...),
              Marshaller(SerialiseInt),
              sender(...)
            ).activate()

    Pipeline( receiver(...),
              DeMarshaller(SerialiseInt),
              consumer(...)
            ).activate()



How does it work?
-----------------

When instantiating the Marshaller or DeMarshaller components, you provide an
object (eg. class) containing these static methods:

* marshall(item)    - returns the item serialised for transmission
* demarshall(item)  - returns the original item, deserialised

Marshaller requires only the marshall(...) static method, and DeMarshaller
requires only demarshall(...).

Why static methods? Because marshalling/demarshalling is a stateless activity.
This distinguishes marshalling activity from other protocols and other processes
that can be implemented with a similar style of framework.

For simplicity this component expects to be given an entire object to marshall
or demarshall. This requires the user to deal with the framing and deframing of
objects separately.

Any data sent to the Marshaller or DeMarshaller components' "inbox" inbox is
passed to the marshall(...) or demarshall(...) method respectively of the
class you supplied. The result is immediately sent on out of the components'
"outbox" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
components' "control" inbox, it is sent on out of the "signal" outbox. The
component will then immediately terminate.



Post script
-----------

The initial data format this is designed to work with is the
MimeDict object.

It is expected that there will be a more complex marshaller that supports
receiving that is capable of receiving objects segmented over multiple messages.
"""

from Axon.Component import component, scheduler
from Axon.Ipc import shutdownMicroprocess, producerFinished


class Marshaller(component):
    """\
    Marshaller(klass) -> new Marshaller component.

    A component for marshalling data (serialising it to a string).

    Keyword arguments:
    
    - klass  -- a class with static method: marshall(data) that returns the data, marshalled.
    """
    Inboxes  = { "inbox"   : "data to be marshalled",
                 "control" : "Shutdown signalling"
               }
    Outboxes = { "outbox" : "marshalled data",
                 "signal" : "Shutdown signalling"
               }

    def __init__(self, klass):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Marshaller, self).__init__()
        self.klass = klass

    def main(self):
        """Main loop."""
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
    """\
    DeMarshaller(klass) -> new DeMarshaller component.

    A component for demarshalling data (deserialising it from a string).

    Keyword arguments:
    - klass  -- a class with static method: demarshall(data) that returns the data, demarshalled.
    """
    Inboxes  = { "inbox"   : "data to be demarshalled",
                 "control" : "Shutdown signalling"
               }
    Outboxes = { "outbox" : "demarshalled data",
                 "signal" : "Shutdown signalling"
               }

    def __init__(self, klass):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DeMarshaller, self).__init__()
        self.klass = klass

    def main(self):
        """Main loop."""
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

__kamaelia_components__  = ( Marshaller, DeMarshaller, )



if __name__ == '__main__':
    pass
