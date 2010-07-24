#!/usr/bin/python
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

import Axon
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.Ipc import shutdownMicroprocess, producerFinished

class undef(object):
    pass

class DemuxRemuxTuple(AdaptiveCommsComponent):
   """\
   #
   # FIXME: derived from the PAR component.
   # FIXME: This should really be a PAR component with a new policy.
   # FIXME: For the moment we'll leave it like this to see how this plays out.
   #
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

   Inboxes = {"inbox":"",
              "control":""}
   Outboxes = {"outbox":"", 
               "signal":"", 
               "_co": "For passing data to subcomponents based on a policy (unusued at present)",
               "_cs": "For signaling to subcomponents shutdown",
              }
   policy = None
   def __init__(self, *components, **argv):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""

      super(DemuxRemuxTuple,self).__init__(**argv)
      self.components = list(components)

   def main(self):
      """Main loop."""

      link_to_component_control = {}

      noControlPassthru=True
      noSignalPassthru=True

      subcomponent_inboxes = {}
      subcomponent_controlboxes = {}
      i = 0
      for c in self.components:
          subcomponent_inboxes[i] = self.addInbox("_subinbox_")
          subcomponent_controlboxes[i] = self.addInbox("_subcontrol_")
          self.link( (c, "outbox"), (self, subcomponent_inboxes[i]) )
          self.link( (c, "signal"), (self, subcomponent_controlboxes[i]))
          i += 1

          c.activate()

      self.addChildren(*self.components)
      yield 1

      shutdown = False
      shutdownMessage = None

      box_values = dict( (x,undef) for x in subcomponent_inboxes)

      while not shutdown:
          # If all the children exit, then exit
          if self.childrenDone():
              shutdown = True
              break

          # If we reach here there may be data in an inbox.
          # May, because a child terminating wakes us up as well.
          if self.policy == None:
              # Default policy: discard all messages sent to the main inbox
              for msg in self.Inbox("inbox"):
                  i = 0
                  for c in self.components:
                      L = self.link( (self, "_co"), (c, "inbox"))
                      self.send( msg[i], "_co")
                      self.unlink(thelinkage=L)
                      i += 1

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

              for boxkey in box_values:
                  if  box_values[boxkey] is undef:
                      if self.dataReady(subcomponent_inboxes[boxkey]):
                          message = self.recv(subcomponent_inboxes[boxkey])
                          box_values[boxkey] = message
              if len([x for x in box_values if box_values[x] is undef]) == 0:
                  self.send( tuple([ box_values[x] for x in box_values ]), "outbox")
                  box_values = dict( (x,undef) for x in subcomponent_inboxes)

              for component_name in subcomponent_controlboxes:
                  if self.dataReady(subcomponent_controlboxes[component_name]):
                      message = self.recv(subcomponent_controlboxes[component_name])
                      self.send(message, "signal")

          # If there's nothing to do, then sleep
          while not self.anyReady() and not shutdown and not self.childrenDone():
              self.pause()
              yield 1
          yield 1

      for boxkey in box_values:
          if  box_values[boxkey] is undef:
              if self.dataReady(subcomponent_inboxes[boxkey]):
                  message = self.recv(subcomponent_inboxes[boxkey])
                  box_values[boxkey] = message

      if len([x for x in box_values if box_values[x] is undef]) == 0:
          self.send( tuple([ box_values[x] for x in box_values ]), "outbox")
          box_values = dict( (x,undef) for x in subcomponent_inboxes)

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

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    Pipeline(
        DataSource([
                        (1,"one"),
                        (2,"two"),
                        (3,"three"),
                        (4,"four"),
                        (5,"five"),
                        (6,"six"),
                   ]),
        DemuxRemuxTuple(                  # Detuple
            PureTransformer(lambda x: x*x),     # Process First item from tuple
            PureTransformer(lambda x: x+" "+x), # Process Second item from tuple
        ),                                # Retuple
        PureTransformer(lambda x: repr(x)+"\n"),
        ConsoleEchoer(),
    ).run()
