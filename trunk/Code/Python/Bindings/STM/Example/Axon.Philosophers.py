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

import time
import Axon
from Axon.STM import Store
import random

def all(aList, value):
    for i in aList:
        if value != i:
            return False
    return True
    
class Philosopher(Axon.ThreadedComponent.threadedcomponent):
    forks = ["fork.1", "fork.2"] # default for testing :-)
    def getforks(self):
        gotforks = False
        while not gotforks:
            try:
                X = self.store.using(*self.forks)
                if all([ X[fork].value for fork in self.forks], None):
                    for fork in self.forks:
                        X[fork].value = self.name
                    X.commit()
                    gotforks = True
                else:
                    time.sleep(random.random())
            except Axon.STM.ConcurrentUpdate:
                time.sleep(random.random())
            except Axon.STM.BusyRetry:
                time.sleep(random.random())
        print "Got forks!", self.name, self.forks
        return X

    def releaseforks(self,X):
        print "releasing forks", self.name
        for fork in self.forks:
            X[fork].value = None
        X.commit()

    def main(self):
        while 1:
            X = self.getforks()
            time.sleep(0.2)
            self.releaseforks(X)
            time.sleep(0.3+random.random())

S = Store()
N = 5
for i in range(1,N):
    Philosopher(store=S,forks=["fork.%d" % i ,"fork.%d" % (i+1)]).activate()

Philosopher(store=S,forks=["fork.%d" % N ,"fork.%d" % 1]).run()
