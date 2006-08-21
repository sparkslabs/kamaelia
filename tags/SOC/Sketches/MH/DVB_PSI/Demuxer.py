#!/usr/bin/env python

# automagic channel tuner
# you set up a DVB_Multiplex component tuned to the right multiplex
#
# then create one of these, saying which channel you want and it'll try to
# find the audio and video streams for it

from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT

import dvb3.frontend
import struct

DVB_RESYNC      = chr(0x47)
DVB_PACKET_SIZE = 188

class DVB_Demuxer(AdaptiveCommsComponent):
    """\
    This demuxer expects to recieve the output from a DVB_Multiplex
    component on its primary inbox. 
    
    The output here is still transport stream packets. Another layer
    is required to decide what to do with these - to yank out the PES
    and ES packets.
    
    Clients subscribe by sending ADD and REMOVE messages to the "request"
    inbox. Messages are of the form:
        ("ADD",    (dest_component, dest_inboxname), [pid, pid, ...])
        ("REMOVE", (dest_component, dest_inboxname), [pid, pid, ...])
    
    This instructs this demuxer to add/remove the specified PIDs to those being
    sent (if any) to the specified destination. 
    
    DVB_Demuxer automatically handles wiring/unwiring from the destination.
    Eg. After a REMOVE message that reduces the number of PIDs being sent to the
    destination to zero, it will be automatically unwired.
    """
    Inboxes = {
        "inbox" : "This is where we expect to recieve a transport stream",
        "request" : "Where we receive add and remove messages",
        "control" : "We will receive shutdown messages here",
    }
    Outboxes = {
        "outbox" : "NOT USED",
        "signal" : "Shutdown signalling",
        "pid_request" : "Messages to subscribe/unsubscribe from PIDs",
    }
    

    def errorIndicatorSet(self, packet):  return ord(packet[1]) & 0x80
    def scrambledPacket(self, packet):    return ord(packet[3]) & 0xc0

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                self.shuttingdown=True
        return self.shuttingdown
    
    def main(self):
        self.pid2outboxes = {} # indexed by pid, to list of boxnames
        self.boxRefCount  = {} # indexed by outboxname
        self.boxes        = {} # indexed by destination
        self.linkages     = {} # indexed by destination
        # destination is (component,inboxname)
        
        buffer = ""
        buffers = []
        self.shuttingdown=False
        
        while not self.shutdown():
            
            while self.dataReady("request"):
                cmd = self.recv("request")
                self.handleCommand(cmd)
                
            while self.dataReady("inbox"):
                buffers.append(self.recv("inbox"))
                
            while len(buffers)>0:
                
                if len(buffer) == 0:
                    buffer = buffers.pop(0)
                else:
                    buffer += buffers.pop(0)
    
                while len(buffer) >= DVB_PACKET_SIZE:
                      i = buffer.find(DVB_RESYNC)
                      if i == -1: # if not found
                          "we have a dud"
                          buffer = ""
                          continue
                      if i>0:
                          # if found remove all bytes preceeding that point in the buffers
                          # And try again
                          buffer = buffer[i:]
                          continue
                      # packet is the first 188 bytes in the buffer now
                      packet, buffer = buffer[:DVB_PACKET_SIZE], buffer[DVB_PACKET_SIZE:]
    
                      if self.errorIndicatorSet(packet): continue
                      if self.scrambledPacket(packet):   continue
    
                      pid = struct.unpack(">H", packet[1: 3])[0] & 0x1fff
    
                      # Send the packet to the outbox appropriate for this PID.
                      # "Fail" silently for PIDs we don't know about and weren't
                      # asked to demultiplex
                      try:
                          for outbox in self.pid2outboxes[ pid ]:
                              self.send(packet, outbox)
                      except KeyError:
                          pass
                          
            self.pause()
            yield 1

    def handleCommand(self,cmd):
        if cmd[0] == "ADD":
            pidlist, dest = cmd[1], cmd[2]          # dest = (component,inboxname)
            
            # get, or set up the outbox
            try:
                outboxname = self.boxes[dest]
            except KeyError:
                outboxname = self.addOutbox("outbox")
                self.boxes[dest] = outboxname
                self.linkages[dest] = self.link((self,outboxname),dest)
                self.boxRefCount[outboxname] = 0
                
            # for each pid
            for pid in pidlist:
                # get, or set up, the list of destinations for that pid
                try:
                    outboxes = self.pid2outboxes[pid]
                except KeyError:
                    outboxes = []
                    self.pid2outboxes[pid] = outboxes
                    # subscribe to this pid
                    self.send(("ADD",[pid]), "pid_request")
                    
                if outboxname not in outboxes:
                    outboxes.append(outboxname)
                    self.boxRefCount[outboxname] += 1
            
        elif cmd[0] == "REMOVE":
            pidlist, dest = cmd[1], cmd[2]
            
            # skip if we dont' actually know about this destination
            try:
                outboxname = self.boxes[dest]
            except KeyError:
                return
                
            for pid in pidlist:
                try:
                    outboxes = self.pid2outboxes[pid]
                
                    if outboxname in outboxes:
                        outboxes.remove(outboxname)
                        self.boxRefCount[outboxname] -=1
                        
                    if outboxes == []:
                        del self.pid2outboxes[pid]
                        self.send(("REMOVE",[pid]), "pid_request")
                        
                except KeyError:
                    pass
                    
            # if nothing else going to this outbox, unlink it, delete it
            # and delete appropriate dtaa structures
            if self.boxRefCount[outboxname] == 0:
                self.unlink(thelinkage=self.linkages[dest])
                self.deleteOutbox(outboxname)
                
                del self.linkages[dest]
                del self.boxes[dest]
                del self.refCount[outboxname]
                
                
                
if __name__=="__main__":
    
    # a little test rig
    import random
    
    class PacketSource(component):
        def main(self):
            while 1:
                for pid in range(0,10):
                    packet = DVB_RESYNC + chr(0x00) + chr(pid) + chr(0x00) + " "*184
                    self.send(packet,"outbox")
                    yield 1
    
    class Subscriber(component):
        def __init__(self, servicename, spacing, *pids):
            super(Subscriber,self).__init__()
            self.notsubscribed = list(pids)
            self.subscribed = []
            self.spacing = " "*spacing
            self.servicename = servicename
            
        def takesomefrom(self,source):
            items = []
            if len(source):
                qty = 1+random.randrange(0,len(source))
                for _ in range(0,qty):
                    i = random.randrange(0,len(source))
                    items.append(source[i])
                    del source[i]
            return items
                
        def changeSubscription(self):
            if random.randrange(0,2) == 1:
                pids = self.takesomefrom(self.notsubscribed)
                self.send( ("ADD",pids,(self,"inbox")), "outbox")
                self.subscribed.extend(pids)
            else:
                pids = self.takesomefrom(self.subscribed)
                self.send( ("REMOVE",pids,(self,"inbox")), "outbox")
                self.notsubscribed.extend(pids)
            print self.spacing,"Now subscribed to pids:"
            print self.spacing,"  ",self.subscribed
                
        def main(self):
            cat = CAT.getcat()
            service = cat.retrieveService(self.servicename)
            self.link((self,"outbox"),service)
            
            nextchangetime = self.scheduler.time + random.randrange(5,10)
            self.notyetreceived = self.subscribed[:]
            while 1:
                while self.dataReady("inbox"):
                    packet = self.recv("inbox")
                    pid = ((ord(packet[1]) << 8) + ord(packet[2])) & 0x1fff
                    if pid not in self.subscribed:
                        print self.spacing,"Shouldn't have received pid:",pid
                    else:
                        if pid in self.notyetreceived:
                            print self.spacing,"Received 1st of pid:",pid
                            self.notyetreceived.remove(pid)
                        
                if self.scheduler.time >= nextchangetime:
                    nextchangetime = self.scheduler.time + random.randrange(10,20)
                    self.changeSubscription()
                    self.notyetreceived = self.subscribed[:]
                
                if self.subscribed:
                    self.pause()
                yield 1
                
    print "---1st subscriber:------|---2nd subscriber:------"
    
    Subscriber("MUX1", 0,  1,2,3,4,5).activate()
    Subscriber("MUX1", 25, 1,2,3,4,5).activate()

    from Kamaelia.Chassis.Pipeline import pipeline
    from sys import path
    path.append("..")
    from ServiceWrapper import Service
    
    pipeline( PacketSource(),
              Service(DVB_Demuxer(),{"MUX1":"request"}),
            ).run()
