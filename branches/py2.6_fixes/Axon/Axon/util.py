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
"""\
===========================================
General utility functions & common includes
===========================================

"""

import sys
from AxonExceptions import invalidComponentInterface
if sys.version_info[1] <= 4:
    from sets import set

#"""This sets the system into production moe which means that many exception could be suppressed to allow the system to keep running.  Test all code with this set to false so that you are alerted to errors"""
production=False

def logError(someException, *args):
    """\
    Currently does nothing but can be rewritten to log ignored errors if the
    production value is true.
    """
    pass

def axonRaise(someException,*args):
    """\
    Raises the supplied exception with the supplied arguments *if*
    Axon.util.production is set to True.
    """
    if production:
        logError(someException, *args)
        return False
    else:
        raise someException(*args)

def removeAll(xs, y):
   """Very simplistic method of removing all occurances of y in list xs."""
   try:
      while 1:
         del xs[xs.index(y)]
   except ValueError, reason:
      if not reason.__str__() == "list.index(x): x not in list":
         raise ValueError, reason

def listSubset(requiredList, suppliedList):
   """Returns true if the requiredList is a subset of the suppliedList."""
   return set(requiredList).issubset(set(suppliedList))

def testInterface(theComponent, interface):
   """Look for a minimal match interface for the component.
   The interface should be a tuple of lists, i.e. ([inboxes],[outboxes])."""
   (requiredInboxes,requiredOutboxes) = interface
   if not listSubset(requiredInboxes, theComponent.Inboxes):
      return axonRaise(invalidComponentInterface, "inboxes", theComponent, interface)
   if not listSubset(requiredOutboxes, theComponent.Outboxes):
      return axonRaise(invalidComponentInterface,"outboxes", theComponent, interface)
   return True

def safeList(arg=None):
   """Returns the list version of arg, otherwise returns an empty list."""
   try:
      return list(arg)
   except TypeError:
      return []

class Finality(Exception):
   """Used for implementing try...finally... inside a generator."""
   pass
   
if __name__ == '__main__':
    print 'listSubset([1,2,3,4], [2,3,4,5]) = %s' % (listSubset([1,2,3,4], [2,3,4,5]))
    print 'listSubset([1,2,3,4], [2,3]) = %s' % (listSubset([2,3], [1,2,3,4]))