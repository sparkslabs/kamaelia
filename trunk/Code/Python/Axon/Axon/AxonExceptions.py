#!/usr/bin/env python2.3

class AxonException(Exception):
   def __init__(self, *args):
      self.args = args

class normalShutdown(AxonException): pass
class invalidComponentInterface(AxonException): pass
class noSpaceInBox(AxonException): pass
class BadParentTracker(AxonException): pass
class ServiceAlreadyExists(AxonException): pass
class BadComponent(AxonException): pass
class BadInbox(AxonException): pass
class MultipleServiceDeletion(AxonException): pass
class NamespaceClash(AxonException): pass
class AccessToUndeclaredTrackedVariable(AxonException): pass
class ArgumentsClash(AxonException): pass
