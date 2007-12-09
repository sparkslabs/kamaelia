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

class Collection(dict):
    def set_store(self,store):
        self.store = store
    def commit(self):
        self.store.set_values(self)


class Store(object):
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def get(self, key):
        return self.store[key].clone()

    def set_values(self, D):
        Fail = False
        if self.lock.acquire(0):
            try:
                for key in D:
                    value = D[key]
                    if not (self.store[key].version > value.version):
                        self.store[key] = Value(value.version+1, copy.deepcopy(value.value), self, key)
                        value.version= value.version+1
                    else:
                        Fail = True
                        break
            finally:
                self.lock.release()
        else:
            raise BusyRetry

        if Fail:
            raise ConcurrentUpdate

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

    def using(self, *keys):
        D = Collection()
        new = []

        # Grab the values that already exist
        for key in keys:
            if key in self.store:
                D[key] = self.store[key].clone()
            else:
                new.append(key)

        # Now add in the values that don't already exist
        if self.lock.acquire(0):
            try:
                for key in new:
                    self.store[key] = Value(0, None,self,key)
                    D[key] = self.store[key].clone()
            finally:
                self.lock.release()
        else:
            raise BusyRetry
        D.set_store(self)
        return D

    def usevar(self, key):
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

            return self.get(key)


    def dump(self):
        print "DEBUG: Store dump ------------------------------"
        for k in self.store:
            print "     ",k, ":", self.store[k]
        print


if 1:
    S = Store()
    D = S.using("account_one", "account_two", "myaccount")
    D["myaccount"].set(0)
    D["account_one"].set(50)
    D["account_two"].set(100)
    D.commit() # 1
    S.dump()

    D = S.using("account_one", "account_two", "myaccount")
    D["myaccount"].set(D["account_one"].value+D["account_two"].value)
    E = S.using("account_one", "myaccount")
    E["myaccount"].set(E["myaccount"].value-100)
    E["account_one"].set(100)
    E.commit() # 2
    D["account_one"].set(0)
    D["account_two"].set(0)
    D.commit() # 3 - should fail
    S.dump()

if 0:
    S = Store()
    D = S.using("account_one", "account_two", "myaccount")
    D["account_one"].set(50)
    D["account_two"].set(100)
    D.commit()
    S.dump()

    D = S.using("account_one", "account_two", "myaccount")
    D["myaccount"].set(D["account_one"].value+D["account_two"].value)
    D["account_one"].set(0)
    D["account_two"].set(0)
    D.commit()
    S.dump()


if 0:
    S = Store()
    D = S.usevar("accounts")
    D.set({"account_one":50, "account_two":100, "myaccount":0})
    D.commit() # First
    S.dump()
    X = D.value
    X["myaccount"] = X["account_one"] + X["account_two"]
    X["account_one"] = 0

    E = S.usevar("accounts")
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
    greeting = S.usevar("hello")
    print repr(greeting.value)
    greeting.set("Hello World")
    greeting.commit()
    # ------------------------------------------------------
    print greeting
    S.dump()
    # ------------------------------------------------------
    par = S.usevar("hello")
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
