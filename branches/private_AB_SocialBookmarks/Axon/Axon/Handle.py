#!/usr/bin/env python

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
Communicating with components from non Axon code
================================================

The Handle component wraps another component and allows data to be sent to and
received from its standard inboxes ("inbox" and "control") and standard outboxes
("outbox" and "signal"). It provides this via thread safe, non-blocking get()
and put() methods.

This is particularly useful in combination with Axon.background - allowing
communication with components running in the background of a non Axon based
piece of code.



Still Experimental
------------------

This code is currently experimental - we'd welcome reports of any issues you may
encounter when using this code.



Example Usage
-------------

Here, Axon/Kamaelia is used to connect to a server then receive text, chunking
it into individual lines. This is done by using Axon in the background (since
other code in this hypothetical system is not Axon based).

NOTE: To see how this could be done without using Axon.Handle, see the examples
in the documentation for Axon.background.

1. We create a background object and call its start() method::

    from Axon.background import background
    
    background().start()

2. We create and activate our Kamaelia pipeline of components, wrapped in an
   instance of the Handle class::
    
    from Axon.Handle import Handle
    from Kamaelia.Chassis.Pipeline import Pipeline 
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Visualisation.PhysicsGraph import chunks_to_lines

    queue = Queue()

    connection = Handle(
        Pipeline(
            TCPClient("my.server.com", 1234),
            chunks_to_lines()
        )
    ).activate()

We can now fetch items of data when they arrive, using the Handle, from the
"outbox" outbox of the pipeline::

    from Queue import Empty

    while 1:
       try:
           received_line = connection.get("outbox")
           print "Received line:", received_line
       except Empty:
           # no data yet
           time.sleep(0.1)

We can also send data, back to the server, by sending it to the "inbox" inbox
of the pipeline::

    connection.put("Bytes to send to server\\n", "inbox")



Behaviour
---------

Handle is a threaded component. It does not have the standard inboxes ("inbox"
and "control") or standard outboxes ("outbox" and "signal"). The only way to
communicate with Handle is via its get() and put() methods.

Instantiate Handle, passing it a component to wrap. Upon activation, Handle
automatically wires inboxes and outboxes of its own to the "inbox" and
"control" inboxes and "outbox" and "signal" outboxes of the component it is
wrapping. Handle then activates the wrapped component.

To send data to the wrapped component's "inbox" or "control" inboxes, call the
put() method, specifying, as arguments, the item of data and the name of the
inbox it is destined for. The data is queued and sent at the next opportunity.

To retrieve data sent out by the wrapped component's "outbox" or "signal"
outboxes, call the get() method, specifying, as an argument, the name of the
outbox in question. This method is *non blocking* - if there is data waiting,
then the oldest item of data is returned, otherwise a Queue.Empty exception is
immediately thrown. 

When the wrapped component terminates, Handle will immediately terminate.
Handle does not respond to shutdown messages received from the wrapped
component. Handle cannot be sent shutdown messages since it has no "control"
inbox on which to receive them.



Limitations
-----------

Limited to standard inboxes and outboxes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle currently only provides access to the standard "inbox" and "control"
inboxes and standard "outbox" and "signal" outboxes of the component it wraps.

If access is required to a different inbox or outbox, try wrapping the component
within a Kamaelia.Chassis.Graphline component and specifying linkages to connect
the inbox or outbox in question to one of the standard inboxes or outboxes of
the Graphline.

CPU Usage
~~~~~~~~~

The current implememntation of Handle involves a degree of polling. However it
does use a slight (approximately 1 centisecond) delay between pollings.

Therefore when idle, CPU usage of this component will be slightly greater than zero.



Design rationale and history
----------------------------

This component is the successor to the earlier "likefile" component. Likefile
suffered from some design issues that resulted in occassional race conditions.

We dropped the name "LikeFile" since whilst it derives from the concept of a
file handle, it doesn't use the same API as file() for some good reasons we'll
come back to.

A file handle is an opaque thing that you can .write() data to, and .read() data
from. This is a very simple concept and belies a huge amount of parallel
activity happening concurrently to your application. The file system is taking
your data and typically buffering it into blocks. Those blocks then may need
padding, and depending on the file system, may actually be written immediately
to the end of a cyclone buffer in a journal with some write operations. Then
periodically those buffers get flushed to the actual disk.

Based on the fact that file handles are a very natural thing for people to work
with, based on their ubiquity, and the fact that it masks the fact you're
accessing a concurrent system from a linear one, that's why we've taken this
approach for integrating Kamaelia components (which are naturally parallel) with
non-Kamaelia code, which is typically not parallel.

For simplicity of implementation, initially the implementation of Handle
supports only the equivalent of non-blocking file handles. This has two
implications:

* Reading data from a Handle may fail, since there may not be any ready yet.
  This is chosen in preference to a blocking operation
  
* Writing data to a Handle may also fail, since the component may not actually
  be ready to receive data from us.
  
  
"""
# component that creates and encapsulates a Pipeline of components, connecting
# their outbox to inbox, and signal to control to form the Pipeline chain.

import ThreadedComponent
import time
import Queue

print "Polite Notice"
print "-------------"

print "The code you are using includes using Axon.Handle. This code is"
print "currently experimental - we'd welcome any issues you may find/experience"
print "with this code."

class Handle(ThreadedComponent.threadedcomponent):
   Inboxes = {
       "_inbox":"From the component to go to the outside world",
       "_control":"From the component to go to the outside world",
   }
   Outboxes = {
       "_outbox":"From the outside world to go to the component",
       "_signal":"From the outside world to go to the component",
   }
   def __init__(self, someComponent):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Handle,self).__init__()
      self.comp = someComponent
      self.inboundData = Queue.Queue()
      self.outboundData = Queue.Queue()
      self.temp = {}

   def put(self, *args):
       """\
       Send an item of data to one of the inboxes of the wrapped component.
       
       The item of data is queued and sent to the inbox as soon as possible.
       
       Arguments:
       
       - the item of data
       - the name of the inbox it is destined for (either "inbox" or "control")
       """
       self.inboundData.put(args)

   def _get(self):
       return self.outboundData.get_nowait()

   def get(self, boxname="outbox"):
       """\
       Return an item of data sent to an outbox of the wrapped component.
       
       This method is non blocking and always returns immediately. If there is
       no data to return, then the exception Queue.Empty is thrown
       
       Arguments:
       
       - boxname  -- (optional) the name of the outbox of the wrapped component
         from which the data should be collected (default="outbox", should be
         either "outbox" or "signal")
       """
       while 1:
           try:
               data,outbox = self._get()
               try:
                   self.temp[outbox].append(data)
               except KeyError:
                   self.temp[outbox] = [ data ]
           except Queue.Empty:
               break
       try:
           X = self.temp[boxname][0]
           del self.temp[boxname][0]
       except KeyError:
          raise Queue.Empty
       except IndexError:
          raise Queue.Empty
       return X

   def main(self):
      """Main loop."""
      self.addChildren(self.comp)

      self.link((self,"_outbox"), (self.comp,"inbox"))
      self.link((self,"_signal"), (self.comp,"control"))
      self.link((self.comp,"outbox"), (self,"_inbox"))
      self.link((self.comp,"signal"), (self,"_control"))

      for child in self.children:
          child.activate()

      # run until all child components have terminated
      # at which point this component can implode

      # becuase they are children, if they terminate, we'll be woken up
      while not self.childrenDone():

          # We manually forward the data here. There are probably nicer methods, but for the
          # moment, lets stick to brute force/clarity

          time.sleep(0.01) # so that we're not totally spinning

          if not(self.inboundData.empty()):
              data,box = self.inboundData.get_nowait()
              if box == "inbox":
                   self.send(data, "_outbox")
              if box == "control":
                   self.send(data, "_signal")

          while self.dataReady("_inbox"):
              self.outboundData.put( (self.recv("_inbox"), "outbox") )
          while self.dataReady("_control"):
              self.outboundData.put( (self.recv("_control"), "signal") )


   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us

       return 0==len(self.childComponents())
                  
if __name__=="__main__":
    print "This is no longer like ThreadWrap - it is not supposed to be"
    print "Usable in the usual manner for a component..."
