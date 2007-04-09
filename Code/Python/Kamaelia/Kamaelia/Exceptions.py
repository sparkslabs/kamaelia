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
