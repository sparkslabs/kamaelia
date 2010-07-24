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

import shelve

class ConcurrentUpdate(Exception): pass

class STM(object):
    debugging = False
    def __init__(self, filename, **argd):
        super(STM, self).__init__(**argd)
        self.filename = filename
#        self.dbm = shelve.open(filename, "c")
        self.dbm = {}

    def zap(self):
        for k in self.dbm.keys():
            del self.dbm[k]

    def store(self, key, value, version=0):
        try:
           (oldvalue, oldversion) = self.dbm[key]
           if self.debugging: print "Already here...", oldvalue, oldversion
           if oldversion == version:
               if self.debugging: print "OK, no updates since you"
               version = version +1
               self.dbm[key] = [value, version]
               if self.debugging: print "added..."
               return version
           else:
               raise ConcurrentUpdate(oldvalue, oldversion)
           
        except KeyError:
          version = 1
          self.dbm[key] = [value, version]
          if self.debugging: print "added..."
          return version
    
    def get(self, key):
        return self.dbm[key]

#
# A *little* kludgey, but look at ClientOne/Rest for how this is used which is quite nice.
#
VALUE = 0
VERSION = 1

class STM_User(object):
    def __init__(self, stm):
        super(STM_User, self).__init__()
        self.stm = stm
        self.local = {}
    def update(self, key, action,*args):
        success = False
        while not success:
            try:
                self.local[key][VALUE] = action(self.local[key][VALUE], *args); yield 1
                self.local[key][VERSION] = self.stm.store(key, self.local[key][VALUE], self.local[key][VERSION]) ; yield 1
                success = True
            except ConcurrentUpdate, e:
                self.local[key] = [e[0],e[1]]
    def retrieve(self, key):
        self.local[key] = X.get(key);
        return self.local[key][0]

    def store(self, key, value):
        try:
            version = self.local[key][VERSION]
        except KeyError:
            self.local[key] = [ 0,0]
            version = 0
        self.local[key][VERSION] = self.stm.store(key, value, version)
        self.local[key][VALUE] = value

    def main(self):
        yield 1

class ClientOne(STM_User):
    def main(self):
        self.store("Balance", 0)
        print "STARTING",self.retrieve("Balance") ;  yield 1
        for i in self.update("Balance", lambda x: x+10): yield 1
        for i in self.update("Balance", lambda x: x+20): yield 1
        for i in self.update("Balance", lambda x: x+30): yield 1

class ClientRest(STM_User):
    def main(self):
        print "STARTING",self.retrieve("Balance") ;  yield 1
        for i in self.update("Balance", lambda x: x+10): yield 1
        for i in self.update("Balance", lambda x: x+20): yield 1
        for i in self.update("Balance", lambda x: x+30): yield 1

X = STM("mystate",zap=True)
X.zap()

L = [ [ ClientOne(X).main() ], [ ClientRest(X).main() ], [ ClientRest(X).main() ]]
NL = []
while len(L)>0:
    for G in L:
        try:
            G[0].next()
            NL.append(G)
        except StopIteration:
            pass
    L = NL
    NL = []

balance,version = X.get("Balance")
print "BALANCE", balance
