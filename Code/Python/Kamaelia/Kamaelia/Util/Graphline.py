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
   def __init__(self, linkages = None, **components):
      if linkages is None:
         raise ValueError("linkages must be set")
      super(Graphline,self).__init__()
      self.layout = linkages
      self.components = dict(components)

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
#      while 1:
#         self.pause()
#         yield 1

      # run until all child components have terminated
      # at which point this component can implode

      # could just look for the first and last component terminating (children with linkages to graphline)
      # BUT the creator of this pipeline might assume that the graphline terminating means ALL
      # children have finished.
      while not self.childrenDone():
          yield 1
          
      self.unplugChildren()
      

   def childrenDone(self):
       """Returns true if all components have terminated
          (ie. their microproceses have finished)
       """
       return False not in [ child._isStopped() for child in self.components.values() ]

   def unplugChildren(self):
      for child in self.components.values():
         self.postoffice.deregisterlinkage(thecomponent=child)
         self.removeChild(child)
                  
if __name__=="__main__":
   pass    