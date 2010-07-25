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

from Axon.Component import component
import os

class UniqueId(component):
    Outboxes = ["msgid"]
    def main(self):
        # unique id takes the form X.Y
        # X is the number of times this program has been shutdown/crashed or whatever + 1 (the epoch)
        # Y is the number of message ids given this epoch so far (including that one)
        
        if os.path.isfile("epoch"):
            f = open("epoch", "r")
            epoch = int(f.read())
            f.close()
        else:
            epoch = 0
            
        epoch += 1
        f = open("epoch", "w")
        f.write(str(epoch))
        f.close()
        
        strepoch = str(epoch)
        messagecount = 0
        
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                # msg should be a component instance
                self.link((self, "msgid"), (msg, "msgid"))
    
                messagecount += 1
                self.send(strepoch + "." + str(messagecount), "msgid")
                self.unlink((self, "msgid"), (msg, "msgid"))
            self.pause()
