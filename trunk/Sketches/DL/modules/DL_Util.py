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

# Some Utilities useful for testing purposes

from Kamaelia.Util.Chargen import Chargen
from Axon import Component
import pickle

class SerialChargen(Chargen):
    """ Generates Hello World0, Hello World1, Hello World2, ....."""

    def main(self):
        """Main loop."""
        count = 0
        while 1:
            self.send("Hello World" + str(count), "outbox")
            count += 1
            yield 1
            

class Pickle(Component.component):

    def main(self):

        while 1:

            if self.dataReady("inbox"):

                data = self.recv("inbox")

                self.send(pickle.dumps(data), "outbox")
            yield 1

class UnPickle(Component.component):

    def main(self):

        while 1:

            if self.dataReady("inbox"):

                data = self.recv("inbox")

                self.send(pickle.loads(data), "outbox")
            yield 1


                
