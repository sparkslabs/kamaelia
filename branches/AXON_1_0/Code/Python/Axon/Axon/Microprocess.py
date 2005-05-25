#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Microprocess - A class supporting parallel execution.

A microprocess is a class supporting parallel execution, provided by
forming a wrapper around a generator. It also provides a place for context
to be stored about the generator. In terms of runtime a microprocess can
be viewed to have 2 different life cycles - that which an external user
sees, and that which the microprocess sees.

In terms of runtime life cycle viewed externally, a microprocess is created,
activated, and then has its next method repeatedly called until a false
value is returned, at which point the microprocess is deleted. In terms
of a more traditional approach the next call approximates to a timeslice
being allocated to a process/thread.

The runtime life cycle from the view of the microprocess stems from the
fact that a generator wraps a thread of control, by effectively treating
the program counter like a static variable. The following describes this
runtime from the microprocess's point of view.

First the '__init__' function is called during initialisation at object
creation time. This results in a non-active, non-running microprocess.
Activation has been deliberately separated from creation and initialisation.
At some point in the future, the microprocess's activate method is called,
activating the object. When the object is activated, an  internal call
to a '_microprocessGenerator' occurs. This function in fact results in
the return object being a generator, which can then have its next method
called repeatedly. This generator is  then stored as an attribute of the
microprocess class.

The following describe the flow of control the generator takes when the
generator is provided with a flow of control/time slice via it's next
method. Initially, it creates a local generator object - 'pc' - by calling
the object's main method. (This allows the client of the microprocess class
to provide their own generator if they wish.) This is necessary due to
the fact that any function containing a 'yield' keyword is a  generator -
the 'yield' keyword cannot be abstracted away. Next, inside a loop, the
microprocess checks to see if it is runnable. If the microprocess is
runnable, the local generator object 'pc' has it's next method called -
effectively providing a time slice to the user of the microprocess class.
Any result provided by the timeslice is then yielded (returned) to the
client of the generator. After this, if the microprocess has its stopped
flag set, the microprocess generator simply yields a null value, followed
by stopping.

This all boils down to checking to see if the microprocess is not stopped
and runnable prior to running the body of a generator formed from the
main method of the class. The intent here is that users will inherit from
the microprocess class, and then reimplement the main method, which
periodically yields control. If the user/inheriting class does not implement
a main method, then the system provides a stub that simply returns.

Essentially the microprocess provides a context for scheduling generators,
and treating them similar to processes/threads.

Clients are not expected to use the microprocess class itself directly -
they are expected to subclass the microprocess class. Subclasses do need
however to call the microprocess constructor. A minimal client class could
look like this::

from microprocess import microprocess
class automaton(microprocess):
   def __init__(self):
      self.Microprocess() # Call superclass constructor
   def main:
      while 1:
      yield 1
      print "Hello Again"

This microprocess would then be run by a wrapper as follows::

   import microprocess, scheduler
   s = scheduler.scheduler()
   a = automaton()
   a.activate()
   s._addThread(a)
   s.runThreads()

The component class does this, and adds further facilities for
inter-microprocess communication. Likewise, the postman class subclasses
microprocess so that it can be scheduled in parallel with other tasks.

As noted previously, every microprocess object has access to a debugger,
which is accessed via the local attribute self.debugger, which we shall
return to later. Likewise every microprocess object contains a reference
to a scheduler.
"""

import time
from util import removeAll
from idGen import strId, numId, tupleId
from debug import debug

# Microprocess - provides a framework for clients to inherit
# to be able to participate in a co-operative concurrency
# environment
#
# Specifically, classes that subclass microprocess, and implement
# either a main() generator function can be activated, and
# scheduled by the scheduler/microthread systems. Essentially a
# microprocess provides a minimal runtime context for the
# scheduling & thread handling system.
# 
# An example minimal microprocess is::
# 
#   class bibble(microprocess):
#      def __init__(self, num):
#         self.num = num
#         self.Microprocess()
#      def main():
#         yield 1
#         while 1:
#            print "we loop forever", num
#            yield 1
# 
# Which can have (say) 4 instantiations activated by the following::
#
#    bibble(1).activate()
#    bibble(2).activate()
#    bibble(3).activate()
#    bibble(4).activate()
# 
# If the scheduler isn't running, it'd need running too::
# 
#    scheduler.run.runThreads()
#
# Again, most of this is hidden from you if you are implementing a
# component.
# 
# All methods though are available to components, and hence it's worth
# noting the pause & stop methods, and their purpose/usage.
#
# Attributes of a Microprocess:
#
#    - **init** - A flag to indicate if the microprocess has been correctly
#      initialised or not. This allows the system to check that a client
#      class has in fact called the parent constructor classes as required
#      or not.
#
#    - **id** - a unique numerical id - this is akin to a standard process
#      id.
#
#    - **runnable** - This indicates if the code is runnable or not. The
#      idea here is to support processes that pause until data becomes
#      available, are unpaused in some manner, and then continue.
#
#    - **stopped** - This indicates that the code is being shutdown. If
#      code is stopped, it is essentially removed from the run queue,
#      and given no further time slices.
#
#    - **name** - The name of the microprocess - this is generally used
#      in debugging.
#
#    - **thread** - This is the generator object created by calling the
#      object's main method. Repeatedly calling self.thread.next() provides
#      the generator function in the generator object more time slices.
#
#    - **scheduler** - This is the scheduler to be used for scheduling
#      child processes of the object.
#
#    - **debugger** - A local debugging object. (See the debug class
#      docs for more detail)
#

import Axon
import CoordinatingAssistantTracker as cat

class microprocess(Axon.AxonObject):
   schedulerClass = None
   trackerClass = None

   def setTrackerClass(cls, newTrackerClass):
      cls.trackerClass = newTrackerClass
   setTrackerClass=classmethod(setTrackerClass)

   def setSchedulerClass(cls, newSchedulerClass):
      cls.schedulerClass = newSchedulerClass
   setSchedulerClass=classmethod(setSchedulerClass)

   def setSchedulerClass(cls,newSchedulerClass):
      cls.schedulerClass = newSchedulerClass
   setSchedulerClass = classmethod(setSchedulerClass)

   def __init__(self):
      """Microprocess constructor.
      Subclasses must call this using the idiom super(TheClass, self).__init__()      """
      self.init  = 1
      self.id,self.name = tupleId(self)
      self.__runnable =1
      self.__stopped = 0
      self.__thread = None
      self.scheduler = None
      self.tracker=cat.coordinatingassistanttracker.getcat()

      # If the client has defined a debugger in their class we don't want to override it.
      # However if they haven't, we provide them with one
      if not 'debugger' in self.__dict__.keys():
         self.debugger = debug()
         self.debugger.useConfig()
         if self.debugger.areDebugging("microprocess.__init__", 5):
            self.debugger.debugmessage("microprocess.__init__", "Defining debugger for self", self.__class__)


   def __str__(self):
      """Standard function for rendering the object as a string."""
      result = ""
      result = result + self.name + " :"
      result = result + self.id.__str__() + " :"
      result = result + self.init.__str__() + " :"
      result = result + self.__runnable.__str__() + " :"
      result = result + self.__stopped.__str__() + " :"
      return result

   def next(self):
      """ M.next() - This is to provide a microprocess object with the
      ability to be dropped in largely wherever a generator object can
      be put. Internally this calls self.thread.next() to pass the
      timeslice down to the actual generator."""
      return self.__thread.next()

   def _activityCreator(self):
      return False

   def _isStopped(self):
      """'M._isStopped()' - test, boolean result indicating if the microprocess is halted."""
      if self.debugger.areDebugging("microprocess._isStopped", 1):
         self.debugger.debugmessage("microprocess._isStopped", "self.stopped",self.__stopped)
      return self.__stopped == 1

   def _isRunnable(self):
      """'M._isRunnable()' - test,
      boolean result indicating if the microprocess is paused.
      """
      if self.debugger.areDebugging("microprocess._isRunnable", 10):
         self.debugger.debugmessage("microprocess._isRunnable", "self.runnable",self.__runnable)
      return self.__runnable == 1

   def stop(self):
      """'M.stop()' -
      Halts the microprocess, no way to "unstop" """
      if self.debugger.areDebugging("microprocess.stop", 1):
         self.debugger.debugmessage("microprocess.stop", "Microprocess STOPPED", self.id,self.name,self)
      self.__stopped = 1
      self.__runnable = 0

   def pause(self):
      """'M.pause()' - Pauses the microprocess.
      sets the runnable flag to false - thus pausing the microprocess."""
      if self.debugger.areDebugging("microprocess.pause", 1):
         self.debugger.debugmessage("microprocess.pause", "Microprocess PAUSED", self.id,self.name,self)
      self.__runnable = 0

   def _unpause(self):
      """'M._unpause()' - Un-pauses the microprocess, sets the runnable flag to true.

      Unpauses the microprocess by setting the runnable flag to true.
      This can only be performed by an external microprocess. This is provided
      since it is conceivable that a more complex scheduler than the one at
      present may wish to manipulate this sort of flag.  Does nothing if
      microprocess has been stopped.
      ."""
      if self.debugger.areDebugging("microprocess._unpause", 1):
         self.debugger.debugmessage("microprocess._unpause", "Microprocess UNPAUSED", self.id,self.name,self)
      if not self._isStopped():
         self.__runnable = 1

   def main(self):
      """'M.main()' - stub function. Client classes are expected to override this.

      If you miss this off a class that directly subclass's microprocess, your program
      will run, but it will not do what you want!"""
      if self.debugger.areDebugging("microprocess.main", 0):
         self.debugger.debugmessage("microprocess.main", self.name,"OI! You're only supposed to blow the bloody doors off!")
      "If you ever see the above message in your debug output, you've made a big mistake!"
      yield 1
      return

   def _microprocessGenerator(self,someobject):
      """This contains the mainloop for a microprocess, returning a
      generator object. Creates the thread of control by calling the
      class's main method, then in a loop repeatedly calls the resulting
      generator's next method providing the object with time slices.
      After each time slice, the _microprocessGenerator yields control
      back to its caller.
      """
      # someobject.setthread = (self) # XXXX Check -- Appears no to be used!
      pc = someobject.main() # Call the object, get a generator function
      while(1):
         # Continually try to run the code, and then release control
         if someobject._isRunnable() :
            # If the object is runnable, we run the objectscheduler=
            v = pc.next()
            yield v           # Yield control back - making us into a generator function
         else:
            # Microprocess is not running, has it stopped completely?
            if someobject._isStopped():
               # Microprocess has stopped
               yield None
               return
            else:
               # Microprocess simply paused
               yield "Paused"

   def activate(self, Scheduler=None, Tracker=None):
      """calls the _microprocessGenerator function to create a generator
      object, places this into the thread attribute of the microprocess
      and appends the component to the scheduler's run queue."""

      if self.debugger.areDebugging("microprocess.activate", 1):
         self.debugger.debugmessage("microprocess.activate", "Activating microprocess",self)
      self.__thread = self._microprocessGenerator(self)

      #
      # Whilst a basic microprocess does not "need" a local scheduler,
      # classes inheriting from microprocess may well wish to do so.
      # (Specifically the component class needs that capability)
      #
      if Scheduler is not None:
         if self.debugger.areDebugging("microprocess.activate", 1):
            self.debugger.debugmessage("microprocess.activate", "Activating microprocess",self)
         Scheduler._addThread(self)
         self.scheduler = Scheduler
      else:
         self.__class__.schedulerClass.run._addThread(self)
         self.scheduler = self.__class__.schedulerClass.run
      if Tracker is not None:
         self.tracker = Tracker
      else:
         pass

      if self.debugger.areDebugging("microprocess.activate", 5):
         self.debugger.debugmessage("microprocess.activate", "Using Scheduler",self.scheduler)
      return self

   def _closeDownMicroprocess(self):
      "Stub method that is overridden internally in Axon but not clients"
      return 0

   def run(self):
      "run - activates the microprocess and runs it from start to finish until StopIteration"
      self.activate()
      try:
         while 1:
            self.next()
      except StopIteration:
         pass # Expect this!

if __name__ == '__main__':
   print "Test code currently disabled"
   if 0:
      def microProcessThreadTest():
         class myProcess(microprocess):
            def main(self):
               i = 100
               yield wouldblock(self)
               while(i):
                  i = i -1
                  print "myProcess",self.name, ":", "hello World"
                  yield notify(self,None, 10, "this")
         threadfactory = microthread()
         r = scheduler()
         for i in range(5):
            p = myProcess(i)
            t = threadfactory.activate(p)
            r._addThread(t)
         context = r.runThreads()

      microProcessThreadTest()
