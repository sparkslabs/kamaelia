#!/usr/bin/env python2.3
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
=======================
Convert Data to Strings
=======================

A simple component that takes data items and converts them to strings.



Example Usage
-------------

A simple pipeline::

    Pipeline( sourceOfNonStrings(),
              Stringify(),
              consumerThatWantsStrings(),
            ).activate()
            


How does it work?
-----------------

Send data items to this component's "inbox" inbox. They are converted to
strings using the str(...) function, and sent on out of the "outbox" outbox.

Anything sent to this component's "control" inbox is ignored.

This component does not terminate.
"""

from Axon.Component import component, scheduler

class Stringify(component):
   """\
   Stringify() -> new Stringify.
   
   A component that converts data items received on its "inbox" inbox to
   strings and sends them on out of its "outbox" outbox.
   """
   
   Inboxes = { "inbox"   : "Data items to convert to string",
               "control" : "NOT USED",
             }
   Outboxes = { "outbox" : "Data items converted to strings",
                "signal" : "NOT USED",
              }
              
   def __init__(self):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Stringify, self).__init__() # !!!! Must happen, if this method exists
      self.activate()


   def mainBody(self):
      """Main loop body."""
      if self.dataReady("inbox"):
         theData = self.recv("inbox")
         self.send(str(theData), "outbox")
      return 1

__kamaelia_components__  = ( Stringify, )

