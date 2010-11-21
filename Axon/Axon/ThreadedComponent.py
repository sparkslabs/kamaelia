#!/usr/bin/env python
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
=======================
Thread based components
=======================

A threaded component is like an ordinary component but where the main() method
is an ordinary method that is run inside its own thread. (Normally main() is
a generator that is given slices of execution time by the scheduler).

This is really useful if your code needs to block - eg. wait on a system call,
or if it is better off being able to run on another CPU (though beware python's
limited ability to scale across multiple CPUs).

If you don't need these capabilities, consider making your component an ordinary
Axon.Component.component instead.

* threadedcomponent - like an ordinary Axon.Component.component, but runs in its
  own thread
* threadedadaptivecommscomponent - a threaded version of
  Axon.AdaptiveCommsComponent.AdaptiveCommsComponent



Just like writing an ordinary component
---------------------------------------

This is nearly identical to writing an ordinary Axon.Component.component. For
example this ordinary component::

    class MyComponent(Axon.Component.component):

        Inboxes = { "inbox"   : "Send the FOO objects to here",
                    "control" : "NOT USED",
                  }
        Outboxes = { "outbox" : "Emits BAA objects from here",
                     "signal" : "NOT USED",
                   }

        def main(self):
            while 1:
                if self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    result = ... do something to msg ...
                    self.send(result, "outbox")

                yield 1

Can be trivially written as a threaded component simply by removing the
``yield`` statements, turning main() into a normal method::
    
    class MyComponent(Axon.ThreadedComponent.threadedcomponent):

        Inboxes = { "inbox"   : "Send the FOO objects to here",
                    "control" : "NOT USED",
                  }
        Outboxes = { "outbox" : "Emits BAA objects from here",
                     "signal" : "NOT USED",
                   }

        def main(self):
            while 1:
                if self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    result = ... do something to msg ...
                    self.send(result, "outbox")


What can a threaded component do?
---------------------------------

Exactly the same things any other component can. The following method calls are
all implemented in a thread safe manner and function exactly as you should
expect:

* self.link()
* self.unlink()
* self.dataReady()
* self.anyReady()
* self.recv()
* self.send()

*self.pause()* behaves slightly differently:

* calling self.pause() pauses immediately - not at the next yield statement
  (since there are no yield statements!)
* self.pause() has an extra optional 'timeout' argument to allow you to write
  timer code that can be interrupted, for example, by incoming messages.


In addition, threadedadaptivecommscomponent also supports the extra methods in
Axon.AdaptiveCommsComponent.AdaptiveCommsComponent:
                    
* self.addInbox()
* self.deleteInbox()
* self.addOutbox()
* self.deleteOutbox()
* *etc..*



Inbox and Outbox queues
-----------------------

There is one difference: because the main() method runs in a different thread
it does not actually interact directly with its own inboxes and outboxes.
Internal queues are used to get data between your thread and the component's
actual inboxes and outboxes. This is hidden for the most part - the method calls
you make to receive and send messages are exactly the same.

When initialising a threadedcomponent you may wish to specify the size limit
(queue length) for these queues. There is a size limit so that if your threaded
component is delivering to a size limited inbox, the effects of the inbox
becoming full propagate back to your thread.

In some ways this is a bit like nesting one component within another - where
all the parent component's inboxes and outboxes are forwarded to the child::

            +-----------------------------------------+
            |           threaded component            |
            |                                         |
            |              +----------+               |
            |              |  main()  |               |
          INBOX -------> inbox      outbox -------> OUTBOX
            |    queue     |          |     queue     |
            |              +----------+               |
            +-----------------------------------------+

What does this mean in practice?

* *More messages get buffered*. - Suppose your threaded component has an internal
  queues of size 5 and is delivering messages to an inbox on another component
  with a size limit of 10. From the perspective of your threaded component you
  will actually be able to send 15 messages before you might start to get
  Axon.AxonExceptions.noSpaceInBox exceptions.

* *Threaded components that output lots of messages might see unexpected 'box
  full' exceptions* - Suppose your threaded component has a small internal queue
  size but produces lots of messages very quickly. The rest of the system may
  not be able to pick up those messages quickly enough to put them into the
  destination inbox. So even though the destination might not have a size limit
  you may still get these exceptions.

The secret is to choose a sensible queue size to balance between it being able
to buffer enough messages without generating errors whilst not being so large as
to render a size limited inbox pointless!


Regulating speed
----------------

In addition to being able to pause (with an optional timeout), a threaded
component can also regulate its speed by briefly synchronising with the rest of
the system. Calling the sync() method simply briefly blocks until the rest of
the system can acknowledge.



Stopping a threaded component
-----------------------------

Note that it is *not* safe to forcibly stop a threaded component (by calling
the stop() method before the microprocess in it has terminated). This is because
there is no true support in python for killing a thread.

Calling stop() prematurely will therefore kill the internal microprocess that
handles inbox/outbox traffic on behalf of the thread, resulting in undefined
behaviour.



When the thread terminates...
-----------------------------

threadedcomponent will terminate - as you would expect. However, there are some
subtleties that may need to be considered. These are due to the existence of the
intermediate queues used to communicate between the thread and the actual
inboxes and outboxes (as described above).

* When main() terminates, even if it has just recently checked its inqueues
  (inboxes) there might still be items of data at the inboxes.
  This is because there is a gap between data that arriving at an inbox, and it
  being forwarded into an inqueue going to the thread.

* When main() terminates, threadedcomponent will keep executing until it has
  finished successfully sending any data in outqueues, out of the respective
  "outboxes". This means that anything main() thinks it has sent is guaranteed
  to be sent. But if the destination is a size limited inbox that has become
  full (and that never gets emptied), then threadedcomponent will indefinitely
  stall because it cannot finish sending.



How is threaded component implemented?
--------------------------------------

threadedcomponet subclasses Axon.Components.component. It overrides the
activate() method, to force activation to use a method called _localmain()
instead of the usual main(). The code that someone writes for their main()
method is instead run in a separate thread.

The code running in main() does not directly access inboxes our outboxes and
doesn't actually create or destroy linkages itself. _localmain() can be thought
of as a kind of proxy for the thread - acting on its behalf within the main
scheduler run thread.

main() is wrapped by _threadmain() which tries to trap any unhandled exceptions
generated in the thread and pass them back to _localmain() to be rethrown.

Internal state:

* **_threadrunning** - flag, cleared by the thread when it terminates
* **queuelengths** - size to be used for internal queues between thread and
  inboxes and outboxes
* **_threadmainmethod** - the main method to be run as a thread
* **_thethread** - the thread object itself

Internal to _localmain():

* **running** - flag tracking if the thread is still runnning
* **stuffWaiting** - flag tracking if there is are things that need to be done
  (if there is stuff waiting then _localmain() should not pause or terminate
  until it finishes)

Communication between the thread and _localmain():
                    
* **inqueues** - dictionary of thread safe queues for getting data from inboxes to the thread
* **outqueues** - dictionary of thread safe queues for getting data from the thread to outboxes
* **threadtoaxonqueue** - thread safe queue for making requests to _localmain()
* **axontothreadqueue** - thread safe queue for replies from _localmain()
* **threadWakeUp** - thread safe event flag for waking up the thread if sleeping
* **_threadId** - unique id that is given to the thread as its 'name'
* **_localThreadId** - the thread id (name) of the thread _localmain() and the scheduler run in


The relationship between _localmain() and the main() method (running in a
separate thread) looks like this::

    +---------------------------------------------------------------------+
    |                         threaded component                          |
    |                                                                     |
    |           +--------------------------------------------+            |
    |           |                _localmain()                |            |
  INBOX ------> |                                            | -------> OUTBOX
    |           |    Ordinary generator based microprocess   |            |
 CONTROL -----> |       in same thread as rest of system     | -------> SIGNAL
    |           |                                            |            |
    |           +--------------------------------------------+            |
    |              |          ^               ^            |              |
    |              |          |               |            |              |
    |          inqueues   outqueues   threadtoaxonqueue    |              |
    |           "inbox"    "outbox"           |            |              |
    |          "control"   "signal"           |    axontothreadqueue      |
    |              |          |               |            |              |
    |              V          |               |            V              |
    |           +--------------------------------------------+            |
    |           |                   main()                   |            |
    |           |                                            |            |
    |           |        Runs in a separate thread           |            |
    |           +--------------------------------------------+            |
    |                                                                     |
    +---------------------------------------------------------------------+

When a message arrives at an inbox, _localmain() collects it and places it into
the thread safe queue self.inqueues[boxname] from which the thread can collect
it. self.dataReady() and self.recv() are both overridden so they access the
queues instead of the normal inboxes.

Similarly, when the thread wants to send to an outbox; self.send() is overridden
so that it is actually sent to a thread safe queue self.outqueues[boxname] from
which _localmain() collects it and sends it on.

Because all queues have a size limit (specified in at initialisation of the
threaded component) this enables the effects of size limited inboxes to
propagate up to the separate thread, via the queue. The implementation of
self.send() is designed to mimic the behaviour

For other methods such as link(), unlink() and (in the case of
threadedadaptivecommscomponent) addInbox(), deleteInbox(), addOutbox() and
deleteOutbox(), the _localmain() microprocess also acts on the thread's behalf.
The request to do something is sent to _localmain() through the thread safe
queue self.threadtoaxonqueue. When the operation is complete, an acknowledgement
is sent back via another queue self.axontothreadqueue::

        _localmain()                         main() [thread]
             |                                 |
             |       please call 'link()'      |
             | ------------------------------> |
             |                                 |
             |                         self.link() called
             |                                 |
             |      return value from call     |
             | <------------------------------ |
             |                                 |

The thread does not continue until it receives the acknowledgement - this is to
prevent inconsistencies in state. For example, a call to create an inbox might
be followed by a query to determine whether there is data in it - the inbox
therefore must be fully set up before that query can be handled.

This is implemented by the _do_threadsafe() method. This method detects whether
it is being called from the same thread as the scheduler (by comparing thread
IDs). If it is not the same thread, then it puts a request into
self.threadtoaxonqueue and blocks on self.axontothreadqueue waiting for a reply.
The request is simply a tuple of a method or object to call and the associated
arguments. When _localmain() collects the request it issues the call and
responds with the return value.

self.pause() is overridden and equivalent functionality reimplemented by
blocking the thread on a threading.Event() object which can be signalled by
_localmain() whenever the thread ought to wake up.


The 'Adaptive' version does *not* ensure the resource tracking and retrieval
methods thread safe. This is because it is assumed these will only be accessed
internally by the component itself from within its separate thread. _localmain()
does not touch these resources.


XXX *TODO*: Thread shutdown - no true support for killing threads in python
            (if ever). stop() method therefore doesn't stop the thread. Only
            stops the internal _localmain() microprocess, which therefore cuts
            the thread off from communicating with the rest of the system.


"""

from __future__ import generators

import Component
from AdaptiveCommsComponent import _AdaptiveCommsable as _AC
from AxonExceptions import noSpaceInBox
import threading
import Queue
from idGen import numId
import sys

DefaultQueueSize = 1000

class threadedcomponent(Component.component):
   """\
   threadedcomponent([queuelengths]) -> new threadedcomponent
   
   Base class for a version of an Axon component that runs main() in a separate
   thread (meaning it can, for example, block). Subclass to make your own.

   Internal queues buffer data between the thread and the Axon inboxes and
   outboxes of the component. Set the default queue length at initialisation
   (default=1000).

   A simple example::

      class IncrementByN(Axon.ThreadedComponent.threadedcomponent):

          Inboxes = { "inbox" : "Send numbers here",
                      "control" : "NOT USED",
                    }
          Outboxes = { "outbox" : "Incremented numbers come out here",
                       "signal" : "NOT USED",
                     }

          def __init__(self, N):
              super(IncrementByN,self).__init__()
              self.n = N

          def main(self):
              while 1:
                  while self.dataReady("inbox"):
                      value = self.recv("inbox")
                      value = value + self.n
                      self.send(value,"outbox")
                      
                  if not self.anyReady():
                      self.pause()
   """

   def __init__(self,queuelengths=DefaultQueueSize, **argd):
      super(threadedcomponent,self).__init__(**argd)
      
      self._threadrunning = False
      
      self.queuelengths = queuelengths
      self.inqueues = dict()
      self.outqueues = dict()
      for box in self.inboxes.iterkeys():
         self.inqueues[box] = Queue.Queue(self.queuelengths)
      for box in self.outboxes.iterkeys():
         self.outqueues[box] = Queue.Queue(self.queuelengths)

      self.threadtoaxonqueue = Queue.Queue()
      self.axontothreadqueue = Queue.Queue()

      self.threadWakeUp = threading.Event()


   def activate(self, Scheduler=None, Tracker=None, mainmethod="main"):
       """\
       Call to activate this microprocess, so it can start to be executed by a
       scheduler. Usual usage is to simply call x.activate().

       See Axon.Microprocess.microprocess.activate() for more info.
       """
       self._threadId = numId()
       self._localThreadId = threading.currentThread().getName()
       self._threadmainmethod = self.__getattribute__(mainmethod)
       self._thethread = threading.Thread(name=self._threadId, target=self._threadmain)
       self._thethread.setDaemon(True) # means the thread is stopped if the main thread stops.
   
       return super(threadedcomponent,self).activate(Scheduler,Tracker,"_localmain")
   
   def _threadmain(self):
        """\
        Exception trapping wrapper for main().

        Runs in the separate thread. Catches any raised exceptions and attempts
        to pass them back to _localmain() to be re-raised.
        """
        try:
            self._threadmainmethod()
        except:
            exception = sys.exc_info()
            # FIXME: Having an option dump of the traceback after the bare except would be useful here
            def throwexception(exception):
                raise exception[0], exception[1], exception[2]
            self._do_threadsafe( throwexception, [exception], {} )
        self._threadrunning = False
        Component.component.unpause(self)
   
   
   def main(self):
      """\
      Override this method, writing your own main thread of control as an
      ordinary method. When the component is activated and the scheduler is
      running, this what gets executed.

      Write it as an ordinary method. Because it is run in a separate thread, it
      can block.

      If you do not override it, then a default main method exists instead that
      will:

      1. Call self.initialiseComponent()
      2. Loop forever calling self.mainBody() repeatedly until mainBody()
         returns a False/zero result.
      3. Call self.closeDownComponent()
      """
      self.initialiseComponent()
      result=1
      while (result):
         result = self.mainBody()
      self.closeDownComponent()

   def initialiseComponent(self):
      """Stub method. **This method is designed to be overridden.** """
      return 1
   def mainBody(self):
      """Stub method. **This method is designed to be overridden.** """
      return None
   def closeDownComponent(self):
      """Stub method. **This method is designed to be overridden.** """
      return 1

   def pause(self, timeout=None):
       """\
       Pauses the thread and blocks - does not return until the something
       happens to re-awake it, or until it times out (if the optional timeout
       is specified)

       Must only be called from within the main() method - ie. from within the
       separate thread.

       Keyword arguments:

       - timeout  -- Optional. None, or the number of seconds after which this call should unblock itself (default=None)
       """
       
       # wait for wakeup from an event, but also have an optional timeout
       self.threadWakeUp.wait(timeout)
       # clear the event immediately afterwards (not a race hazard, since
       # if something else caused it to be set, it doesn't matter - we've
       # already woken, and we've not yet started handling the causes of the
       # event)
       self.threadWakeUp.clear()
       return


   def forwardInboxToThread(self, box):
       while self._nonthread_dataReady(box):
          if not self.inqueues[box].full():
               msg = self._nonthread_recv(box)
               self.inqueues[box].put(msg)
               self.threadWakeUp.set()     # wake a paused main()
          else:
               break


   def _localmain(self):
       """\
       Do not overide this unless you reimplement the pass through of the boxes
       to the threads, and state management.
       """

       # start the thread
       self._threadrunning = True
       self._thethread.start()
       running = True
       stuffWaiting = False
       while running or stuffWaiting:
          # decide if we need to stop...
          running = self._thethread.isAlive()
          # ...but we'll still flush queue's through:
          # (must make sure we flush ALL messages from each queue)
          
          # decide how many requests from the thread that we'll handle
          # before flushing queues
          # If we don't consider: a thread puts item in an outqueue then issues
          # a command to delete that queue. It does this *after* we've checked 
          # outqueues, but *before* we process threadtoaxonqueue. That item
          # in the outqueue would be lost.
          # This way we guarantee flushing any queue activity done by the thread
          # before the command
          msgcount = self.threadtoaxonqueue.qsize()
          
          stuffWaiting = False


          for box in self.inboxes:
              if "control" == box:
                  continue
              self.forwardInboxToThread(box)

          if "control" in self.inboxes:
              self.forwardInboxToThread("control")

                  
          for box in self.outboxes:
              
              while not self.outqueues[box].empty():
                  if not self.outboxes[box].isFull():
                      msg = self.outqueues[box].get()
                      # wake *after* item is taken from queue, otherwise thread
                      # might get there first and still think its full!
                      self.threadWakeUp.set() # wake thread, just like we would be if something we've sent is collected
                      try:
                          self._nonthread_send(msg, box)
                      except noSpaceInBox, e:
                          raise RuntimeError("Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?")
                  else:
                      stuffWaiting = True
                      break

          # we've already decided earlier how many we are handling. We don't
          # change our minds now, for reasons given above
          for i in range(0,msgcount):
              msg = self.threadtoaxonqueue.get()
              self._handlemessagefromthread(msg)

          if running:
              Component.component.pause(self)
          
          yield 1
       self._threadrunning = False

   def _handlemessagefromthread(self,msg):
       """\
       Unpacks a message containing a request to run a method of the form
       (objectToCall, argList, argDict) then calls it and places the result
       in the axontothreadqueue queue.

       Used to execute methods on behalf of the separate thread. Results are
       returned to it via the return queue.
       """
       (cmd, argL, argD) = msg
#       print cmd, argL, argD
       result = cmd(*argL,**argD)
       self.axontothreadqueue.put(result)

   _nonthread_dataReady = Component.component.dataReady
   _nonthread_recv      = Component.component.recv
   _nonthread_send      = Component.component.send

   def dataReady(self,boxname="inbox"):
       """\
       Returns true if data is available in the requested inbox.

       Used by the main() method of a component to check an inbox for ready data.
       
       Call this method to periodically check whether you've been sent any
       messages to deal with!

       You are unlikely to want to override this method.
       """
       return self.inqueues[boxname].qsize()

   def recv(self,boxname="inbox"):
       """\
       returns the first piece of data in the requested inbox.

       Used by the main() method to recieve a message from the outside world.
       All comms goes via a named box/input queue

       You will want to call this method to actually recieve messages you've been
       sent. You will want to check for new messages using dataReady first
       though.

       You are unlikely to want to override this method.
       """
       # don't forget to wake up _localmain() - it might have been sleeping
       # waiting to put something else into this inqueue
       Component.component.unpause(self)
       # collect message from queue.
       return self.inqueues[boxname].get()

   def send(self,message, boxname="outbox"):
       """\
       appends message to the requested outbox.

       Used by the main() method to send a message to the outside world.
       All comms goes via a named box/output queue

       You will want to call this method to send messages.
       
       Raises Axon.AxonExceptions.noSpaceInBox if this outbox is linked to a
       destination inbox that is full, or if your component is producing messages
       faster than Axon can pass them on.

       You are unlikely to want to override this method.
       """
       try:
           self.outqueues[boxname].put_nowait(message)
           # wake up _localmain() so it can collect the message and send it on
           Component.component.unpause(self)        # FIXME: Fragile
       except Queue.Full:
           raise noSpaceInBox(self.outqueues[boxname].qsize(), self.queuelengths)

   def link(self, source,sink,passthrough=0):
        """\
        Creates a linkage from one inbox/outbox to another.

        -- source  - a tuple (component, boxname) of where the link should start from
        -- sink    - a tuple (component, boxname) of where the link should go to

        Other optional arguments:

        - passthrough=0  - (the default) link goes from an outbox to an inbox
        - passthrough=1  - the link goes from an inbox to another inbox
        - passthrough=2  - the link goes from an outbox to another outbox

        See Axon.Postoffice.link(...) for more information.
        """
        cmd = super(threadedcomponent,self).link
        return self._do_threadsafe( cmd, (source,sink), {"passthrough":passthrough} )

   def unlink(self, thecomponent=None, thelinkage=None):
        """\
        Destroys all linkages to/from the specified component or destroys the
        specific linkage specified.

        Only destroys linkage(s) that were created *by* this component itself.
        
        Keyword arguments:
        
        - thecomponent -- None or a component object
        - thelinakge   -- None or the linkage to remove
        """
        cmd = super(threadedcomponent,self).unlink
        return self._do_threadsafe( cmd, (thecomponent,thelinkage), {} )

   def sync(self):
        """\
        Call this from main() to synchronise with the main scheduler's thread.

        You may wish to do this to throttle your component's behaviour
        This is akin to posix.sched_yield or shoving extra "yield"
        statements into a component's generator.
        """
        return self._do_threadsafe( lambda:None, [], {} )
   
   def _do_threadsafe(self, cmd, argL, argD):
        """\
        Internal method for ensuring a method call takes place in the main
        scheduler's thread.
        """
        # If this method determines it is being called from a different thread
        # then instead of doing the method call it bundles what it was going to
        # call and the arguments into an internal queue (which is serviced by
        # _localmain() ) and waits for the result of the call to be passed back.
        
        if self._threadrunning and threading.currentThread().getName() != self._localThreadId:
            # call must be synchronous (wait for reply) because there is a reply
            # and because next instruction in thread might assume this outbox
            # exists
            self.threadtoaxonqueue.put( (cmd, argL, argD ) )
            Component.component.unpause(self)
            return self.axontothreadqueue.get()
        else:
            return cmd(*argL,**argD)


        
class threadedadaptivecommscomponent(threadedcomponent, _AC):
    """\
    threadedadaptivecommscomponent([queuelengths]) -> new threadedadaptivecommscomponent
    
    Base class for a version of an Axon adaptivecommscomponent that runs main()
    in a separate thread (meaning it can, for example, block).
    
    Subclass to make your own.
    
    Internal queues buffer data between the thread and the Axon inboxes and
    outboxes of the component. Set the default queue length at initialisation
    (default=1000).
    
    Like an adaptivecommscomponent, inboxes and outboxes can be added and deleted
    at runtime.
    
    A simple example::
    
        class IncrementByN(Axon.ThreadedComponent.threadedcomponent):
    
            Inboxes = { "inbox" : "Send numbers here",
                        "control" : "NOT USED",
                      }
            Outboxes = { "outbox" : "Incremented numbers come out here",
                        "signal" : "NOT USED",
                       }
    
            def __init__(self, N):
                super(IncrementByN,self).__init__()
                self.n = N
    
            def main(self):
                while 1:
                    while self.dataReady("inbox"):
                        value = self.recv("inbox")
                        value = value + self.n
                        self.send(value,"outbox")
                        
                    if not self.anyReady():
                        self.pause()
    """

    def __init__(self,*argL,**argD):
        threadedcomponent.__init__(self,*argL,**argD)
        _AC.__init__(self)

    def addInbox(self,*args):
        """
        Allocates a new inbox with name *based on* the name provided. If a box
        with the suggested name already exists then a variant is used instead.
    
        Returns the name of the inbox added.
        """
        return self._do_threadsafe(self._unsafe_addInbox, args, {})
    
    def deleteInbox(self,name):
        """\
        Deletes the named inbox. Any messages in it are lost.
    
        Try to ensure any linkages to involving this outbox have been destroyed -
        not just ones created by this component, but by others too! Behaviour is
        undefined if this is not the case, and should be avoided.
        """
        return self._do_threadsafe(self._unsafe_deleteInbox, [name], {})
    
    def addOutbox(self,*args):
        """\
        Allocates a new outbox with name *based on* the name provided. If a box
        with the suggested name already exists then a variant is used instead.
    
        Returns the name of the outbox added.
        """
        return self._do_threadsafe(self._unsafe_addOutbox, args, {})
    
    def deleteOutbox(self,name):
        """\
        Deletes the named outbox.
    
        Try to ensure any linkages to involving this outbox have been destroyed -
        not just ones created by this component, but by others too! Behaviour is
        undefined if this is not the case, and should be avoided.
        """
        return self._do_threadsafe(self._unsafe_deleteOutbox, [name], {})
        
    def _unsafe_addInbox(self,*args):
        """\
        Internal thread-unsafe code for adding an inbox.
        """
        # Use method from superclass to do it
        name = super(threadedadaptivecommscomponent,self).addInbox(*args)
        # Also set up a corresponding queue to get data to the thread
        self.inqueues[name] = Queue.Queue(self.queuelengths)
        return name
    
    def _unsafe_deleteInbox(self,name):
        # Use method from superclass to do it
        super(threadedadaptivecommscomponent,self).deleteInbox(name)
        # Also remove the corresponding queue that gets data to the thread
        del self.inqueues[name]
    
    def _unsafe_addOutbox(self,*args):
        # Use method from superclass to do it
        name = super(threadedadaptivecommscomponent,self).addOutbox(*args)
        # Also set up a corresponding queue to get data from the thread
        self.outqueues[name] = Queue.Queue(self.queuelengths)
        return name
    
    def _unsafe_deleteOutbox(self,name):
        # Use method from superclass to do it
        super(threadedadaptivecommscomponent,self).deleteOutbox(name)
        # Also remove the corresponding queue that gets data from the thread
        del self.outqueues[name]



if __name__ == "__main__":
    import time, sys
    
    class TheThread(threadedcomponent):
        def main(self):
            self.send("ADD SRC")
            for i in range(10):
                t=1.0+time.time()
                while time.time() < t:
                    self.pause(t-time.time())   # time.sleep(1.0)
                self.send("Threaded: "+str(i))
            self.send("DEL SRC")
                
    class FSMThread(threadedcomponent):
        def initialiseComponent(self):
            self.count=10
            self.send("ADD SRC")
        def mainBody(self):
            t=1.0+time.time()
            while time.time() < t:
                self.pause(t-time.time())   # time.sleep(1.0)
            self.send("FSMThread: "+str(self.count))
            self.count=self.count-1
            return self.count
        def closeDownComponent(self):
            self.send("DEL SRC")
            
    class NotThread(Component.component):
        def main(self):
            self.send("ADD SRC")
            for i in range(20):
                t=time.time()+0.5
                while time.time() < t:
                    yield 1
                self.send("Normal: "+str(i))
                yield 1
            self.send("DEL SRC")
                    
    class AAThread(threadedadaptivecommscomponent):
        def add(self,dst):
            newname = self.addOutbox("sink")
            linkage = self.link( (self, newname), dst )
            self.destinations[newname] = (dst, linkage)
            self.send("ADD SRC", newname)
            
        def rem(self,dst):
            box,linkage = [(box,linkage) for (box,(d,linkage)) in self.destinations.items() if d==dst][0]
            del self.destinations[box]
            self.send("DEL SRC", box)
            self.unlink(thelinkage=linkage)
            self.deleteOutbox(box)
            
        def main(self):
            self.destinations = {}
            
            for i in range(10):
                time.sleep(1.0)
                while self.dataReady("inbox"):
                    cmd,dst = self.recv("inbox")
                    if cmd=="ADD":
                        self.add(dst)
                    elif cmd=="DEL":
                        self.rem(dst)
                
                for box in self.destinations:
                    self.send("AAThread "+box+": "+str(i)+"\n", box)
                    
            for dst, _ in self.destinations.values():
                self.rem(dst)
    
    class OneShot(threadedcomponent):
        def __init__(self,msg,delay=0):
            super(OneShot,self).__init__()
            self.msg = msg
            self.delay = delay
            
        def main(self):
            time.sleep(self.delay)
            self.send( self.msg )
    
    class Outputter(Component.component):
        def main(self):
            refcount = 0
            done=False
            while not done:
                yield 1
                if self.dataReady("inbox"):
                    data = self.recv("inbox")
                    if data=="ADD SRC":
                        refcount = refcount+1
                    elif data=="DEL SRC":
                        refcount = refcount-1
                        if refcount == 0:
                            done=True
                    sys.stdout.write(str(data)+"\n")
                    sys.stdout.flush()
            self.send("DONE","outbox")

    
    class Container(Component.component):
        def main(self):
            t = TheThread().activate()
            n = NotThread().activate()
            f = FSMThread().activate()
            out = Outputter().activate()
            self.link( (t,"outbox"), (out,"inbox") )
            self.link( (n,"outbox"), (out,"inbox") )
            self.link( (f,"outbox"), (out,"inbox") )
            
            self.link( (out,"outbox"), (self,"inbox") )
            
            a = AAThread().activate()
            start = OneShot(msg=("ADD",(out,"inbox")),delay=0.5).activate() # first received is a '0'
            stop = OneShot(msg=("DEL",(out,"inbox")),delay=5.5).activate() # last received is a '4'
            self.link( (start,"outbox"), (a,"inbox") )
            self.link( (stop,"outbox"), (a,"inbox") )
            
            # wait until outputter sends us a signal its finished
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
                
    c = Container().run()
    
    print "-----Synchronous inbox delivered to by a threaded component-----"
    print "Sender              Middle man          Slow receiver"
    print "------------------------------------------------------------"

    class SynchronousSlowReceiver(Component.component):
        def main(self):
            self.inboxes['inbox'].setSize(5)
            while 1:
                while not self.dataReady("inbox"):
                    self.pause()
                    yield 1
                    
                r = self.recv("inbox")
                
                t=time.time() + 0.2
                while time.time() < t:
                    time.sleep(0.02)
                    yield 1
                
                sys.stdout.write("                                        received "+str(r)+"\n")
                sys.stdout.flush()
                
                if not r: break
                
    class ThreadedMiddleMan(threadedcomponent):
        def __init__(self):
            super(ThreadedMiddleMan,self).__init__(queuelengths=2)

        def main(self):
            self.inboxes['inbox'].setSize(2)
            while 1:
                while not self.dataReady("inbox"):
                    self.pause()
                    
                r = self.recv("inbox")
                sys.stdout.write("                    received "+str(r)+"\n")
                sys.stdout.flush()

                try:
                    self.send(r,"outbox")
                    sys.stdout.write("                    sent "+str(r)+"\n")
                    sys.stdout.flush()
                except noSpaceInBox:
                        sys.stdout.write("                    held up sending\n")
                        sys.stdout.flush()
                        while 1:
                            try:
                                self.send(r,"outbox")
                                sys.stdout.write("                    sent\n")
                                sys.stdout.flush()
                                break
                            except noSpaceInBox:
                                self.pause()

                if not r:
                    break


    class ThreadedSender(threadedcomponent):
        def __init__(self):
            super(ThreadedSender,self).__init__(queuelengths=2)
        
        def main(self):
            for i in range(20,-1,-1):
                try:
                    self.send(i,"outbox")
                    sys.stdout.write("sent "+str(i)+"\n")
                    sys.stdout.flush()
                except noSpaceInBox:
                    sys.stdout.write("held up sending "+str(i)+"\n")
                    sys.stdout.flush()
                    while 1:
                        try:
                            self.send(i,"outbox")
                            sys.stdout.write("sent\n")
                            sys.stdout.flush()
                            break
                        except noSpaceInBox:
                            self.pause()
                            print "Y"
#                            time.sleep(0.1)
    
    t = ThreadedSender().activate()
    m = ThreadedMiddleMan().activate()
    r = SynchronousSlowReceiver()
    r.link( (t,"outbox"), (m,"inbox") )
    r.link( (m,"outbox"), (r,"inbox") )
    
    r.run()
