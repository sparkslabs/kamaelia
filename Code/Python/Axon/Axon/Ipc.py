#!/usr/bin/python
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
===================
IPC message classes
===================

Some standard IPC messages used by Axon. The base class for all IPC classes is
ipc. 

Some purposes for which these can be used are described below. This is not
exhaustive and does *not* cover all of the Ipc classes defined here!



Shutting down components
------------------------

* Axon.Ipc.shutdownMicroprocess
* Axon.Ipc.producerFinished

If you want to order a component to stop, most will do so if you send either of
these ipc objects to their "control" inbox. When a component does stop, most
send on the same message they received out of their "signal" outbox (or a
message of their own creation if they decided to shutdown without external
prompting)

Producer components, such as file readers or network connections will send a
producerFinished() ipc object rather than shutdownMicroprocess() to indicate
that the shutdown is due to them finishing producing data.

You can therefore link up components in a chain - linking "signal" outboxes to
"control" inboxes to allow shutdown messages to cascade - making it easier to
shutdown and clean up a system.

How should components behave when they receive either of these Ipc messages?
In most cases, components simply shut down as soon as possible and send the same
message on out of their "signal" outbox. However many components behave slightly
more subtley to ensure the last few items of data passing throuhg a chain of
components are not accidentally lost:

* If the message is a producerFinished() message, then a component may wish to
  finish processing any data still left in its inboxes or internal buffers
  before terminating and passing on the producerFinished() message.

* If the message is a shutdownMicroprocess() message, then a component should
  ideally try to terminate rather than finish what it is doing.

Many components therefore containg logic similar to this::
    
    class MyComponent(Axon.Component.component):

        def main(self):

            while still got things to do and not received "shutdownMicroprocess":
                ..do things..
                ..check "control" inbox..
                yield 1

            if not received any shutdown message:
                self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
            else:
                self.send(message received, "signal")

producerFinished() can be likened to notification of a clean shutdown - rather
like a unix process closing its stdout file handle when it finishes.
shutdownMicroproces() is more like a hard termination due to a system being
interrupted.



Knock-on shutdowns between microprocesses
-----------------------------------------

* Axon.Ipc.shutdownMicroprocess

When a microprocess terminates, the scheduler calls its Axon.Microprocess.microprocess._closeDownMicroprocess()
method. This method can return an Axon.Ipc.shutdownMicroprocess ipc object, for
example::

    def _closeDownMicroprocess(self):
        return Axon.Ipc.shutdownMicroprocess(anotherMicroprocess)

The scheduler will ensure that other microprocess is also shut down.



shutdown vs shutdownMicroprocess
--------------------------------

* Axon.Ipc.shutdown
* Axon.Ipc.shutdownMicroprocess

You may notice that shutdownMicroprocess appears to be used for two purposes -
knock-on shutdowns and signalling component shutdown.

Axon.Ipc.shutdown was originally intended to be used rather than
Axon.Ipc.shutdownMicroprocess; however because most components support the
latter (which was an accidental mistake) the latter should continue to be used.

Axon may at some stage make these two Ipc classes synonyms for each other to
resolve this issue, but this decision has not been taken yet.



Setting off a new microprocess and waiting for it to complete
-------------------------------------------------------------

* Axon.Ipc.WaitComplete
* Axon.Ipc.reactivate

Used by:

* components / microprocesses
* Axon.Scheduler.scheduler

A microprocess can yield a WaitComplete() Ipc message to the scheduler to ask
for another microprocess to be started. When that second microprocess completes,
the original one resumes - it waits until the second one completes.

This is a nice little way to sidestep the restriction in python that you can't
nest yield statements for a given generator inside methods/functions it calls.

For example, here's a clean way to wait for data arriving at the "inbox" inbox
of a component::

    class MyComponent(Axon.Component.component):
    
        def main(self):
            ...
            yield WaitComplete(self.waitForInbox())
            msg = self.recv("inbox")

        def waitForInbox(self):
            while not self.dataReady("inbox"):
                yield 1

Internally, the scheduler uses Axon.Ipc.reactivate to ensure the original
microprocess is resumed after the one that was launched terminates.


                
"""
class ipc(object):
   """Message base class"""
   pass

class WaitComplete(ipc):
   """\
   WaitComplete(generator) -> new WaitComplete object.
   
   Message to ask the scheduler to temporarily suspect this microprocess and
   run a new one instead based on the generator provided; resuming the original
   when the new one completes.
   
   Use within a microprocess by yielding one back to the scheduler.

   Arguments:

   - the generator to be run as the separate microprocess
   """
   def __init__(self, *args,**argd):
      self.args = args
      self.argd = argd

class reactivate(ipc):
   """\
   reactivate(original) -> new reactivate ipc message.

   Returned by Axon.Microprocess.microprocess._closeDownMicroprocess() to the
   scheduler to get another microprocess reactivated.
   
   Keyword arguments:

   - original  -- The original microprocess to be resumed. Assigned to self.original
   """
   def __init__(self, original):
      self.original = original

class newComponent(ipc):
   """\
   newComponent(\*components) -> new newComponent ipc message.
   
   Message used to inform the scheduler of a new component that needs a thread
   of control and activating.

   Use within a microprocess by yielding one back to the scheduler.
   
   Arguments:

   - the components to be activated
   """
   def __init__(self, *components):
      self._components = components
   def components(self):
      """Returns the list of components to be activated"""
      return self._components

class shutdownMicroprocess(ipc):
   """\
   shutdownMicroprocess(\*microprocesses) -> new shutdownMicroprocess ipc message.
   
   Message used to indicate that the component recieving it should shutdown.
   Or to indicate to the scheduler a shutdown knockon from a terminating
   microprocess.

   Arguments:
       
   - the microprocesses to be shut down (when used as a knockon)
   """
   def __init__(self, *microprocesses):
      self._microprocesses = microprocesses
   def microprocesses(self):
      """Returns the list of microprocesses to be shut down"""
      return self._microprocesses


class notify(ipc):
   """\
   notify(caller,payload) -> new notify ipc message.
   
   Message used to notify the system of an event. Subclass to implement your own
   specific notification messages.

   Keyword arguments:

   - caller   -- a reference to whoever/whatever issued this notification. Assigned to self.caller
   - payload  -- any relevant payload relating to the notification. Assigned to self.object
   """
   def __init__(self, caller, payload):
      self.object = payload
      self.caller = caller

class shutdown(ipc):
   """\
   Message used to indicate that the component recieving it should shutdown.

   Due to legacy mistakes, use shutdownMicroprocess instead.
   """
   pass

class status(ipc):
   """\
   status(status) -> new status ipc message.
   
   General Status message.
   
   Keyword arguments:

   - status  -- the status.
   """
   def __init__(self, status):
      self._status =status
   def status(self):
      """Returns what the status is"""
      return self._status

class wouldblock(ipc):
   """\
   wouldblock(caller) -> new wouldblock ipc message.
   
   Message used to indicate to the scheduler that the system is likely to block
   now.

   Keyword arguments:

   - caller  -- who it is who is likely to block (presumably a microprocess). Assigned to self.caller
   """
   def __init__(self,caller):
      self.caller = caller

class producerFinished(ipc):
   """\
   producerFinished([caller][,message]) -> new producerFinished ipc message.
   
   Message to indicate that the producer has completed its work and will produce
   no more output. The receiver may wish to shutdown.

   Keyword arguments:

   - caller   -- Optional. None, or the producer who has finished. Assigned to self.caller
   - message  -- Optional. None, or a message giving any relevant info. Assigned to self.message
   """
   def __init__(self,caller=None,message=None):
      self.caller = caller
      self.message = message

class errorInformation(ipc):
   """\
   errorInformation(caller[,exception][,message]) -> new errorInformation ipc message.
   
   A message to indicate that a non fatal error has occured in the component.
   It may skip processing errored data but should respond correctly to future
   messages.

   Keyword arguments:

   - caller     -- the source of the error information. Assigned to self.caller
   - exception  -- Optional. None, or the exception that caused the error. Assigned to self.exception
   - message    -- Optional. None, or a message describing the problem. Assigned to self.message
   """
   def __init__(self, caller, exception=None, message=None):
      self.caller = caller # the component that the error occured in.
      self.exception = exception # if an exception was caught the exception object
      self.message = message # the message with bad data that caused the exception or error

if __name__ == '__main__':
   print "This class currently contains no test code."
