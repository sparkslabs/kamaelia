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
import inspect
import re

#
# Reuseable IShards
#

def ShutdownHandler(self):
    while self.dataReady("control"):
        cmsg = self.recv("control")
        if isinstance(cmsg, Axon.Ipc.producerFinished) or \
           isinstance(cmsg, Axon.Ipc.shutdownMicroprocess):
            self.send(cmsg, "signal")
            done = True

# not used in MagnaDoodle test case (PygameComponentShard.py)
# (new chassis doesn't inherit from shardable, thus can't getIShard)
def LoopOverPygameEvents(self):
    while self.dataReady("inbox"):
        for event in self.recv("inbox"):
            if event.type == pygame.MOUSEBUTTONDOWN:
                exec self.getIShard("MOUSEBUTTONDOWN")
            elif event.type == pygame.MOUSEBUTTONUP:
                exec self.getIShard("MOUSEBUTTONUP")
            elif event.type == pygame.MOUSEMOTION:
                exec self.getIShard("MOUSEMOTION")

def RequestDisplay(self):
    displayservice = PygameDisplay.getDisplayService()
    self.link((self,"display_signal"), displayservice)
    self.send( self.disprequest, "display_signal")

def GrabDisplay(self):
    self.display = self.recv("callback")
