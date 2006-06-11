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
"""Kamaelia Concurrency Component Framework.

POSTOFFICE

A post office creates and destroys linkages and looks after them for the duration
of their existence. It hands out linkage objects that can be used as handles
to layer deregister (remove) the linkage.


"""
import time

from util import removeAll
from idGen import strId, numId
from debug import debug
from AxonExceptions import AxonException
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
      "Provides a string representation of a postoffice, designed for debugging"
      result = "{{ POSTOFFICE: " + self.debugname
      result = result + "links " + self.linkages.__str__() + " }}"
      return result

   def link(self, source, sink, **optionalargs):
       (sourcecomp, sourcebox) = source
       (sinkcomp, sinkbox) = sink
       thelink = linkage(sourcecomp,sinkcomp,sourcebox,sinkbox,**optionalargs)
       self.linkages.append(thelink)
       thelink.getSinkbox().addsource( thelink.getSourcebox() )
       return thelink

   def unlink(self, thecomponent=None, thelinkage=None):
        """\
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
