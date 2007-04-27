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

    First need a more generic chooser - one where you can add items to the list dynamically
       - using the chooser as the recorder and the means to step through the data
       - then build a recorder around this that does the time based stuff  
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import time

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
                if self.pos != 0:
                    self.emit()
        
            elif cmd == "PREV":
                self.pos -= 1
                if self.pos != len(self.buffer)-1:
                    self.emit()
                
            else:
                pass

      
    def emit(self):
        if self.pos >= 0 and self.pos < len(self.buffer):
            self.send( self.buffer[self.pos], "outbox")

          

class timestamper(component):
    """Timestamps data.
    
       If 'data' arrives in the inbox, (timestamp, data) is sent out of the outbox

       As data is passed through this component, the timestamps are guaranteed
       to be unique and ordered.

       The timestamp is a tuple (system_timestamp, sequencenumber)
       The combination if these two values is guaranteed to be unique, and
       for two timestamps A and B, where B was generated after A, it is guaranteed
       that A < B.
    """
    
    def main(self):

        seqcount = 0
        oldt = time.time()
        while not self.shutdown():
            t = time.time()
            while self.dataReady("inbox"):
                if t == oldt:
                    seqcount += 1
                else:
                    seqcount = 0
                    oldt = t
                timestamp = (t, seqcount)
                data = self.recv("inbox")
                self.send( (timestamp, data), "outbox" )

            self.pause()
            yield 1

              
    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
            

class detuple(component):
    """Detuples data"""

    def __init__(self, index):
        super(detuple, self).__init__()
        self.index = index

    def main(self):
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send( data[self.index], "outbox")

            self.pause()
            yield 1

    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
            

        
class directionNormaliser(component):
    """Takes data in the form (timestamp, A, B).
    
       If timestamp > previous received timestamp, return A
       If timestamp < previous received timestamp, return B
       If timestamp == previous received timestamp, shouldn't happen

       For the very first item received, A will be returned
    """

    def main(self):
        while not self.shutdown() and not self.dataReady("inbox"):
            self.pause()
            yield 1

        if not self.dataReady("inbox"):
            return

        data = self.recv("inbox")
        timestamp = data[0]
        self.send( data[1], "outbox" )
        direction = +1

        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data[0] > timestamp:
                    direction = +1
                    self.send( data[1], "outbox" )
                elif data[0] < timestamp:
                    direction = -1
                    self.send( data[2], "outbox" )
                else:
                    raise "directionNormaliser component entered unsafe state"

            self.pause()
            yield 1
            

    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

        
            
class PlayControl(component):
    """A PVR like playback interface. Uses an external (ordered) datasource like a chooser.

       Requires data to be timestamped - in the form (timestamp, data....)
       
       Fetches one in advance, so needs behaviour semantics as defined in RecordingChooser.

    """
          
    Inboxes  = { "inbox"     : "control 'PLAY', 'STOP', 'NEXT', 'PREV', 'RPLAY",
                 "control"   : "",
                 "playspeed" : "speed of play (must be >0 ... 0.5=halfspeed, 1.0=realtime, 2.0=doublespeed...)",
                 "data"      : "items of timestamped data, returned from the datasource",
               }
    Outboxes = { "outbox"  : "outgoing data",
                 "signal"  : "",
                 "datareq" : "requests for data 'NEXT', 'PREV'"
               }
               
    def __init__(self, initialMode="PLAY", initalPlaySpeed = 1.0):
        super(PlayControl, self).__init()
        
        if initialPlaySpeed <= 0:
            raise AttributeError("Play speed must be > 0.0")
        self.speed = initialPlaySpeed
        
        if initialMode == "PLAY":
           self.direction = "NEXT"
        elif initialMode == "RPLAY":
            self.direction = "PREV"
        else:
            self.direction = None
        

        
    def main(self):
        
        self.pendingRequests = [] # 'NEXT' and 'PREV' requests that have not yet been fulfilled by the datasource
        self.prevTimestamp = None        # the timestamp of the most recently received from the datasource
                                  
        self.waitingData = [] # data waiting for the right time to be sent
        self.lastSentTimestamp = None   # timestamp of last piece of data sent from the waitingData queue
        self.lastSentMoment = None      # moment in 'real' time at which this was done

        # get the ball rolling
        if self.direction:
            self.issue(self.direction)

        while not self.shutdown():
            self.handleData()
            self.handleCommands()
            self.emitData()
            self.makeRequests()
            
            yield 1

    def request(self, cmd):
        """Issue a data request and also add it to the list of pending requests"""
        self.pendingRequests.append( cmd )
        self.send(cmd, "datareq")


    def handleData(self):
        """Deal with data returned from the chooser style component"""
        while self.dataReady("data"):
            data = self.recv("data")
            timestamp = data[0]
            #payload = data[1:]

            # lets work out whether this item is a NEXT or PREV step
            # if its the first step, then we assume its the same as the pending request
            direction = None
            if prevTimestamp == None:
                direction = self.pendingRequests[0]
            elif timestamp > prevTimestamp:
                direction = "NEXT"
            elif timestamp < prevTimestamp:
                direction = "PREV"
            else:
                raise "Two items received with the same timestamp. Cant handle."

            # pop items off until we find one that matches the direction the data has moved in
            while self.pendingRequests:
                req = self.pendingRequests[0]
                del self.pendingRequests[0]
                if req == direction:
                    break

            # add to the 'to be sent out' queue
            self.waitingData.append( data )

            
    def emitData(self):
        """Emit data at the right time"""

        # if the mode is PLAY or RPLAY we know what to do - if the data is in the right direction, emit, otherwise
        # discard

        nothingtodo=False

        while self.waitingData and not nothingtodo:
            data = self.waitingData[0]
            (timestamp, payload) = data
            timenow = time.time()
            
            if self.direction == None:
                # if not in a 'play' or 'rplay' mode then this must be stepping data, so send it immediately
                del self.waitingData[0]
                self.send( data, "outbox")
                
            elif self.direction == "NEXT":

                if (self.lastSentTimestamp == None):        # bootstrap the process
                    self.send( data, "outbox" )
                    del self.waitingData[0]
                    self.lastSentTimestamp = timestamp
                    self.lastSentMoment = timenow
                    
                elif (self.lastSentTimestamp > timestamp):
                    del self.waitingData[0]
                    
                else:
                    nextMoment = self.lastSentMoment + (timestamp - self.lastSentTimestamp)/self.speed

                    if timenow >= nextMoment:
                        self.send( data, "outbox" )
                        del self.waitingData[0]
                        self.lastSentTimestamp = timestamp
                        self.lastSentMoment = nextMoment      # could be timenow, but this hopefully avoids gradual drift
                    else:
                        nothingtodo = True
                
            elif self.direction == "PREV":
    
                if (self.lastSentTimestamp == None):        # bootstrap the process
                    self.send( data, "outbox" )
                    del self.waitingData[0]
                    self.lastSentTimestamp = timestamp
                    self.lastSentMoment = timenow
                    
                elif (self.lastSentTimestamp < timestamp):
                    del self.waitingData[0]
                    
                else:
                    nextMoment = self.lastSentMoment + (self.lastSentTimestamp - timestamp)/self.speed  # time running backwards

                    if timenow >= nextMoment:
                        self.send( data, "outbox" )
                        del self.waitingData[0]
                        self.lastSentTimestamp = timestamp
                        self.lastSentMoment = nextMoment      # could be timenow, but this hopefully avoids gradual drift
                    else:
                        nothingtodo = True
                
            else:
                raise "Unsafe state - self.direction set to invalid value"


        
    def makeRequests(self):
        """Ensure a steady flow of requests to the data source if in play mode"""
        if self.direction:              # if in PLAY or RPLAY mode

            # note we achieve rate limiting by taking into account the waitingData queue
            if len(self.pendingRequests) + len(waitingData) < 1:    # threshold
                self.issue(self.direction)


    def handleCommands(self):
        """Handle incoming commands to change the play mode (PLAY, STOP, RPLAY, NEXT, PREV)"""

        while self.dataReady("playspeed"):
            newspeed = self.recv("playspeed")
            if newspeed > 0 and newspeed != self.speed:
                # could do with sorting along the lines of the variable rate control component
                # - to handle speed changes mid stride
                self.speed = newspeed
       
        
        while self.dataReady("inbox"):
            cmd = self.recv("inbox").upper()

            if cmd == "STOP":
                self.direction = None

            elif cmd == "PLAY" or cmd == "RPLAY":
                newdirection = "NEXT"
                if cmd == "RPLAY":
                    newdirection = "PREV"
                    
                if newdirection != self.direction:
                    self.direction = newdirection
                    # look at the pending request queue, tally up how far the
                    # pending requests will offset us from the direction we need to
                    # move
                    #
                    # eg. if newdirection=PREV, and pending=[NEXT, PREV, NEXT]
                    # then tally = +1-1+1 = +1
                    #
                    # then move that much to compensate and move one further
                    offset = 0
                    for req in self.pendingRequests:
                        if req == self.direction:
                            offset -= 1
                        else:
                            offset += 1

                    offset += 1
                    for i in range(0, offset):
                        self.issue(self.direction)

                    self.lastSentTimestamp = None # reset time syncing for output


            elif cmd == "NEXT" or cmd == "PREV":
                if self.direction == None:          # if not in play mode, otherwise do nothing
                    self.issue(cmd)

                    
    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
        
        

class pairer(component):
    """Takes values coming in from two inboxes and pairs them as a tuple (inbox, inbox2)"""
    Inboxes  = { "inbox"   : "first item in the tuple",
                 "inbox2"  : "second item in the tuple",
                 "control" : "",
               }

    def main(self):
        self.queues = [ ("inbox", []),
                        ("inbox2", [])
                      ]

        while not self.shutdown():

            # read incoming data
            for (box, q) in self.queues:
               while self.dataReady(box):
                   q.append( self.recv(box) )

            # send out stuff
            while 0 not in [len(q) for (box,q) in self.queues]:
                data = tuple([ q[0] for (box,q) in self.queues ])
                self.send(data, "outbox")
                for (box,q) in self.queues:
                    del q[0]

            yield 1
            self.pause()
            
                
        
class topologyReverser(component):
    """Takes topology commands in lists and outputs reverse commands in lists

       eg.
         [ ("ADD","NODE",blah) ] --> [ ("DEL","NODE",blah) ]
         [ ("DEL","NODE",blah) ] --> [ ("ADD","NODE",blah), ("ADD","LINK",blah) ]
         
    """

    def __init__(self):
        super(topologyReverser, self).__init__()

        self.nodes = {}   # id -> (id, name, other data)
        self.links = {}   # from,to -> (from, to, other data)
        

    def main(self):
        
        while not self.shutdown():

            while self.dataReady("inbox"):
                cmds = self.recv("inbox")
                output = []
                for cmd in cmds:
                    output.extend( list(self.reverse(cmd)) )
                    
                if output:
                    self.send(output, "outbox")
                    
            
            yield 1
            self.pause()

    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

                                

    def reverse(self, msg):
        """Reverse a topology command"""
        try:            
            if len(msg) >= 2:
                cmd = msg[0].upper(), msg[1].upper()

            if cmd == ("ADD", "NODE"):
                self.nodes[msg[2]] = msg[2:]        # add to table of nodes
                yield ["DEL", "NODE"] + msg[2:]
                return

            elif cmd == ("DEL", "NODE"):
                yield ["ADD", "NODE"] + self.nodes[msg[2]]
                del self.nodes[msg[2]]
                for link in self.links:
                    if link[0] == msg[2] or link[1] == msg[2]:
                        yield ["ADD","LINK"] + link
                        del self.links[ (link[0],link[1]) ]
                        

            elif cmd == ("ADD", "LINK"):
                self.links[ (msg[2],msg[3]) ] = msg[2:]   # add to table of links
                yield ["DEL", "LINK"] + msg[2:]
                return

            elif cmd == ("DEL", "LINK"):
                yield ["ADD", "LINK"] + self.links[ (msg[2],msg[3]) ]
                del self.links[ (msg[2],msg[3]) ]        # remove from table of links
                return

            elif cmd == ("DEL", "ALL") and len(msg) == 2:
                for node in self.nodes:
                    yield ["ADD","NODE"] + node
                for link in self.links:
                    yield ["ADD","LINK"] + link
                self.nodes = {}
                self.links = {}

        yield cmd    # pass through anything else

        
    def shutdown(self):
        """Checks for and passes on shutdown messages"""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

