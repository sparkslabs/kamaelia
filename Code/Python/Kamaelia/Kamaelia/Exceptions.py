#!/usr/bin/env python2.3
#
# Bunch of Exceptions Specific to Kamaelia.
# This module should be usable using the idiom
#     from KamaeliaExceptions import *
#
# since it takes care to only have publicly visible values that should be.
# (cf import foo as _foo)
#
#

from Axon.AxonExceptions import AxonException as _AxonException

class socketSendFailure(_AxonException): pass
class connectionClosedown(_AxonException): pass
class connectionDied(connectionClosedown): pass
class connectionDiedSending(connectionDied): pass
class connectionDiedReceiving(connectionDied): pass
class connectionServerShutdown(connectionClosedown): pass

class BadRequest(_AxonException):
   "Thrown when parsing a request fails"
   def __init__(self, request, innerexception):
      self.request = request
      self.exception = innerexception
