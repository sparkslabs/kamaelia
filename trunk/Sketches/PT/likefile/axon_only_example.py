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

import time, sys, Axon
from Axon.likefile import LikeFile, schedulerThread

schedulerThread().start()


class Reverser(Axon.Component.component):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox') # strings have no "reverse" method, hence this indexing 'hack'.
            else: self.pause()
            yield 1


# Unix's "rev" tool, implemented using likefile.

reverser = LikeFile(Reverser())

while True:
    line = sys.stdin.readline().rstrip() # get rid of the newline
    reverser.put(line)
    enil = reverser.get()
    print enil