#!/usr/bin/python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
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
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""
General utility functions & common includes
"""

#import sets
from AxonExceptions import invalidComponentInterface


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
   """Returns True if requiredList is a subset of suppliedList, False otherwise.
   Efficient for short required lists but copying and sorting both lists first
   may be better if required list is long."""
   for item in requiredList:
      if not item in suppliedList:
         return False
   return True

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
   
