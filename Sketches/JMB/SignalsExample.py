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
from Axon.Ipc import producerFinished

class Killer(component):
    def main(self):
        yield 1
        self.send(producerFinished(self), 'signal')
        yield 1
        
class Killee(component):
    def main(self):
        not_done = True
        while not_done:
            for msg in self.Inbox('control'):
                if isinstance(msg, producerFinished):
                    not_done = False
                    print 'Killee dying!'
                
            if not self.anyReady() and not_done:
                self.pause()
                    
            yield 1
                    
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline(Killer(), Killee()).run()