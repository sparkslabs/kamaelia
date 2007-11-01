#!/usr/bin/python

import shelve

class ConcurrentUpdate(Exception): pass

class STM(object):
    debugging = False
    def __init__(self, filename, **argd):
        super(STM, self).__init__(**argd)
        self.filename = filename
        self.dbm = shelve.open(filename, "c")

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
               self.dbm[key] = (value, version)
               if self.debugging: print "added..."
               return version
           else:
               raise ConcurrentUpdate(oldvalue, oldversion)
           
        except KeyError:
          version = 1
          self.dbm[key] = (value, version)
          if self.debugging: print "added..."
          return version
    
    def get(self, key):
        return self.dbm[key]

        
X = STM("mystate",zap=True)
X.zap()

version = X.store("Balance", 0) # Create version 1
balance,version = X.get("Balance")
print "BALANCE", balance

def clientone(X):
    balance,version = X.get("Balance") ; yield 1

    success = False
    while not success:
        try:
            balance = balance + 10 ; yield 1
            version = X.store("Balance", balance, version) ; yield 1
            success = True
        except ConcurrentUpdate, e:
            balance, version = e

    success = False
    while not success:
        try:
            balance = balance + 20 ; yield 1
            version = X.store("Balance", balance, version) ; yield 1
            success = True
        except ConcurrentUpdate, e:
            balance, version = e

    success = False
    while not success:
        try:
            balance = balance + 30 ; yield 1
            version = X.store("Balance", balance, version) ; yield 1
            success = True
        except ConcurrentUpdate, e:
            balance, version = e


if 1:
    L = [clientone(X), clientone(X),clientone(X),clientone(X)]
    NL = []
    while len(L)>0:
        for G in L:
            try:
                G.next()
                NL.append(G)
            except StopIteration:
                pass
        L = NL
        NL = []

balance,version = X.get("Balance")
print "BALANCE", balance





