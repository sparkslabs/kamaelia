#!/usr/bin/python

import pprint
class ConcurrentUpdate(Exception): pass

class STM(object):
    debugging = False
    def __init__(self, **argd):
        super(STM, self).__init__(**argd)
        self.dbm = {}

    def __repr__(self):
        return pprint.pformat(self.dbm)

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

class Var_STM(object):
    debugging = False
    def __init__(self, **argd):
        super(Var_STM, self).__init__(**argd)
        self.dbm = {}

    def __repr__(self):
        return pprint.pformat(self.dbm)

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
        (value, version) = self.dbm[key]
        V = Var(key, value, version, self)
        return V

    def new(self, key, value):
        try:
            V = self.get(key)
            raise "Grrr"
        except KeyError:
            version = self.store(key, value, 0)
            V = Var(key, value, version, self)
            return V

class Var(object):
    def __init__(self, key, value, version, source):
        self.name = key
        self.value = value
        self.version = version
        self.source = source
    def isfresh(self):
        V = self.source.get(self.name)
        return V.version != self.version
    def __repr__(self):
        if self.isfresh():
            extra = " (stale)"
        else:
            extra = ""
        return repr(self.value) + extra
    def ints(self):
        return "(%s,%s,%s,%s)" % (str(self.name), str(self.value), str(self.version), str(self.source.__class__))
    def set(self, value):
        version = self.source.store(self.name, value, self.version)
        self.value= value
        self.version = version

    def update(self, func):
        while 1:
            try:
                newvalue = func(self.value)
                self.set(newvalue)
                break
            except ConcurrentUpdate:
                V = self.source.get(self.name)
                self.value = V.value
                self.version = V.version

Y = Var_STM()
x = Y.new("x", 5)
y = Y.get("x")
x.set(x.value+5)
x.set(x.value+5)

print
print "y:", y, "x:", x
print "y(full)", y.ints()
print "x(full)", x.ints()
print Y

y.update(lambda x: x+5)
print
print "y:", y, "x:", x
print "y(full)", y.ints()
print "x(full)", x.ints()
print Y

y.update(lambda x: x+5)
print
print "y:", y, "x:", x
print "y(full)", y.ints()
print "x(full)", x.ints()
print Y

