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

import pypm
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Button import Button

class MidiTest(Axon.Component.component):
    def __init__(self, port_number):
        super(MidiTest, self).__init__()
        pypm.Initialize()
        self.output = pypm.Output(port_number, 0)

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                #Note on (with note num from inbox) if we get data
                self.output.WriteShort(0x90, self.recv("inbox"), 127)
            yield 1

if __name__ == "__main__":
    Graphline(bd = Button(caption="BD", msg=36, position=(0, 0)),
              sd = Button(caption="SD", msg=38, position = (50, 0)),
              hh = Button(caption="HH", msg=46, position = (100, 0)),
              midi_out = MidiTest(0),
              linkages = {
                  ("bd", "outbox") : ("midi_out", "inbox"),
                  ("hh", "outbox") : ("midi_out", "inbox"),
                  ("sd", "outbox") : ("midi_out", "inbox"),
              }
    ).run()