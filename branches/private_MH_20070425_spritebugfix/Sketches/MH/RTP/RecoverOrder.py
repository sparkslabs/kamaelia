#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess


class RecoverOrder(component):
   """\
   RecoverOrder() -> new RecoverOrder component.

   Receives and buffers (seqnum, data) pairs, and reorders them by ascending
   sequence number and emits them (when its internal buffer is full).
   """
   def __init__(self, bufsize=30, modulo=None):
      super(RecoverOrder,self).__init__()
      self.bufsize=bufsize
      self.modulo=modulo
   
   def main(self):
      """Main loop."""
      bufsize = self.bufsize
      
      datasource = []
      while 1:
         if not self.anyReady():
             self.pause()
         yield 1
         while self.dataReady("inbox"):
            item = self.recv("inbox")
            self.insertitem(datasource,item)
      
            if len(datasource) == bufsize:
               try:
                  if datasource[0] != datasource[1]:
                     self.send(datasource[0], "outbox")
               except IndexError:
                   self.send(datasource[0], "outbox")
               del datasource[0]

      need_clean_shutdown_make_this_true_and_fix = False
      if need_clean_shutdown_make_this_true_and_fix:
         while datasource != []:
            try:
               if datasource[0] != datasource[1]:
                     self.send(datasource[0], "outbox")
            except IndexError:
                     self.send(datasource[0], "outbox")
            del datasource[0]

   def insertitem(self,buffer,item):
        # print seqnum every 1024 items, so we can see progress is happening
        if 0== (item[0] & 0x3ff):
            print item[0]
   
        if len(buffer)==0:
            buffer.insert(0,item)
        else:
            # determine wrap point
            midindex = buffer[len(buffer)/2][0]
            thresh = (midindex + self.modulo/2) % self.modulo
            
            index = item[0]
            if index<thresh:
                index = index+self.modulo
                
            # find the right place to insert into the buffer, such that it remains ordered
            # speculatively test front first (hopefully already in order!)
            cmp=buffer[-1][0]
            if (index <= cmp) or (index <= cmp+self.modulo):
                buffer.append(item)
            else:
                # ah well, out of order, do binary search to find the right place to insert
                lo=-1
                hi=len(buffer)
                while hi-lo > 1:
                    mid=(lo+hi)/2
                    midindex = buffer[mid][0]
                    if midindex<thresh:
                        midindex = midindex+self.modulo
                    if index < midindex:
                        hi=mid
                    else:
                        lo=mid
                buffer.insert(mid,item)
