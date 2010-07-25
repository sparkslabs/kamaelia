#! /usr/bin/env python
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

import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Scheduler import scheduler

class ThreadedTest(threadedcomponent):
    def __init__(self):
        super(ThreadedTest, self).__init__()
        self.last = time.time()

    def main(self):
        while 1:
            t = time.time()
            print t - self.last
            self.last = t
            time.sleep(0.0005)


if __name__ == "__main__":
    ThreadedTest().run()


