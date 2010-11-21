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
=====================================
Components - the basic building block
=====================================

A component is a microprocess with a microthread of control and input/output
queues (inboxes and outboxes) which can be connected by linkages to other
components. Ie. it has code that runs whilst the component is active, and
mechanisms for sending and receiving data to and from other components.

* A component is based on a microprocess - giving it its thread of execution.

There are other variants on the basic component:
    
* Axon.AdaptiveCommsComponent.AdaptiveCommsComponent
* Axon.ThreadedComponent.threadedcomponent
* Axon.ThreadedComponent.threadedadaptivecommscomponent

If your component needs to block - eg. wait on a system call; then make it a
'threaded' component. If it needs to change what inboxes or outboxes it has at
runtime, then make it an 'adaptive' component.



The basics of writing a component
---------------------------------

Here's a simple example::

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


Or, more specifically:

1. **Subclass the component class**. Don't forget to call the superclass
   initializer if you write your own __init__ method::

        class MyComponent(Axon.Component.component):

            def __init__(self, myArgument, ...):
                super(MyComponent, self).__init__()
                ...

2. **Declare any inboxes or outboxes you expect it to have** - do this as
   static members of the class called "Inbox" and "Outbox". They should be
   dictionaries where the key is the box name and the value serves as documentation
   describing what the box is for::

        Inboxes = { "inbox"   : "Send the FOO objects to here",
                    "control" : "NOT USED",
                  }
        Outboxes = { "outbox" : "Emits BAA objects from here",
                     "signal" : "NOT USED",
                   }

   You can also do this as lists, but doing it as a dictionary with documentation
   values is much more useful to people wanting to use your component.

   If you don't specify any then you get the default "inbox" and "control"
   inboxes and "outbox" and "signal" outboxes.

3. **Write the main() method** - it must be a generator - namely just like an
   ordinary method or function, but with 'yield' statements regularly
   interspersed through it. This is the thread of execution in the component -
   just use yield statements regularly so other components get time to execute.

   If you need to know more, these might help you:

   * `A tutorial on "How to write components" <http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1113495151>`_
   * `the Mini Axon tutorial <http://kamaelia.sourceforge.net/MiniAxon/>`_
   * the Axon.Microprocess.microprocess class


   
Running a component
-------------------

Once you have written your component class; simply create instances and activate
them; then start the scheduler to begin execution::

    x = MyComponent()
    y = MyComponent()
    z = AnotherComponent()
    x.activate()
    y.activate()
    z.activate()

    scheduler.run.runThreads()

If the scheduler is already running, then simply activating a component will
start it executing.



Communicating with other components - creating linkages
-------------------------------------------------------

Components have inboxes and outboxes. The main() thread of execution in a
component communicates with others by picking up messages that arrive in its
inboxes and sending out messages to its outboxes. For example here is a simple
block of code for the main() method of a component that echoes anything it
receives to the console and also sends it on::

    if self.dataReady("inbox"):
        msg = self.recv("inbox")
        print str(msg)
        self.send(msg,"outbox")

    yield 1

Use the dataReady() method to find out if there is (one or more items of) data
waiting at the inbox you name. recv() lets you collect a message from an inbox.
Use the send() method to send a message to the outbox you name. There is also an
anyReady() method that will tell you if *any* inbox has data waiting in it.

A message gets from one component's outbox to another one's inbox if there is a
linkage between them (going from the outbox to the inbox). A component can
create and destroy linkages by using the link() and unlink() methods.

For example, we could create a linkage from a component's outbox called "outbox"
to a different component's inbox called "inbox"::

    theLink = self.link( (self, "outbox"), (otherComponent, "inbox") )

Using the handle that we were given, we can destroy that linkage later::

    self.unlink(theLinkage = theLink)

Linkages normally go from an outbox to an inbox - after all the whole idea is
to get messages that one component sends to its own outbox to arrive at another
component's inbox. However you can also create 'passthrough' linkages from an
inbox to another inbox; or from an outbox to another outbox.

This is particularly useful if you want to encapsulate a child component - hide
it from view so other components only need to be wired up to you.

For example, your component may want any data being sent to one of its inboxes
to be forwarded automatically onto an inbox on the child. This is a type '1'
passthrough linkage::

    thelink = self.link( (self,"inbox"), (myChild,"inbox"), passthrough=1 )

Or if you want anything a child sends to its outbox to be sent out of one of
your own outboxes, which is a type '2' passthrough::

    thelink = self.link( (myChild,"outbox"), (self,"outbox"), passthrough=2 )

The alternative, of course, is to add extra inboxes and outboxes to communicate
with the child, and to write a main() method that simply passes the data on.
Passthrough linkages are more efficient and quicker to code!

There is no performance penalty for delivering a message along a such a chain of
linkages (eg. outbox ---> outbox ---> inbox ---> inbox ---> inbox). Axon
resolves the chain and delivers straight to the final destination inbox!



Child components
----------------

Components can create and activate other components. They can adopt them as
children::

    newComponent = FooComponent()
    self.addChildren(newComponent)
    newComponent.activate()

Making a component your child means that:

* you will be woken (if asleep) when your child terminates

* the removeChild() method provides a convenient way to make sure any linkages
  you have made involving that child are destroyed.

* calling childComponents() lists all children you currently have

Whether another component is your child or not, you can tell if it has
terminated yet by calling its _isStopped() method.

For example, a component might want to create a child component, make a linkage
to it then wait until that child terminates before cleaning it up. Achieve this
by writing code like this in the main() body of the component::

    src = RateControlledFileReader("myTextFile",readmode="lines")
    dst = ConsoleEchoer()

    lnk = self.link( (src,"outbox"), (dst,"inbox") )

    self.addChildren(src,dst)    # we will be woken if they terminate
    src.activate()
    dst.activate()

    while not dst._isStopped() and not src._isStopped():
        self.pause()
        yield 1

    self.unlink(thelinkage = lnk)
    self.removeChild(src)
    self.removeChild(dst)
    




Going to sleep (pausing)
------------------------

When a component has nothing to do it can pause. This means it will not be
executed again until it is woken up. Pausing is a good thing since it
relinquishes cpu time for other parts of the system instead of just wasting it.

**When would you want to pause?** - usually when there is nothing left waiting
in any of your inboxes and there is nothing else for your component to do::

    class Echoer(Axon.Component.component):

        def main(self):
            while 1:
                if self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    print str(msg)
                    self.send(msg,"outbox")

                if not self.anyReady():
                    self.pause()

                yield 1

Calling the pause() method means that *at the next yield statement* your
component will be put to sleep. It doesn't happen as soon as you call pause() -
only when execution reaches the next ``yield``.

**What will wake up a paused component?** - any of the following:

* a message arriving at any inbox (even one with messages already waiting in it)
* a message being collected from an inbox that is linked to one of our outboxes
* a child component terminating

Your component *cannot* wake itself up - only the actions of other components
can cause it to be woken. Why? You try writing some code that stops executing
(pauses) yet can issue a method call to ask to be woken! :-)



Old style main thread
---------------------

Components also currently support an 'old' style for writing their main thread
of execution. 

**This way of writing components is likely to be deprecated in the near future.
We suggest you write a main() method as a generator instead.**

To do old-style; instead of writing a generator you write 3 functions - one for
initialisation, main execution and termination. The thread of execution for the
component is therefore effectively this::

    self.initialiseComponent()
    
    while 1:
        result = self.mainBody()
        if not result:
            break
    
    self.closeDownComponent()

initialiseComponent() is called once when the component first starts to
execute.


mainBody() is called every execution cycle whilst it returns a non zero
value. If it returns a zero value then the component starts to shut down.

closeDownComponent() is called when the component is about to shut down.

A simple echo component might look like this::

    class EchoComponent(Axon.Component.component):

        def initialiseComponent(self):
            # We can perform pre-loop initialisation here!
            # In this case there is nothing really to do
            return 1

        def mainBody(self):
            # We're now in the main loop
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                print msg
                self.send(msg,"outbox")

            if not self.anyReady():
                self.pause()

            # If we wanted to exit the loop, we return a false value
            # at the end of this function
            # If we want to continue round, we return a true, non-None,
            # value. This component is set to run & run...
            return 1

      def closeDownComponent(self):
            # We can't get here since mainLoop above always returns true
            # If it returned false however, we would get sent here for
            # shutdown code.
            # After executing this, the component stops execution
            return



Internal Implementation
-----------------------

Component is a subclass of microprocess (from which it inherits the ability to
have a thread of execution). It includes its own postoffice object for creating
and destroying linkages. It has a collection of inboxes and outboxes.
 
Attributes:

* **Inboxes** and **Outboxes** - static members defining the list of names for
  inboxes and outboxes a component should be given when it is created.
          
* **inboxes** and **outboxes** - the actual collections of inboxes and outboxes
  that are set up when the component is initialised. Implemented as dictionaries
  mapping names to the postbox objects.

* **postoffice** - a postoffice object, used to create, destroy and manage
  linkages.
  
* **children** - list of components registered as children of this component.

* **_callOnCloseDown** - list of callback functions to be called when this
  component terminates. Used to notify parents of children that their child has
  terminated.

"""
import time

from util import removeAll
from idGen import strId, numId
from debug import debug
from Microprocess import microprocess
from Postoffice import postoffice
from Scheduler import scheduler
from AxonExceptions import noSpaceInBox
from Linkage import linkage
from Ipc import *


from Box import makeInbox,makeOutbox

TraceAllSends = False
TraceAllRecvs = False

class component(microprocess):
   """\
   Base class for an Axon component. Subclass to make your own.

   A simple example::

      class IncrementByN(Axon.Component.component):

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
                      
                  yield 1
   """
          
   Inboxes  = {"inbox" : "Default inbox for bulk data. Used in a pipeline much like stdin",
               "control" : "Secondary inbox often used for signals. The closest analogy is unix signals"
              }
              
   Outboxes = {"outbox": "Default data out outbox, used in a pipeline much like stdout",
               "signal": "The default signal based outbox - kinda like stderr, but more for sending singal type signals",
              }
   
   Usescomponents=[]

   def __init__(self, *args, **argd):
      """You want to overide this method locally.

      You MUST remember to call the superconstructor for things to work however.
      The way you do this is: super(YourClass,self).__init__()
      """
      super(component, self).__init__()
      self.__dict__.update(argd)
      self.inboxes = dict()
      self.outboxes = dict()

      # Create boxes for inboxes/outboxes
      for boxname in self.Inboxes:
          self.inboxes[boxname] = makeInbox(notify=self.unpause)
      for boxname in self.Outboxes:
          self.outboxes[boxname] = makeOutbox(notify=self.unpause)

      self.children = []
      self._callOnCloseDown = []

      self.postoffice = postoffice("component :" + self.name)
      if TraceAllSends:
          self._o_send = self.send
          self.send = self._debug_send
      if TraceAllRecvs:
          self._o_recv = self.recv
          self.recv = self._debug_recv


   def setInboxSize(self, boxname, size):
       "boxname - some boxname, must be an inbox ; size - maximum number of items we're happy with"
       self.inboxes[boxname].setSize(size)

   def __str__(self):
      """Provides a useful string representation of the component.
      You probably want to override this, and append this description using
      something like: 'component.__str__(self)'
      """
      result = "Component " + self.name + " [ inboxes : " + self.inboxes.__str__() + " outboxes : " + self.outboxes.__str__()
      return result

   def __addChild(self, child):
      """\
      Register component as a child.

      This takes a child component, and adds it to the children list of this
      component. It also registers to be woken up by the child if it terminates.

      This has a number of effects internally, and includes
      registering the component as capable of recieving and sending messages.
      It doesn't give the child a thread of control however!

      You will want to call this function if you create child components of your
      component.
      """
      try:
          child._callOnCloseDown.append(self.unpause)
          self.children.append(child)
      except Exception, e:
          print "WARNING, I really REALLY should not be showing you this error for", str(child)
          print "         What you have probably done is used a CLASS where you "
          print "         should have used an instance"
          print "         eg You meant to use ExampleProtocol() but actually had"
          print "                             ExampleProtocol - ie you missed off instantiation"
          raise e

   def addChildren(self,*children):
      """\
      Register the specified component(s) as children of this component

      This component will be woken if any of its children terminate.

      Note that any children still need to be activated!
      """
      for child in children:
         self.__addChild(child)

   def removeChild(self, child):
      """\
      Deregister component as a child.

      Removes the child component, and deregisters it from notifying us when it
      terminates. Also removes any linkages this component has made that
      involve this child.

      You probably want to do this when you enter a closedown state
      of some kind for either your component, or the child component.
      """
      removeAll(self.children, child)
      removeAll(child._callOnCloseDown, self.unpause)
      self.postoffice.unlink(thecomponent=child)

   def childComponents(self):
      """\
      Returns list of child components
      """
      return self.children[:]

   def anyReady(self):
       """\
       Returns true if *any* inbox has any data waiting in it.

       Used by a component to check an inbox for ready data.
      
       You are unlikely to want to override this method.
       """
       for box in self.inboxes:
          if self.dataReady(box):
             if box:
                return box 
             else:
                return True
       return False

   def dataReady(self,boxname="inbox"):
      """\
      Returns true if data is available in the requested inbox.

      Used by a component to check an inbox for ready data.
      
      Call this method to periodically check whether you've been sent any
      messages to deal with!

      You are unlikely to want to override this method.
      """
      return self.inboxes[boxname].local_len()


   def link(self, source,sink,*optionalargs, **kwoptionalargs):
      """\
      Creates a linkage from one inbox/outbox to another.

      -- source  - a tuple (component, boxname) of where the link should start from
      -- sink    - a tuple (component, boxname) of where the link should go to

      Other optional arguments:

      - passthrough=0  - (the default) link goes from an outbox to an inbox
      - passthrough=1  - the link goes from an inbox to another inbox
      - passthrough=2  - the link goes from an outbox to another outbox

      See Axon.Postoffice.postoffice.link() for more information.
      """
#      print "DEBUGLINK", self.name, source, sink
      return self.postoffice.link(source, sink, *optionalargs, **kwoptionalargs)


   def unlink(self, thecomponent=None, thelinkage=None):
       """\
       Destroys all linkages to/from the specified component or destroys the
       specific linkage specified.

       Only destroys linkage(s) that were created *by* this component itself.
       
       Keyword arguments:
       
       - thecomponent -- None or a component object
       - thelinkage   -- None or the linkage to remove
      
       See Axon.Postoffice.postoffice.unlink() for more information.
       """
       return self.postoffice.unlink(thecomponent,thelinkage)


   def recv(self,boxname="inbox"):
      """\
      returns the first piece of data in the requested inbox.

      Used by a component to recieve a message from the outside world.
      All comms goes via a named box/input queue

      You will want to call this method to actually recieve messages you've been
      sent. You will want to check for new messages using dataReady first
      though.

      You are unlikely to want to override this method.
      """
      return self.inboxes[boxname].pop(0)

   def _debug_recv(self,boxname="inbox"):
      shortname = self.name[self.name.rfind(".")+1:]
      message = self._o_recv(boxname)
      print "RECV: %s %s '%s' : %s" % (str(id(message)), shortname , boxname, str(message))
      return message


   def Inbox(self, boxname="inbox"):
       while self.dataReady(boxname):
           yield self.recv(boxname)

   def send(self,message, boxname="outbox"):
      """\
      appends message to the requested outbox.

      Used by a component to send a message to the outside world.
      All comms goes via a named box/output queue.

      You will want to call this method to send messages.
      
      Raises Axon.AxonExceptions.noSpaceInBox if this outbox is linked to a
      destination inbox that is full.

      You are unlikely to want to override this method.
      """
      self.outboxes[boxname].append(message)

   def _debug_send(self,message, boxname="outbox"):
      shortname = self.name[self.name.rfind(".")+1:]
      
      print "SEND: %s %s '%s' : %s" % (str(id(message)), shortname , boxname, str(message))
      self._o_send(message, boxname)
       

   def main(self):
      """\
      Override this method, writing your own main thread of control as a generator.
      When the component is activated and the scheduler is running, this what
      gets executed.

      Write it as a python generator with regular yield statements returning a
      non zero value.

      If you do not override it, then a default main method exists instead that
      will:

      1. Call self.initialiseComponent()
      2. Loop forever calling self.mainBody() yielding the return value each time
         until mainBody() returns a False/zero result.
      3. Call self.closeDownComponent()
      """
      result = self.initialiseComponent()
      if not result:
         result = 1
      yield result
      while(result):
         result = self.mainBody()
         if result:
            yield result
      yield self.closeDownComponent()

   def initialiseComponent(self):
      """Stub method. **This method is designed to be overridden.** """
      return 1
   def mainBody(self):
      """Stub method. **This method is designed to be overridden.** """
      return None
   def closeDownComponent(self):
      """Stub method. **This method is designed to be overridden.** """
      return 1
   
   def _closeDownMicroprocess(self):
      """\
      Overrides original in microprocess class.
      
      Ensures callbacks are deregistered, and all linkages created by
      this component are destroyed.
      """
      for callback in self._callOnCloseDown:
          callback()
      self.postoffice.unlinkAll()
      return None

   def _deliver(self, message, boxname="inbox"):
       """For tests and debugging ONLY - delivers message to an inbox."""
       self.inboxes[boxname].append(message)

if 0: # if __name__ == '__main__':
   def producersConsumersSystemTest():
      class Producer(component):
         Inboxes=[]
         Outboxes=["result"]
         def __init__(self):
            super(producersConsumersSystemTest, self).__init__()
         def main(self):
            i = 100
            while(i):
               i = i -1
               self.send("hello", "result")
               yield  1

      class Consumer(component):
         Inboxes=["source"]
         Outboxes=["result"]
         def __init__(self):
            super(Consumer, self).__init__()
            self.count = 0
            self.i = 30
         def doSomething(self):
            print self.name, "Woo",self.i
            if self.dataReady("source"):
               self.recv("source")
               self.count = self.count +1
               self.send(self.count, "result")

         def main(self):
            yield 1
            while(self.i):
               self.i = self.i -1
               self.doSomething()
               yield 1

      class testComponent(component):
         Inboxes=["_output"]
         Outboxes=["output"]
         def __init__(self):
            super(testComponent, self).__init__()

            self.lackofinterestingthingscount = 0
            self.total = 0

            self.producer, self.consumer =Producer(), Consumer()
            self.producer2, self.consumer2 = Producer(), Consumer()

            self.addChildren(self.producer, self.producer2, self.consumer, self.consumer2)

            self.link((self.producer, "result"), (self.consumer, "source"))
            linkage(self.producer2, self.consumer2, "result", "source", self.postoffice)
            linkage(self.consumer,self,"result","_output", self.postoffice)
            linkage(self.consumer2,self,"result","_output", self.postoffice)
         def childComponents(self):
            return [self.producer, self.consumer,self.producer2, self.consumer2]
         def mainBody(self):
            if len(self.inboxes["_output"]) > 0:
               result = self.recv("_output")
               self.total = self.total + result
               print "Result recieved from consumer : ", result, "!"
               print "New Total : ", self.total, "!"
            else:
               self.lackofinterestingthingscount = self.lackofinterestingthingscount +1
               if self.lackofinterestingthingscount > 2:
                  print "Exiting. Nothing interesting for ", self.lackofinterestingthingscount, " iterations"
                  return 0
            return 1

      r = scheduler()
      p = testComponent()
      children = p.childComponents()
      p.activate()
      for p in children:
         p.activate()
      scheduler.run.runThreads(slowmo=0)# context = r.runThreads()

   producersConsumersSystemTest()
