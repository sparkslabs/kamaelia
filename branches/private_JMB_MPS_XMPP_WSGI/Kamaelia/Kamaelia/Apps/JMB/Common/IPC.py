#!/usr/bin/env python
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

from Axon.Ipc import producerFinished, notify

# Pull in rather than redefine the standard ipc/control messages
from Kamaelia.IPC import socketShutdown, serverShutdown
from Kamaelia.IPC import newCSA, shutdownCSA, newServer
from Kamaelia.IPC import newWriter, newReader, newExceptional
from Kamaelia.IPC import removeReader, removeWriter, removeExceptional

class userLoggedOut(notify):
   def __init__(self, thread):
      self.thread = thread
      
class batchDone(notify):
   def __init__(self, thread):
      self.thread=thread
      
class newBatch(notify):
   def __init__(self, batch, bundle, to_jid):
      self.batch_id = batch
      self.bundle = bundle
      self.to_jid = to_jid

__ipc_msgs = [removeExceptional, removeWriter, removeReader, newExceptional, newReader,
              newWriter, newServer, shutdownCSA, newCSA, serverShutdown, socketShutdown,
              userLoggedOut, batchDone, newBatch]
from Axon.Ipc import GetIPCs
__ipc_msgs.extend(GetIPCs())

__ipc_lookup = {}

def LookupByText(name):
   global __ipc_lookup
   if not __ipc_lookup:
      for item in __ipc_msgs:
         __ipc_lookup[item.__name__] = item
         
   return __ipc_lookup.get(name)

def ToText(signal):
   """Convert a signal into a text representation"""
   return type(signal).__name__
   
if __name__ == '__main__':
   signal_type = LookupByText('producerFinished')
   signal = signal_type()
   text = ToText(signal)
   
   print 'signal=%s' % (signal)
   print 'text=%s' % (text)
