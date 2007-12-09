#!/usr/bin/python
#
# (C) 2007 Kamaelia Contributors(1) All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
#
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

import copy
import threading

class ConcurrentUpdate(Exception): pass
class BusyRetry(Exception): pass

class Value(object):
    def __init__(self, version, value,store,key):
        self.version = version
        self.value = value
        self.store = store
        self.key = key

    def __repr__(self):
        return "Value"+repr((self.version,self.value))

    def set(self, value):
        self.value = value

    def commit(self):
        self.store.set(self.key, self)

    def clone(self):
        return Value(self.version, copy.deepcopy(self.value),self.store,self.key)

class Store(object):
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def get(self, key):
        return self.store[key].clone()

    def set(self, key, value):
        success = False
        if self.lock.acquire(0):
            try:
                if not (self.store[key].version > value.version):
                    self.store[key] = Value(value.version+1, copy.deepcopy(value.value), self, key)
                    value.version= value.version+1
                    success = True
            finally:
                self.lock.release()
        else:
            raise BusyRetry

        if not success:
            raise ConcurrentUpdate

    def using(self, key):
        try:
            return self.get(key)
        except KeyError:
            if self.lock.acquire(0):
                try:
                    self.store[key] = Value(0, None,self,key)
                finally:
                    self.lock.release()
            else:
                raise BusyRetry

            return self.get(key) # Yes, this can still fail, this is still perhaps non-ideal - should probably
                                 # have a flag to allow retrying a few times first.

    def dump(self):
        for k in self.store:
            print k, ":", self.store[k]


S = Store()
D = S.using("accounts")
D.set({"account_one":50, "account_two":100, "myaccount":0})
D.commit() # First
S.dump()
X = D.value
X["myaccount"] = X["account_one"] + X["account_two"]
X["account_one"] = 0

E = S.using("accounts")
Y = E.value
Y["myaccount"] = Y["myaccount"]-100
Y["account_one"]= 100
E.set(Y)
E.commit() # Second
S.dump()

X["account_two"] = 0
D.set(X)
D.commit()  # Third
S.dump()
print "Committed", D.value["myaccount"]

if 0:
    S = Store()
    greeting = S.using("hello")
    print repr(greeting.value)
    greeting.set("Hello World")
    greeting.commit()
    # ------------------------------------------------------
    print greeting
    S.dump()
    # ------------------------------------------------------
    par = S.using("hello")
    par.set("Woo")
    par.commit()
    # ------------------------------------------------------
    print greeting
    S.dump()
    # ------------------------------------------------------
    greeting.set("Woo")
    greeting.commit()
    print repr(greeting), repr(greeting.value)
    S.dump()
