#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess


class PipeBuild(Axon.Component.component):
    """This component takes messages instructing it to add/remove entities from
    a pipeline, and outputs the messages needed to update a topology viewer, and
    also a full enumeration of the pipeline

    Accepts:
        ("ADD", id_, name, data, afterid)
           Add item to pipeline, with id_, name, and data, immediately after the
           element with id 'afterid'. Or on the end if afterid == None.
        ("DEL", id_)
           Remove item from the pipeline with id_

    Emits:
        Topology msgs:
           ("DEL", "ALL")
           ("ADD", "NODE", ...)
           ("ADD", "LINK", ...)
           ("DEL", "NODE", ...)
           ("DEL", "LINK", ...)

        Pipeline enumeration messages:
           ("PIPELINE", [ <pipeline data items> ])

    """

    def __init__(self):
        super(PipeBuild, self).__init__()
        self.pipeline = []

    def main(self):
        done = False
        self.send( ("DEL", "ALL"), "outbox")
        while not done:
            
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                self.updatePipeline(command)
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")

            if not done:
                self.pause()

            yield 1
        
        
    def updatePipeline(self, cmd):
        if cmd[0] == "ADD":
            self.do_addComponent(id_=cmd[1],name=cmd[2], data=cmd[3], afterid=cmd[4])

        if cmd[0] == "DEL":
            self.do_delComponent(id_=cmd[1])

        self.outputPipeline()
        
    def do_addComponent(self, id_, name, data, afterid=None):
        # send to topology viewer the 'add node' command
        msg = ("ADD","NODE", id_, name, "randompos", "component")
        self.send( msg, "outbox")
        
        # add to the pipeline and wire it in 'after' specified location
        index = len(self.pipeline)
        if afterid != None:
            for c in self.pipeline:
                if c['id'] == afterid:
                    index = self.pipeline.index(c) + 1

        self.pipeline.insert(index, {"id":id_,"data":data} )

        if index < len(self.pipeline)-1:
            # break apart where we're slipping the new one in
            msg = ("DEL","LINK", self.pipeline[index-1]['id'], self.pipeline[index+1]['id'] )
            self.send( msg, "outbox")
            # join new one to next
            msg = ("ADD","LINK", id_, self.pipeline[index+1]['id'] )
            self.send( msg, "outbox")

        if index > 0:
            # join to previous
            msg = ("ADD","LINK", self.pipeline[index-1]['id'], id_ )
            self.send( msg, "outbox")
                    
        

    def do_delComponent(self, id_):
        self.send( ("DEL","NODE", id_), "outbox")
        index = -1
        for c in self.pipeline:
            if c['id'] == id_:
                index = self.pipeline.index(c)

        if index != -1:
            del self.pipeline[index]

            if index > 0 and index < len(self.pipeline):
                msg = ("ADD", "LINK", self.pipeline[index-1]['id'], self.pipeline[index]['id'])
                self.send( msg, "outbox")


    def outputPipeline(self):
        self.send( ("PIPELINE", [c['data'] for c in self.pipeline]), "outbox")
        