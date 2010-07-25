#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
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
# Licensed to the BBC under a Contributor Agreement: PO

import Axon

class Forwarder(Axon.Component.component):
    """
    Forwarder() -> a new Forwarder component
    
    A forwarder component, forwards its inboxes to its outboxes.
    
    The content sent to inbox or secondary-inbox is forwarded to
    outbox, and the content sent to control or secondary-control is
    forwarded to signal.
    
    Example usage
    -------------
    
    plugsplitter = PlugSplitter()
    forwarder    = Forwarder()
    plug         = Plug(plugsplitter,  forwarder)
    plug.activate()
    outsideForwarder = Forwarder()
    plug.link((plug, 'outbox'), (outsideForwarder, 'secondary-inbox'))
    plug.link((plug, 'signal'), (outsideForwarder, 'secondary-control'))
    # outsideForwarder can be used in a linking component (Graphline, 
    # Pipeline, etc.) without any BoxAlreadyLinkedToDestination 
    # problem.
    
    """
    Inboxes = {
            "inbox"             : "Received messages are forwarder to outbox",
            "secondary-inbox"   : "Received messages are forwarder to outbox",
            "control"           : "Received messages are forwarder to signal",
            "secondary-control" : "Received messages are forwarder to signal",
    }
    def __init__(self, **argv):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Forwarder, self).__init__(**argv)

    def main(self):
        while True:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data,"outbox")

            while self.dataReady("secondary-inbox"):
                data = self.recv("secondary-inbox")
                self.send(data,"outbox")

            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data, "signal")
                return

            while self.dataReady("secondary-control"):
                data = self.recv("secondary-control")
                self.send(data, "signal")
                return

            if not self.anyReady():
                self.pause()
            yield 1
