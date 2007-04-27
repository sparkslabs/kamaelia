#!/usr/bin/env python

class ipc(object):
    pass

class shutdown(ipc):
    pass

class shutdownMicroprocess(shutdown):

    def __new__(cls):
        if cls != shutdownNow and shutdownNow not in cls.__bases__:
            print "*** tsk tsk, creating a shutdownMicroprocess!!"
        return shutdown.__new__(shutdownNow)


class shutdownNow(shutdownMicroprocess):
    pass


class basedOnShutdownMicroprocess(shutdownMicroprocess):
    pass


print "What is a shutdownNow?"
s=shutdownNow()
print type(s)
print
print isinstance(s,shutdownNow)
print isinstance(s,shutdownMicroprocess)
print isinstance(s,shutdown)
print

print "What is a shutdownMicroprocess"
s=shutdownMicroprocess()
print type(s)
print
print isinstance(s,shutdownNow)
print isinstance(s,shutdownMicroprocess)
print isinstance(s,shutdown)

print "What is a shutdownNow?"
s=basedOnShutdownMicroprocess()
print type(s)
print
print isinstance(s,shutdownNow)
print isinstance(s,shutdownMicroprocess)
print isinstance(s,shutdown)
print

