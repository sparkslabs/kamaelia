#!/usr/bin/python
# -*- coding: utf-8 -*-
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

