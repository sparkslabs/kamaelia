#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===================================
Simple framework for filtering data
===================================

A framework for filtering a stream of data. Write an object providing a
filter(...) method and plug it into a Filter component.



Example Usage
-------------
Filters any non-strings from a stream of data::
    
    class StringFilter(object):
        def filter(self, input):
            if type(input) == type(""):
                return input
            else:
                return None            # indicates nothing to be output

    myfilter = Filter(filter = StringFilter).activate()
    


How does it work?
-----------------

Initialize a Filter component, providing an object with a filter(...)
method.

The method should take a single argument - the data to be filtered. It should
return the result of the filtering/processing. If that result is None then
the component outputs nothing, otherwise it outputs whatever the value is that
was returned.

Data received on the component's "inbox" inbox is passed to the filter(...)
method of the object you provided. The result is output on the "outbox" outbox.

If a producerFinished message is received on the "control" inbox then it is sent
on out of the "signal" outbox. The component will then terminate.

However, before terminating it will repeatedly call your object's filter(...)
method, passing it an empty string ("") until the result returned is None.
If not None, then whatever value the filter(...) method returned is output. This
is to give your object a chance to flush any data it may have been buffering.

Irrespective of whether your filtering object buffers any data from one call to
the next, you must ensure that (eventually) calling it with an empty string ("")
will result in None being returned.

"""


from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

class NullFilter(object):
   """A filter class that filters nothing.  This is the null default for the Filter."""
   def filter(self, newtext):
      return newtext
      
class Filter(component):
   """\
   Filter([filter]) -> new Filter component.

   Component that can modify and filter data passing through it. Plug your own
   'filter' into it.
   
   Keyword arguments:
   
   - filter  -- an object implementing a filter(data) method (default=NullFilter instance)
   """

   Inboxes  = { "inbox"   : "Data to be filtered",
                "control" : "Shutdown signalling",
              }
   Outboxes = { "outbox" : "Filtered data",
                "signal" : "Shutdown signalling",
              }
       
   def __init__(self, filter = NullFilter()):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Filter, self).__init__()
      self.filter = filter
      
   def mainBody(self):
      """Main loop body."""
      if self.dataReady():
         mes = self.recv()
         outmes = self.filter.filter(mes)
         if outmes is not None:
            self.send(outmes)
      if self.dataReady("control"):
         mes = self.recv("control")
         if isinstance(mes, producerFinished):
            self.send(mes, "signal")
            return 0
      return 1
            
   def closeDownComponent(self):
      """Flush any data remaining in the filter before shutting down."""
      while 1:
        outmes = self.filter.filter("")
        if outmes is None:
            break
        self.send(outmes)

import Kamaelia.Support.Deprecate as Deprecate

FilterComponent = Deprecate.makeClassStub(
    Filter,
    "Use Kamaelia.Util.Filter:Filter instead of Kamaelia.Util.Filter:FilterComponent",
    "WARN"
    )

__kamaelia_components__  = ( Filter, )

