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
        self.store = {}                # Threadsafe
        self.lock = threading.Lock()

    # ////---------------------- Direct access -----------------------\\\\
    # Let's make this lock free, and force the assumption that to do this the store must be locked.
    # Let's make this clear by marking these private
    def __get(self, key):                # Reads Store Value - need to protect during clone
        return self.store[key].clone()

    def __make(self, key):               # Writes Store Value - need to prevent multiple concurrent write
        self.store[key] = Value(0, None,self,key)

    def __do_update(self, key, value):   # Writes Store Value  - need to prevent multiple concurrent write
        self.store[key] = Value(value.version+1, copy.deepcopy(value.value), self, key)
        value.version= value.version+1

    def __can_update(self,key, value):   # Reads Store Value - possibly thread safe, depending on VM implementation
        return not (self.store[key].version > value.version)
    # \\\\---------------------- Direct access -----------------------////



    # ////----------------- Single Value Mediation ------------------\\\\
    # Both of these are read-write
    def usevar(self, key, islocked=False):   # Reads and Writes Values (since value may not exist)
        locked = islocked
        if not locked:
            locked = self.lock.acquire(0)
        result = None
        if locked:
            try:
                try:
                    result = self.__get(key)
                except KeyError:
                    self.__make(key)
                    result = self.__get(key)
            finally:
                if not islocked:
                    self.lock.release() # only release if we acquire
        else:
            raise BusyRetry
        return result


    def set(self, key, value): # Reads and Writes Values (has to check store contents)
        locked = self.lock.acquire(0)
        HasBeenSet = False
        if locked:
            try:
                if self.__can_update(key, value):
                    self.__do_update(key, value)
                    HasBeenSet = True
            finally:
                self.lock.release()
        else:
            raise BusyRetry
        if not HasBeenSet:
            raise ConcurrentUpdate

    # \\\\----------------- Single Value Mediation ------------------////

    # ////----------------- Multi-Value Mediation ------------------\\\\
    # Both of these are read-write
    def using(self, *keys):    # Reads and Writes Values (since values may not exist)
        locked = self.lock.acquire(0)
        if locked:
            try:

                D = Collection()
                for key in keys:
                    D[key] = self.usevar(key,islocked=True)
                D.set_store(self)

            finally:
                self.lock.release()
        else:
            raise BusyRetry

        return D

    def set_values(self, D):  # Reads and Writes Values (has to check store contents)
        CanUpdateAll = True # Hope for the best :-)

        locked = self.lock.acquire(0)
        if locked:
            try:
                for key in D:
                    # Let experience teach us otherwise :-)
                    CanUpdateAll = CanUpdateAll and self.__can_update(key, D[key]) # Reading Store

                if CanUpdateAll:
                    for key in D:
                        self.__do_update(key, D[key]) # Writing Store
            finally:
                self.lock.release()
        else:
            raise BusyRetry

        if not CanUpdateAll:
            raise ConcurrentUpdate
    # \\\\----------------- Multi-Value Mediation ------------------////

    def dump(self):
        # Who cares really? This is a debug :-)
        print "DEBUG: Store dump ------------------------------"
        for k in self.store:
            print "     ",k, ":", self.store[k]
        print

if __name__ == "__main__":
    if 0:
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
        D.commit()  # Third - This Should fail
        S.dump()
        print "Committed", D.value["myaccount"]

    if 1:
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
        greeting.commit() # Should fail
        print repr(greeting), repr(greeting.value)
        S.dump()
