#!/usr/bin/env python
#
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

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg, "signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False

    def main(self):
        uid = self.name
        self.send(uid, "uid")

        while not self.finished():
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

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg, "signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False

    def main(self):
        uid = object()

        while not self.finished():
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

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg, "signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False

    def main(self):
        uid = object()

        while not self.finished():
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
