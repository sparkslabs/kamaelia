#!/usr/bin/python
"""
General utility functions & common includes
"""

from AxonExceptions import invalidComponentInterface
import sets

#"""This sets the system into production moe which means that many exception could be suppressed to allow the system to keep running.  Test all code with this set to false so that you are alerted to errors"""
production=False

def logError(someException, *args):
    "Currently does nothing but can be rewritten to log ignored errors if the production value is true."
    pass

def axonRaise(someException,*args):
    if production:
        logError(someException, *args)
        return False
    else:
        raise someException(*args)

def removeAll(xs, y):
   """ Very simplistic method of removing all occurances of y in list xs.
   """
   try:
      while 1:
         del xs[xs.index(y)]
   except ValueError, reason:
      if not reason.__str__() == "list.index(x): x not in list":
         raise ValueError, reason

def listSubset(requiredList, suppliedList):
   return sets.Set(requiredList).issubset(sets.Set(suppliedList))

def testInterface(theComponent, interface):
   "Look for a minimal match interface for the component"
   (requiredInboxes,requiredOutboxes) = interface
   if not listSubset(requiredInboxes, theComponent.Inboxes):
      return axonRaise(invalidComponentInterface, "inboxes", theComponent, interface)
   if not listSubset(requiredOutboxes, theComponent.Outboxes):
      return axonRaise(invalidComponentInterface,"outboxes", theComponent, interface)
   return True

def safeList(arg=None):
   try:
      return list(arg)
   except TypeError:
      return []

class Finality(Exception):
   """Used for implementing try...finally... inside a generator
   """
   pass
   
