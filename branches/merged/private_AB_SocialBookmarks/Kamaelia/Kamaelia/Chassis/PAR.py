#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

This component is well behaved with regard to shutdown. It has the following behaviour: if
it recieves a shutdownMicroprocess message on it's control box, it forwards a copy of this
to all the subcomponents. When they exit, this component exits. This enables it to be used
to shutdown entire systems cleanly. For example, the above example using PAR can be shutdown
after 15 seconds using this code::

    class timedShutdown(Axon.ThreadedComponent.threadedcomponent):
        TTL = 1
        def main(self):
            time.sleep(self.TTL)
            self.send(Axon.Ipc.shutdownMicroprocess(), "signal")

    Pipeline(
        timedShutdown(TTL=5),
        Pipeline(
            PAR(
                Button(caption="Next",     msg="NEXT", position=(72,8)),
                Button(caption="Previous", msg="PREV", position=(8,8)),
                Button(caption="First",    msg="FIRST" ,position=(256,8)),
                Button(caption="Last",     msg="LAST", position=(320,8)),
            ),
            Chooser(items = files),
            Image(size=(800,600), position=(8,48), maxpect=(800,600)),
        ),
    ).run()

For a larger example, the following is also a well behaved with regard to shutdown
from PAR components - despite containing a ticker, buttons, 2 different video playback
subsystems, two "talker text" panes, and a presentation tool::

    Pipeline(
            timedShutdown(TTL=15),
            PAR(
                Pipeline(
                         ReadFileAdaptor(file, readmode="bitrate",
                                         bitrate = 300000*8/5),
                         DiracDecoder(),
                         MessageRateLimit(framerate),
                         VideoOverlay(position=(260,48), size=(200,300)),
                ),
                Pipeline( ReadFileAdaptor(file, readmode="bitrate", bitrate = 2280960*8),
                          DiracDecoder(),
                          ToRGB_interleaved(),
                          VideoSurface(size=(200, 300), position=(600,48)),
                ),
                Pipeline(
                    PAR(
                        Button(caption="Next",     msg="NEXT", position=(72,8)),
                        Button(caption="Previous", msg="PREV", position=(8,8)),
                        Button(caption="First",    msg="FIRST" ,position=(256,8)),
                        Button(caption="Last",     msg="LAST", position=(320,8)),
                    ),
                    Chooser(items = files),
                    Image(size=(200,300), position=(8,48), maxpect=(200,300)),
                ),
                Pipeline(
                    Textbox(size=(200,300), position=(8,360)),
                    TextDisplayer(size=(200,300), position=(228,360)),
                ),
                Ticker(size=(200,300), position=(450,360)),
            ),
    ).run()


How does it work?
-----------------

As present this is a relatively simple container component. It links all the outboxes
from all it's subcomponents to it's own outboxes. It then activates them all, and pauses.
When awoken by a message on the control inbox, this is forwared to the child components
in order to shutdown.

Policies
--------

To be written. The idea behind policies is to allow someone to override the
default behaviour regarding inbox data. This potentially enables the
creation of things like threadpools, splitters, and general workers.


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
          # We shouldn't pause if a shutdownMicroprocess was sent to us (hence the flag)
          if not self.anyReady() and not shutdown:
              self.pause()
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

