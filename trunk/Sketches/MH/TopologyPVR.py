#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# topology change pvr

# or at least the components to get there


"""
  Use cases:
    play forward/backward
    fast forward/backward
    pause
    jump
    jump to 'now'
    stepping
    jumping through checkpoints? (checkpoints could be marked up in the sequence)
    
  Generalisations of properties:
    current position
    playing/paused
    play direction and speed
    
  Generalisation of functions
    plug in a stream interpreter that generates teh 'reverse' direction stream
    playout control
    reverse stream generation
    store
    
    
  I'm thinking:
    
    Generate the stream tagged with 'how to reverse the stream' data
    (time, delta) ---> split --> detuple(0) ---------------------------------> join ---> (time, (delta, reversedelta))
                             --> detuple(1) --> split --------------> join -->
                                                      --> reverse -->
                                                    
    what about things in teh stream like 'checkpoints' or bookmarks? they're timestamp info, so they should be in that part of the stream

    First need a more generic chooser - one where you can add items to the list dynamically
       - using the chooser as the recorder and the means to step through the data
       - then build a recorder around this that does the time based stuff  
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess



class RecordingChooser(component):
    """A chooser where you add to (either end of) the list of items being iterated over at any time.
     
       RecordingChooser is a bit of a rubbish name, need a better one
    """
    Inboxes = { "nextItems" : "New items to go on the end of the list",
                "prevItems" : "New items prepend to the front of the list",
                "inbox"    : "'NEXT', 'PREV', 'FIRST', 'LAST'",
                "control"  : "",
              }
            
    Outboxes = { "outbox" : "outputs items",
                 "signal" : "",
               }
             
    def __init__(self, winding = False):
        """Initialisation.
           winding = True causes all items to be enumerated in order when jumping to FIRST or LAST
       
           next and prev requests are auto queued if you try to go past the endstops
           next/prev requests are cancelled out by each other or flushed by FIRST/LAST requests
           SAME requests are not supported
        """
        super(RecordingChooser, self).__init__()
        self.winding = winding

        
    def main(self):
        # we don't yet have a starting position in the data, this will depend on whether the initial request
        # is a NEXT/FIRST implying starting at the start
        # or a PREV/LAST implying starting at the end
        self.buffer = []
        moved = False
        self.initialpos = 0
        while not moved:
            yield 1
            self.handleNewDataNoPos()
            moved = self.handleRequestsNoPos()
      
            if self.shutdown():
                return
      
        while 1:
            yield 1
      
            self.handleNewData()
            self.handleRequests()
      
            if self.shutdown():
                return
        
        
        
    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
    
    def handleNewDataNoPos(self):
        # new items for the front of the set
        while self.dataReady("nextItems"):
            data = self.recv("nextItems")
            self.buffer.append(data)
      
        # new items for the back
        while self.dataReady("prevItems"):
            data = self.recv("prevItems")
            self.buffer.insert(0, data)
            self.initialpos += 1


    def handleRequestsNoPos(self):
    
        if self.dataReady("inbox"):
            cmd = self.recv("inbox").upper()
      
            if cmd == "SAME":
                return False
          
            elif cmd == "FIRST":
                self.pos = 0
                self.emit()
                return True
        
            elif cmd == "LAST":
                self.pos = len(self.buffer)-1
                self.emit()
                return True
        
            elif cmd == "NEXT":
                self.pos = self.initialpos
                self.emit()
                return True
        
            elif cmd == "PREV":
                self.pos = self.initialpos-1
                self.emit()
                return True
        
            else:
                return False
    
        return False
    
    
    def handleNewData(self):
        # new items for the front of the set
        while self.dataReady("nextItems"):
            data = self.recv("nextItems")
            self.buffer.append(data)
      
            #  0   1   2   3   4 new
            #                     ^
            #                    waiting to emit
            if len(self.buffer)-1  <= self.pos:
                self.send(data, "outbox")
      
        # new items for the back
        while self.dataReady("prevItems"):
            data = self.recv("prevItems")
            self.buffer.insert(0, data)
      
            if self.pos < 0:
                self.send(data, "outbox")      # emit if we're waiting for catchup
        
            self.pos += 1
      
      
    def handleRequests(self):
    
        while self.dataReady("inbox"):
            cmd = self.recv("inbox").upper()
      
            if cmd == "SAME":
                self.emit()
          
            elif cmd == "FIRST":
                if self.winding and self.pos >= 0:
                    while self.pos > 0:
                        self.pos -= 1
                        self.emit()
                else:
                    self.pos = 0
                    self.emit()
        
            elif cmd == "LAST":
                if self.winding and self.pos <= len(self.buffer)-1:
                    while self.pos < len(self.buffer)-1:
                        self.pos += 1
                        self.emit()
                else:
                    self.pos = len(self.buffer)-1
                    self.emit()
        
            elif cmd == "NEXT":
                self.pos += 1
                self.emit()
        
            elif cmd == "PREV":
                self.pos -= 1
                self.emit()
                
            else:
                pass

      
    def emit(self):
        if self.pos >= 0 and self.pos < len(self.buffer):
            self.send( self.buffer[self.pos], "outbox")

          
