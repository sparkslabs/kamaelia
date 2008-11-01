#!/usr/bin/env python

# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
==================================
Wiring up components in a topology
==================================

The Graphline component wires up a set of components and encapsulates them as a
single component. They are wired up to each other using the 'graph' of linkages
that you specify.



Example Usage
-------------
Joining a PromtedFileReader and a rate control component to make a file reader
that reads at a given rate::

   return Graphline(RC  = ByteRate_RequestControl(**rateargs),
                    RFA = PromptedFileReader(filename, readmode),
                    linkages = { ("RC",  "outbox")  : ("RFA", "inbox"),
                                ("RFA", "outbox")  : ("self", "outbox"),
                                ("RFA", "signal")  : ("RC",  "control"),
                                ("RC",  "signal")  : ("self", "signal"),
                                ("self", "control") : ("RFA", "control")
                                }

The references to 'self' create linkages that passes through a named inbox on
the graphline to a named inbox of one of the child components. Similarly a
child's outbox is pass-through to a named outbox on the graphline.

## XXXX FIXME: Will be sensible to include a more complex example here including the shutdown behaviour


How does it work?
-----------------

A Graphline component gives you a way of wiring up a system of components and
then encapsulating th ewhole as a single component, with its own inboxes and
outboxes.

The components you specify are registered as children of the Graphline
component. When you activate the component, all the child components are
activated, and the linkages you specified are created between them.

When specifying linkages, the component 'name' is the string version of the
argument name you used to refer to the component. In the example above, the
components are therefore referred to as "RC" and "RFA".

If the name you specify is not one of the components you specify, then it is
assumed you must be referring to the Graphline component itself. In the above
example, "self" is used to make this clear. This gives you a way of passing data
in and out of the system of components you have specified.

In these cases, it is assumed you wish to create a pass-through linkage - you
want the Graphline component to forward the named inbox to a child's inbox, or
to forward a child's outbox to a named outbox of the Graphline. For example::

    Graphline( child = MyComponent(...),
               linkages = { ...
                            ("self", "inbox") : ("child", "bar"),
                            ... }
             )

... is interpreted as meaning you want to forward the "inbox" inbox of the
Graphline to the "bar" inbox of the component referred to as "child".
Similarly::

    Graphline( child = MyComponent(...),
               linkages = { ...
                            ("child", "fwibble") : ("self", "outbox"),
                            ... }
             )

...is interpreted as wishing to forward the "fwibble" outbox of the component
referred to as "child" to the "outbox" outbox of the Graphline component.

Any inbox or outbox you name on the Graphline component is created if it does
not already exist. For example, you might want the Graphline to have a "video"
and an "audio" inbox::

    Graphline( videoHandler = MyVideoComponent(),
               audioHandler = MyAudioComponent(),
               linkages = { ...
                            ("self", "video") : ("videoHandler", "inbox"),
                            ("self", "audio") : ("audioHandler", "inbox"),
                            ...
                          }
             )

The Graphline component will always have inboxes "inbox" and "control" and
outboxes "outbox" and "signal", even if you do not specify any linkages to them.

During runtime, the Graphline component monitors the child components. It will
terminate if, and only if, *all* the child components have also terminated.

NOTE that if your child components create additional components themselves, the
Graphline component will not know about them. It only monitors the components it
was originally told about.

Graphline does not intercept any of its inboxes or outboxes. It ignores whatever
traffic flows through them. If you have specified linkages from them to
components inside the graphline, then the data automatically flows to/from them
as you specified.

## XXXX FIXME: This needs updating to discuss the shutdown behaviour.

"""

# component that creates and encapsulates a pipeline of components, connecting
# their outbox to inbox, and signal to control to form the pipeline chain.

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon
from Axon.Ipc import shutdownMicroprocess
from Axon.Ipc import producerFinished

component = _Axon.Component.component


class Graphline(component):
   """\
   Graphline(linkages,**components) -> new Graphline component

   Encapsulates the specified set of components and wires them up with the
   specified linkages.

   Keyword arguments:
   
   - linkages    -- dictionary mapping ("componentname","boxname") to ("componentname","boxname")
   - components  -- dictionary mapping names to component instances (default is nothing)
   """
   
   Inboxes = {"inbox":"", "control":""}
   Outboxes = {"outbox":"", "signal":"", "_cs": "For signaling to subcomponents shutdown"}
    
   def __init__(self, linkages = None, **components):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      if linkages is None:
         raise ValueError("linkages must be set")

      self.layout = linkages
      self.components = dict(components)

      # adds to 'Inboxes' and 'Outboxes' before superclass takes those lists to create them
      self.addExternalPostboxes()
      
      super(Graphline,self).__init__()


   def addExternalPostboxes(self):
      """Adds to self.Inboxes and self.Outboxes any postboxes mentioned in self.layout that don't yet exist"""
      for componentRef,sourceBox in self.layout:
         toRef, toBox = self.layout[(componentRef,sourceBox)]
         fromComponent = self.components.get(componentRef, self)
         toComponent = self.components.get(toRef, self)

         if fromComponent == self:
             if sourceBox not in self.Inboxes:
                 # add inbox to list, and copy any description text (if it exists)
                 try:
                     self.Inboxes[sourceBox] = toComponent.Inboxes[toBox]
                 except (KeyError, IndexError, TypeError):
                     self.Inboxes[sourceBox] = ""

         if toComponent == self:
             if toBox not in self.Outboxes:
                 # add outbox to list, and copy any description text (if it exists)
                 try:
                     self.Outboxes[toBox] = fromComponent.Outboxes[sourceBox]
                 except (KeyError, IndexError, TypeError):
                     self.Outboxes[toBox] = ""
      
   def main(self):
      """Main loop."""
      
      link_to_component_control = {}
      
      noControlPassthru=True
      noSignalPassthru=True

      for componentRef,sourceBox in self.layout:
         toRef, toBox = self.layout[(componentRef,sourceBox)]

         fromComponent = self.components.get(componentRef, self)
         toComponent = self.components.get(toRef, self)

         if toBox == "control":
             link_to_component_control[toComponent] = False

         passthrough = 0
         if fromComponent == self: passthrough = 1
         if toComponent == self: passthrough = 2
         if (fromComponent == self) and (toComponent == self):
            passthrough = 0
            print "WARNING, assuming linking outbox to inbox on the graph. This is a poor assumption"
         
         self.link((fromComponent,sourceBox), (toComponent,toBox), passthrough=passthrough)

         if fromComponent==self and sourceBox=="control":
             noControlPassthru=False

         if toComponent == self and toBox == "signal":
             noSignalPassthru=False

      for ref in self.components.values():
          if link_to_component_control.get(ref, None) == None:
              link_to_component_control[ref] = True

      self.addChildren(*self.components.values())
      self.components_to_get_control_messages = []
      for ref in link_to_component_control:
          if link_to_component_control[ref]:
              self.components_to_get_control_messages.append( ref )

      for child in self.children:
          child.activate()

## XXXX FIXME: Would be nice to have a clearer name for this
      shutdownMprocMsg=None

      # run until all child components have terminated
      # at which point this component can implode

      # becuase they are children, if they terminate, we'll be woken up
      while not self.childrenDone():
          if not self.anyReady():
              self.pause()
          
          if noControlPassthru and self.dataReady("control"):
              msg = self.recv("control")
              for toComponent in self.components_to_get_control_messages:
## XXXX FIXME: Worth noting that self.link here may fail if the subcomponent
## XXXX FIXME: is linked to whilst the graphline is running. If that
## XXXX FIXME: happens, we should catch it, and allow the link to continue
## XXXX FIXME: elsewhere

                  L = self.link( (self, "_cs"), (toComponent, "control"))

                  self.send( msg, "_cs")
                  yield 1
                  self.unlink(thelinkage=L)

              if isinstance(msg, shutdownMicroprocess) or (msg==shutdownMicroprocess):
                  shutdownMprocMsg=msg
          
          yield 1
   
      if noSignalPassthru:
          if shutdownMprocMsg!=None:
              self.send(shutdownMprocMsg, "signal")
          else:
              self.send(producerFinished(), "signal")
   
   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us

       return 0==len(self.childComponents())

__kamaelia_components__  = ( Graphline, )


if __name__=="__main__":
   pass    

