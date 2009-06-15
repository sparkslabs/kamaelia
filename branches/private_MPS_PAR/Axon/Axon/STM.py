#!/usr/bin/python
#
# Copyright (C) 2007 Kamaelia Contributors(1) All Rights Reserved.
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

"""
===
STM
===

Support for basic in-process software transactional memory.



What IS it?
-----------

Software Transactional Memory (STM) is a technique for allowing multiple
threads to share data in such a way that they know when something has gone
wrong. It's been used in databases (just called transactions there really) for
some time and is also very similar to version control. Indeed, you can think of
STM as being like variable level version control.



Why is it useful?
-----------------

Why do you need it? Well, in normal code, Global variables are generally
shunned because it can make your code a pain to work with and a pain to be
certain if it works properly. Even with linear code, you can have 2 bits of
code manipulating a structure in surprising ways - but the results are
repeatable. Not-properly-managed-shared-data is to threaded systems as
not-properly-managed-globals are to normal code. (This code is one way of
helping manage shared data)

Well, with code where you have multiple threads active, having shared data is
like an even nastier version of globals. Why? Well, when you have 2 (or more)
running in parallel, the results of breakage can become hard to repeat as two
pieces of code "race" to update values.

With STM you make it explicit what the values are you want to update, and only
once you're happy with the updates do you publish them back to the shared
storage. The neat thing is, if someone else changed things since you last
looked, you get told (your commit fails), and you have to redo the work. This
may sound like extra work (you have to be prepared to redo the work), but it's
nicer than your code breaking :-)

The way you get that message is the .commit raises a ConcurrentUpdate
exception.

Also, it's designed to work happily in code that requires non-blocking usage -
which means you may also get a BusyRetry exception under load. If you do, you
should as the exception suggests retry the action that you just tried. (With or
without restarting the transaction)

Apologies if that sounds too noddy :)



Using It
--------

Accessing/Updating a single shared value in the store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can have many single vars in a store of course... If they're related though
or updated as a group, see the next section::

    from Axon.STM import Store

    S = Store()
    greeting = S.usevar("hello")
    print repr(greeting.value)
    greeting.set("Hello World")
    greeting.commit()



Accessing/Updating a collection of shared values in the store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Likewise you can use as many collections of values from the store as you like::

    from Axon.STM import Store

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



What can (possibly) go wrong?
-----------------------------

You can have 2 people trying to update the same values at once. An example of
this would be - suppose you have the following commands being executed by 2
threads with this mix of commands::

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

You do actually want this to fail because you have concurrent updates. This
will fail on the third commit, and fail by throwing a ConcurrentUpdate
exception. If you get this, you should redo the transaction.

The other is where there's lots of updates happening at once. Rather than the
code waiting until it acquires a lock, it is possible for either the .using,
.usevar or .commit methods to fail with a BusyRetry exception. This means
exactly what it says on the tin - the system was busy & you need to retry. In
this case you do not have to redo the transaction. This is hard to replicate
except under load. The reason we do this however is because most Kamaelia
components are implemented as generators, which makes blocking operation ( as a
.acquire() rather than .acquire(0) would be) an expensive operation.
"""

import copy
import threading

class ConcurrentUpdate(Exception): pass
class BusyRetry(Exception): pass

class Value(object):
    """
    Value(version, value, store, key) -> new Value object

    A simple versioned key-value pair which belongs to a thread-safe store

    Arguments:
    
    - version -- the initial version of the value
    - value -- the object's initial value
    - store -- a Store object to hold the value and it's history
    - key -- a key to refer to the value
    
    Note: You do not instantiate these - the Store does that
    """
    def __init__(self, version, value,store,key):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        self.version = version
        self.value = value
        self.store = store
        self.key = key

    def __repr__(self):
        return "Value"+repr((self.version,self.value))

    def set(self, value):
        """ Set the value without storing """
        self.value = value

    def commit(self):
        """ Commit a new version of the value to the store """
        self.store.set(self.key, self)

    def clone(self):
        """ Returns a clone of the value """
        return Value(self.version, copy.deepcopy(self.value),self.store,self.key)

class Collection(dict):
    """
    Collection() -> new Collection dict

    A dictionary which belongs to a thread-safe store
    
    Again, you do not instantiate these yourself
    """
    def set_store(self,store):
        """ Set the store to associate the collection with """
        self.store = store

    def commit(self):
        """ Commit new versions of the collection's items to the store """
        self.store.set_values(self)


class Store(object):
    """
    Store() -> new Store object

    A thread-safe versioning store for key-value pairs
    
    You instantiate this as per the documentation for this module
    """
    def __init__(self):
        self.store = {}                # Threadsafe
        self.lock = threading.Lock()

    # ////---------------------- Direct access -----------------------\\\\
    # Let's make this lock free, and force the assumption that to do this the store must be locked.
    # Let's make this clear by marking these private
    def __get(self, key):                # Reads Store Value - need to protect during clone
        """
        Retreive a value.  Returns a clone of the Value.  Not thread-safe.
        """
        return self.store[key].clone()

    def __make(self, key):               # Writes Store Value - need to prevent multiple concurrent write
        """ Create a new key-value pair.  Not thread-safe """
        self.store[key] = Value(0, None,self,key)

    def __do_update(self, key, value):   # Writes Store Value  - need to prevent multiple concurrent write
        """
        Update a key-value pair and increment the version.  Not thread-safe
        """
        self.store[key] = Value(value.version+1, copy.deepcopy(value.value), self, key)
        value.version= value.version+1

    def __can_update(self,key, value):   # Reads Store Value - possibly thread safe, depending on VM implementation
        """
        Returns true if a value can be safely updated.  Potentially not
        thread-safe
        """
        return not (self.store[key].version > value.version)
    # \\\\---------------------- Direct access -----------------------////



    # ////----------------- Single Value Mediation ------------------\\\\
    # Both of these are read-write
    def usevar(self, key, islocked=False):   # Reads and Writes Values (since value may not exist)
        """
        Tries to get an item from the store.  Returns the requested Value
        object.  If the store is already in use a BusyRetry error is raised.
        """
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
        """
        Tries to update a value in the store.  If the store is already in use
        a BusyRetry error is raised.  If the value has been updated by another
        thread a ConcurrentUpdate error is raised
        """
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
        """
        Tries to get a selection of items from the store.  Returns a Collection
        dictionary containing the requested values.  If the store is already
        in use a BusyRetry error is raised.
        """
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
        """
        Tries to update a selection of values in the store.  If the store is
        already in use a BusyRetry error is raised.  If one of the values has
        been updated by another thread a ConcurrentUpdate error is raised.
        """
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
