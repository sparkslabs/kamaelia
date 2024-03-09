#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
===========================
General Kamaelia Exceptions
===========================

This module defines a set of standard exceptions generally useful in Kamaelia.
They are all based on the Axon.AxonExceptions.AxonException base class.


The exceptions
--------------

* **BadRequest(request, innerexception)** - signalling that a request caused an
  exception``self.request`` is the original request and ``self.exception`` is
  the exception that it caused to be thrown
  
* **socketSendFailure()** - signalling that a socket failed trying to send

* **connectionClosedown()** - singalling that a connection closed down

* **connectionDied()** - signalling that a connection died
  * connectionDiedSending()
  * connectionDiedReceiving()
  * connectionServerShutdown()

"""

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
