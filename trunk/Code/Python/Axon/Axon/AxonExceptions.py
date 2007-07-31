#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===============
Axon Exceptions
===============

AxonException is the base class for all axon exceptions defined here.

"""

class AxonException(Exception):
   """\
   Base class for axon exceptions.

   Any arguments listed are placed in self.args
   """
   def __init__(self, *args):
      self.args = args

class normalShutdown(AxonException):
    # NOT SURE OF MEANING
    # NOT USED IN AXON
    # NOT USED IN KAMAELIA
    # NOT USED IN SKETCHES
    pass

class invalidComponentInterface(AxonException):
    """\
    Component does not have the required inboxes/outboxes.

    Arguments:

    - *"inboxes"* or *"outboxes"*  - indicating which is at fault
    - the component in question
    - (inboxes,outboxes) listing the expected interface

    Possible causes:

    - Axon.util.testInterface() called with wrong interface/component specified?
    
    """
    pass

class noSpaceInBox(AxonException):
    """\
    Destination inbox is full.

    Possible causes:
    
    - The destination inbox is size limited?
    - It is a threaded component with too small a 'default queue size'?
    """
    pass

class BadParentTracker(AxonException):
    """\
    Parent tracker is bad (not actually a tracker?)

    Possible causes:
    
    - creating a coordinatingassistanttracker specifying a parent that is not
      also a coordinatingassistanttracker?
    """
    pass


class ServiceAlreadyExists(AxonException):
    """\
    A service already exists with the name you specifed.

    Possible causes:
    
    - Two or more components are trying to register services with the
      coordinating assistant tracker using the same name?
    """
    pass

class BadComponent(AxonException):
    """\
    The object provided does not appear to be a proper component.

    Arguments:

    - the 'component' in question
    
    Possible causes:

    - Trying to register a service (component,boxname) with the coordinating
      assistant tracker supplying something that isn't a component?

    """
    pass

class BadInbox(AxonException):
    """\
    The inbox named does not exist or is not a proper inbox.

    Arguments:

    - the 'component' in question
    - the inbox name in question
    
    Possible causes:

    - Trying to register a service (component,boxname) with the coordinating
      assistant tracker supplying something that isn't a component?
    """
    pass

class MultipleServiceDeletion(AxonException):
    """\
    Trying to delete a service that does not exist.

    Possible causes:

    - Trying to delete a service (component,boxname) from the coordinating
      assistant tracker twice or more times?
    """
    pass

class NamespaceClash(AxonException):
    """\
    Clash of names.

    Possible causes:

    - two or more requests made to coordinating assistant tracker to track
      values under a given name (2nd request will clash with first)?
    - should have used updateValue() method to update a value being tracked by
      the coordinating assistant tracker?
    """
class AccessToUndeclaredTrackedVariable(AxonException):
    """\
    Attempt to access a value being tracked by the coordinating assistant
    tracker that isn't actually being tracked yet!

    Arguments:

    - the name of the value that couldn't be accessed
    - the value that it was to be updated with (optional)

    Possible causes:

    - Attempt to update or retrieve a value with a misspelt name?
    - Attempt to update or retrieve a value before it starts being tracked?
    """
    
class ArgumentsClash(AxonException):
    """\
    Supplied arguments clash with each other.

    Possible causes:

    - meaning of arguments misunderstood? not allowed this given combination of
      arguments or values of arguments?
    """
    pass

class BoxAlreadyLinkedToDestination(AxonException):
    """\
    The inbox/outbox already has a linkage going *from* it to a destination.
    
    Arguments:

    - the box that is already linked
    - the box that it is linked to
    - the box you were trying to link it to

    Possible causes:
    
    - Are you trying to make a linkage going from an inbox/outbox to more than
      one destination?
    - perhaps another component has already made a linkage from that
      inbox/outbox?
    """
    pass