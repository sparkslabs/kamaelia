#!/usr/bin/env python

# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

# component that creates and encapsulates a pipeline of components, connecting
# their outbox to inbox, and signal to control to form the pipeline chain.

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

component = _Axon.Component.component


class Graphline(component):
   Inboxes = {"inbox":"", "control":""}
   Outboxes = {"outbox":"", "signal":""}
    
   def __init__(self, linkages = None, **components):
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
                 except KeyError, IndexError:
                     self.Inboxes[sourceBox] = ""

         if toComponent == self:
             if toBox not in self.Outboxes:
                 # add outbox to list, and copy any description text (if it exists)
                 try:
                     self.Outboxes[toBox] = fromComponent.Outboxes[sourceBox]
                 except KeyError, IndexError:
                     self.Outboxes[toBox] = ""
      
   def main(self):
      # NEW CODE
      components = []
      for componentRef,sourceBox in self.layout:
         toRef, toBox = self.layout[(componentRef,sourceBox)]
         fromComponent = self.components.get(componentRef, self)
         toComponent = self.components.get(toRef, self)

         if fromComponent != self and fromComponent not in components: components.append(fromComponent)
         if toComponent   != self and toComponent   not in components: components.append(toComponent)

         passthrough = 0
         if fromComponent == self: passthrough = 1
         if toComponent == self: passthrough = 2
         if (fromComponent == self) and (toComponent == self):
            passthrough = 0
            print "WARNING, assuming linking outbox to inbox on the graph. This is a poor assumption"
         
         self.link((fromComponent,sourceBox), (toComponent,toBox), passthrough=passthrough)

      self.addChildren(*components)
      yield _Axon.Ipc.newComponent(*(self.children))

      # run until all child components have terminated
      # at which point this component can implode

      # could just look for the first and last component terminating (children with linkages to graphline)
      # BUT the creator of this pipeline might assume that the graphline terminating means ALL
      # children have finished.
      while not self.childrenDone():
          # can't self.pause() as children may not pass data in/out of this graphline, or may not immediately terminate
          yield 1
          
      self.unplugChildren()
      

   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us
               
       return 0==len(self.childComponents())

           
   def unplugChildren(self):
      for child in self.childComponents():
         self.removeChild(child)   # deregisters linkages for us

         
                  
if __name__=="__main__":
   pass    