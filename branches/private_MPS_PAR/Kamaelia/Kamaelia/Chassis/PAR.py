#!/usr/bin/env python

# Copyright (C) 2009 British Broadcasting Corporation and Kamaelia Contributors(1)
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
==========================================================
Running components in parallel conveniently, shared output
==========================================================

The PAR component activates all the subcomponents listed to run in parallel
- hence the name - from Occam. Shutdown messages are passed to all
subcomponents. Their shutdown messages propogate out the PAR component's
signal outbox.

Future work will include the ability to define input policies regarding what
to do with messages from the main inbox. (not yet implemented)

For more complex topologies, see the Graphline component.


Example Usage
-------------

One example initially. This::

    Pipeline(
       PAR(
           Button(caption="Next", msg="NEXT", position=(72,8)),
           Button(caption="Previous", msg="PREV",position=(8,8)),
           Button(caption="First", msg="FIRST",position=(256,8)),
           Button(caption="Last", msg="LAST",position=(320,8)),
       ),
       Chooser(items = files),
       Image(size=(800,600), position=(8,48)),
    ).run()

Is equivalent to this::

    Graphline(
         NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
         PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
         FIRST = Button(caption="First", msg="FIRST",position=(256,8)),
         LAST = Button(caption="Last", msg="LAST",position=(320,8)),

         CHOOSER = Chooser(items = files),
         IMAGE = Image(size=(800,600), position=(8,48)),
         linkages = {
            ("NEXT","outbox") : ("CHOOSER","inbox"),
            ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
            ("FIRST","outbox") : ("CHOOSER","inbox"),
            ("LAST","outbox") : ("CHOOSER","inbox"),

            ("CHOOSER","outbox") : ("IMAGE","inbox"),
         }
    ).run()



Shutdown Examples
-----------------

To be written.



How does it work?
-----------------

To be written.


Policies
--------

To be written. The idea behind policies is to allow someone to override the
default behaviour regarding inbox data. This potentially enables the
creation of things like threadpools, splitters, and general workers.


Shutdown Handling
-----------------

To be written.


"""

import Axon
from Axon.Ipc import shutdownMicroprocess
from Axon.Ipc import producerFinished

class PAR(Axon.Component.component):
   """\
   PAR(inputpolicy=None, outputpolicy=None, *components) -> new PAR component

   Activates all the components contained inside in parallel (Hence the name - from Occam).
   
   Inputs to inboxes can be controlled by passing in a policy. The default
   policy is this::

      messages to "control" are forwarded to all children
      
      if a control is a shutdownMicroprocess, shutdown
      
      when all children exit, exit.
      
      messages to "inbox" are forwarded to all components by default.

   See the module docs on writing a policy function. 
   
   Outputs from all outboxes are sent to the graphline's corresponding
   outbox. At present supported outboxes replicated are: "outbox", and
   "signal".
   
   For more complex wiring/policies you probably ought to use a Graphline
   component.

   Keyword arguments:
   
   - policy    -- policy function regarding input mapping.
   - components -- list of components to be activated.
   """
   
   Inboxes = {"inbox":"", "control":""}
   Outboxes = {"outbox":"", 
               "signal":"", 
               "_co": "For passing data to subcomponents based on a policy (unusued at present)",
               "_cs": "For signaling to subcomponents shutdown",
              }
   policy = None
   def __init__(self, *components, **argv):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""

      super(PAR,self).__init__(**argv)
      self.components = list(components)
      

      
   def main(self):
      """Main loop."""
      
      link_to_component_control = {}
      
      noControlPassthru=True
      noSignalPassthru=True
      
      for c in self.components:
          for outbox in ["outbox", "signal"]:
              self.link( (c, outbox), (self, outbox), passthrough=2 )
          c.activate()
      
      self.addChildren(*self.components)
      yield 1

      shutdown = False
      shutdownMessage = None
            
      while not shutdown:
          
          # If all the children exit, then exit
          if self.childrenDone():
              shutdown = True
              break
          
          # If we reach here there may be data in an inbox.
          # May, because a child terminating wakes us up as well.
          if self.policy == None:
              # Default policy: discard all messages sent to the main inbox
              for _ in self.Inbox("inbox"):
                  pass
              
              # Default policy, pass on all control messages to all sub components
              # Shutdown the PAR component if the message is a shutdownMicroprocess message
              for msg in self.Inbox("control"):
                  for c in self.components:

                      L = self.link( (self, "_cs"), (c, "control"))
                      self.send( msg, "_cs")
                      self.unlink(thelinkage=L)

                  if isinstance(msg, shutdownMicroprocess) or (msg==shutdownMicroprocess):
                      shutdown = True
                      shutdownMessage = msg

          # If there's nothing to do, then sleep
          while not self.anyReady():
              self.pause()
              yield 1
          yield 1

      if shutdownMessage:
          self.send(shutdownMessage, "signal")
      else:
          self.send(producerFinished(), "signal")

      for child in self.childComponents():
          self.removeChild(child)   # deregisters linkages for 
   
   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us

       return 0==len(self.childComponents())

__kamaelia_components__  = ( PAR, )


if __name__=="__main__":
   pass    

