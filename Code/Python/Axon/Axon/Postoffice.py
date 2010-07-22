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
================
Axon postoffices
================

A postoffice object looks after linkages. It can create and destroy them and
keeps records of what ones currently exist. It hands out linkage objects that
can be used as handles to later unlink (remove) the linkage.

THIS IS AN AXON INTERNAL! If you are writing components you do not need to
understand this.

Developers wishing to understand how Axon is implemented should read on with
interest!



How is this used in Axon?
-------------------------

Every component has its own postoffice. The component's link() and unlink()
methods instruct the post office to create and remove linkages.

When a component terminates, it asks its post office to remove any outstanding
linkages.



Example usage
-------------

Creating a link from an inbox to an outbox; a passthrough link from an inbox
to another inbox; and a passthrough link from an outbox to another outbox::
    
    po = postoffice()
    c0 = component()
    c1 = component()
    c2 = component()
    c3 = component()

    link1 = po.link((c1,"outbox"), (c2,"inbox"))
    link2 = po.link((c2,"inbox"), (c3,"inbox"), passthrough=1)
    link3 = po.link((c0,"outbox"), (c1,"outbox"), passthrough=2)

Removing one of the linkages; then all linkages involving component c3; then all
the rest::
    
    po.unlink(thelinkage=link3)
    
    po.unlink(thecomponent=c3)
    
    po.unlinkAll()



More detail
-----------

A postoffice object keeps creates and destroys objects and keeps a record of
which ones currently exist.

The linkage object returned when a linkage is created serves only as a handle.
It does not form any operation part of the linkage.

Multiple postoffices can (in fact, will) exist in an Axon system. Each looks
after its own collection of linkages. A linkage created at one postoffice will
*not* be known to other postoffice objects.

"""


import time

from util import removeAll
from idGen import strId, numId
from debug import debug
from AxonExceptions import AxonException
from AxonExceptions import BoxAlreadyLinkedToDestination
from Linkage import linkage

class postoffice(object):
   """\
   The post office looks after linkages between postboxes, thereby ensuring
   deliveries along linkages occur as intended.
   
   There is one post office per component.

   A Postoffice can have a debug name - this is to help differentiate between
   postoffices if problems arise.
   """
   def __init__(self, debugname=""):
      """ Constructor. If a debug name is assigned this will be stored as a
      debugname attribute.
      """
      super(postoffice, self).__init__()
      if debugname:
         self.debugname = debugname + ":debug "
      else:
         self.debugname =""
      self.linkages = list()


   def __str__(self):
      """Provides a string representation of a postoffice, designed for debugging"""
      result = "{{ POSTOFFICE: " + self.debugname
      result = result + "links " + self.linkages.__str__() + " }}"
      return result

   def link(self, source, sink, *optionalargs, **kwoptionalargs):
       """\
       link((component,boxname),(component,boxname),**otherargs) -> new linkage
       
       Creates a linkage from a named box on one component to a named box on
       another. See linkage class for meanings of other arguments. A linkage
       object is returned as a handle representing the linkage created.
       
       The linkage is registered with this postoffice.
       
       Throws Axon.AxonExceptions.BoxAlreadyLinkedToDestination if the source
       is already linked to somewhere else (Axon does not permit one-to-many).
       """
       (sourcecomp, sourcebox) = source
       (sinkcomp, sinkbox) = sink
       thelink = linkage(sourcecomp,sinkcomp,sourcebox,sinkbox,*optionalargs,**kwoptionalargs)
       try:
           thelink.getSinkbox().addsource( thelink.getSourcebox() )
       except BoxAlreadyLinkedToDestination, e:
           raise e
       self.linkages.append(thelink)
       return thelink

   def unlink(self, thecomponent=None, thelinkage=None):
        """\
        unlink([thecomponent][,thelinkage] -> destroys linkage(s).
        
        Destroys the specified linkage, or linkages for the specified component.
        
        Note, it only destroys linkages registered in this postoffice.
        """
        if thelinkage:
            try:
                self.linkages.remove(thelinkage)
            except ValueError:
                pass
            else:
                thelinkage.getSinkbox().removesource( thelinkage.getSourcebox() )
        if thecomponent:
            i=0
            num =len(self.linkages)
            while i<num:
                linkage = self.linkages[i]
                if linkage.source == thecomponent or linkage.sink == thecomponent:
                    num=num-1
                    self.unlink(thelinkage=linkage)
                else:
                    i=i+1

   def unlinkAll(self):
       """\
       Destroys all linkages made with this postoffice.
       """
       num =len(self.linkages)
       while num > 0:
           linkage = self.linkages[0]
           num=num-1
           self.unlink(thelinkage=linkage)


   def deregisterlinkage(self, thecomponent=None,thelinkage=None):
       """Stub for legacy"""
       noisy_deprecation_warning = "Use Postoffice.unlink() method instead. Or if writing components, use component.unlink() in preference Component: " + str(thecomponent) + " Linkage: "+ str(thelinkage)
       # raise DeprecationWarning(noisy_deprecation_warning)
       print noisy_deprecation_warning
       return self.unlink(thecomponent,thelinkage)



   def islinkageregistered(self, linkage):
      """Returns a true value if the linkage given is registered with the postoffie."""
      return self.linkages.count(linkage)



if __name__ == '__main__':
   pass

# RELEASE: MH, MPS
