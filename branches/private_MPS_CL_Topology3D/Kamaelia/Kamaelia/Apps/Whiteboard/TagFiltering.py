#!/usr/bin/env python
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
#

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline

# A pair of components for tagging data with a unique ID and filtering out
# data with a given unique ID
#
# A third component that combines the two, wrapping another component,
# tagging all outbound data, and filtering out any data with the same uid that
# comes back.

class UidTagger(component):
    Inboxes = { "inbox"   : "incoming items",
                "control" : "shutdown signalling",
              }
    Outboxes = { "outbox" : "items tagged with uid",
                 "signal" : "shutdown signalling",
                 "uid"    : "uid used for tagging, emitted at start",
               }

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        uid = self.name
        self.send(uid, "uid")

        while self.shutdown():
            while self.dataReady("inbox"):
                item = self.recv("inbox")
                self.send( (uid,item), "outbox" )

            self.pause()
            yield 1


class FilterTag(component):
    Inboxes = { "inbox"   : "incoming tagged items",
                "control" : "shutdown signalling",
                 "uid"    : "uid to filter",
              }
    Outboxes = { "outbox" : "items, not tagged with uid",
                 "signal" : "shutdown signalling",
               }

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        uid = object()

        while self.shutdown():
            while self.dataReady("uid"):
                uid = self.recv("uid")

            while self.dataReady("inbox"):
                (ID,item) = self.recv("inbox")
                if not ID == uid:
                    self.send( item, "outbox" )

            self.pause()
            yield 1


class FilterButKeepTag(component):
    Inboxes = { "inbox"   : "incoming tagged items",
                "control" : "shutdown signalling",
                 "uid"    : "uid to filter",
              }
    Outboxes = { "outbox" : "items, not tagged with uid",
                 "signal" : "shutdown signalling",
               }

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        uid = object()

        while self.shutdown():
            while self.dataReady("uid"):
                uid = self.recv("uid")

            while self.dataReady("inbox"):
                (ID,item) = self.recv("inbox")
                if not ID == uid:
                    self.send( (ID,item), "outbox" )

            self.pause()
            yield 1


def TagAndFilterWrapper(target, dontRemoveTag=False):
    """\
    Returns a component that wraps a target component, tagging all traffic
    coming from its outbox; and filtering outany traffic coming into its inbox
    with the same unique id.
    """
    if dontRemoveTag:
        Filter = FilterButKeepTag
    else:
        Filter = FilterTag

    return Graphline( TAGGER = UidTagger(),
                      FILTER = Filter(),
                      TARGET = target,
                      linkages = {
                          ("TARGET", "outbox") : ("TAGGER", "inbox"),    # tag data coming from target
                          ("TAGGER", "outbox") : ("self", "outbox"),

                          ("TAGGER", "uid")    : ("FILTER", "uid"),      # ensure filter uses right uid

                          ("self", "inbox")    : ("FILTER", "inbox"),    # filter data going to target
                          ("FILTER", "outbox") : ("TARGET", "inbox"),

                          ("self", "control")  : ("TARGET", "control"),  # shutdown signalling path
                          ("TARGET", "signal") : ("TAGGER", "control"),
                          ("TAGGER", "signal") : ("FILTER", "control"),
                          ("FILTER", "signal") : ("self", "signal"),
                      },
                    )

def FilterAndTagWrapper(target, dontRemoveTag=False):
    """\
    Returns a component that wraps a target component, tagging all traffic
    going into its inbox; and filtering outany traffic coming out of its outbox
    with the same unique id.
    """
    if dontRemoveTag:
        Filter = FilterButKeepTag
    else:
        Filter = FilterTag

    return Graphline( TAGGER = UidTagger(),
                      FILTER = Filter(),
                      TARGET = target,
                      linkages = {
                          ("TARGET", "outbox") : ("FILTER", "inbox"),    # filter data coming from target
                          ("FILTER", "outbox") : ("self", "outbox"),

                          ("TAGGER", "uid")    : ("FILTER", "uid"),      # ensure filter uses right uid

                          ("self", "inbox")    : ("TAGGER", "inbox"),    # tag data going to target
                          ("TAGGER", "outbox") : ("TARGET", "inbox"),

                          ("self", "control")  : ("TARGET", "control"),  # shutdown signalling path
                          ("TARGET", "signal") : ("TAGGER", "control"),
                          ("TAGGER", "signal") : ("FILTER", "control"),
                          ("FILTER", "signal") : ("self", "signal"),
                      },
                    )

def TagAndFilterWrapperKeepingTag(target):
    return TagAndFilterWrapper(target, dontRemoveTag=True)

def FilterAndTagWrapperKeepingTag(target):
    return FilterAndTagWrapper(target, dontRemoveTag=True)
