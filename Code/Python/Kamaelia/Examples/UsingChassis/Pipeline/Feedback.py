#!/usr/bin/python
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

# Checked: 2024/03/24

import random
import time
import Axon
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

class LSystem(Axon.ThreadedComponent.threadedcomponent):
    """A simple L system modeller. Allows replacement of the model for the purposes of handling feedback"""
    rules = {
        "B" : "BTL",
        "L" : "B",
    }
    def mutateModel(self, model):
        newmodel = ""
        for atom in model:
            try:
                replacement = self.rules[atom]
                newmodel += replacement
            except KeyError:
                newmodel += atom
        return newmodel
        
    def main(self):
        model = "B"
        while not self.dataReady("control"):
            self.send( model, "outbox")
            for i in self.Inbox("inbox"):
                model = i
            model = self.mutateModel(model)
            time.sleep(0.4)
        self.send(self.recv("control"), "signal")
        
class Damage(Axon.Component.component):
    """Simple L-System damager"""
    def damageModel(self, model):
        newmodel = ""
        dratio = 0
        if len(model)<10: dratio = 0
        if len(model)>60: dratio = 50
        for atom in model:
            if random.randint(0,100) > dratio:
                newmodel += atom
        return newmodel
        
    def main(self):
        while not self.dataReady("control"):
            for model in self.Inbox("inbox"):
                model = self.damageModel(model)
                self.send( model , "outbox")
            yield 1
        self.send(self.recv("control"), "signal")

Pipeline(
    LSystem(),
    ConsoleEchoer(tag="\n", forwarder=True), # Would be nice to be a renderer
    Damage(),
    
    circular = True,
).run()

