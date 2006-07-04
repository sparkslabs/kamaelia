#!/usr/bin/env python

# improved PSI packet reconstructor to handle multiple packets
# this one is a service you subscribe to:
# send it a request asking to be sent PSI packets from a given set of PIDs
# and it'll instantiate PSIPacketReconstructor components as required and
# route the results to the inbox you provided.

from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor

from Axon.Ipc import shutdownMicroprocess, producerFinished
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

class PSIPacketReconstructorService(AdaptiveCommsComponent):
    """\
    
    Subscribe to PSI packets by sending ("ADD", (component,inbox), [PIDs] ) to "request"
    Unsubscribe by sending ("REMOVE", (component,inbox), [PIDs] ) to "request"
    """
    Inboxes = { "inbox" : "Incoming DVB TS packets",
                "control" : "Shutdown signalling",
                "request" : "Place for subscribing/unsubscribing from different PSI packet streams",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling",
                 "pid_request" : "For issuing requests for PIDs",
               }
               
    def __init__(self):
        super(PSIPacketReconstructorService,self).__init__()
        
        # pid handlers: key,value = PID,(outboxname,ctrlboxname,inboxname,PSIcomponent)
        # ( outbox, ctrlbox ----> PSIcomponent ----> inbox )
        self.activePids = {}
        
        # key,value = PID, [outboxnames]
        self.destinations = {}
        
        # key,value = (component, inbox),(outboxname, linkage, [PIDs])
        self.subscriptions = {}
        
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                return True
        return False
        
        
    def handleSubscribeUnsubscribe(self, msg):
        cmd, pids, dest = msg
        
        if cmd=="ADD":
            # add (or fetch existing) outbox going to this destination
            try:
                recipientOutbox, linkage, subscribedToPids = self.subscriptions[dest]
            except KeyError:
                recipientOutbox = self.addOutbox("outbox")
                linkage = self.link( (self, recipientOutbox), dest)
                subscribedToPids = []
                self.subscriptions[dest] = recipientOutbox, linkage, subscribedToPids
                
            for pid in pids:
                # add (or fetch existing) PSI packet reconstructor for this PID
                try:
                    outboxname, ctrlboxname, inboxname, PSIcomponent = self.activePids[pid]
                except KeyError:
                    # set up a new PSI packet reconstructor
                    outboxname = self.addOutbox("_toReconstructor_"+str(pid))
                    inboxname  = self.addInbox("_fromReconstructor_"+str(pid))
                    ctrlboxname = self.addOutbox("_signalReconstructor_"+str(pid))
                    PSIcomponent = PSIPacketReconstructor().activate()
                    self.addChildren(PSIcomponent)
                    self.link((self,outboxname),(PSIcomponent,"inbox"))
                    self.link((self,ctrlboxname),(PSIcomponent,"control"))
                    self.link((PSIcomponent,"outbox"),(self,inboxname))
                    self.activePids[pid] = outboxname, ctrlboxname, inboxname, PSIcomponent
                    # and subscribe to the PID for it
                    self.send( ("ADD",[pid],(self,"inbox")), "pid_request")
                    
                # add (or fetch existing) routing for this PID
                try:
                    recipientOutboxes = self.destinations[pid]
                except KeyError:
                    recipientOutboxes = []
                    self.destinations[pid] = recipientOutboxes
                    
                # for this pid, make sure our outbox is one of the recipients
                if recipientOutbox not in recipientOutboxes:
                    recipientOutboxes.append(recipientOutbox)
                    
                # for this outbox, add to the list of pids it receives
                if pid not in subscribedToPids:
                    subscribedToPids.append(pid)
                    
        elif cmd=="REMOVE":
            # work out which outbox we must be using
            try:
                recipientOutbox, linkage, subscribedToPids = self.subscriptions[dest]
            except KeyError:
                return
                
            for pid in pids:
                if pid in subscribedToPids:
                    subscribedToPids.remove(pid)
                    self.destinations[pid].remove(recipientOutbox)
                    
                    # if nobody is subscribed to this pid anymore, clean up the PSI reconstructor component etc
                    if not self.destinations[pid]:
                        del self.destinations[pid]
                        
                        # shutdown the PSI reconstructor, unlink from it, and delete inboxes/outboxes
                        outboxname, ctrlboxname, inboxname, PSIcomponent = self.activePids[pid]
                        self.send(shutdownMicroprocess(self), ctrlboxname)
                        self.removeChild(PSIcomponent)
                        self.unlink(thecomponent=PSIcomponent)
                        self.deleteOutbox(outboxname)
                        self.deleteOutbox(ctrlboxname)
                        self.deleteInbox(inboxname)
                        del self.activePids[pid]
                        # and unsubscribe from the PID for it
                        self.send( ("REMOVE",[pid],(self,"inbox")), "pid_request")
                        
            # if no longer subscribed to any PIDs on this destination, then clean it up
            if not subscribedToPids:
                self.unlink(thelinkage = linkage)
                self.deleteOutbox(recipientOutbox)
                del self.subscriptions[dest]
    
    
    def main(self):
        while not self.shutdown():
            
            while self.dataReady("request"):
                self.handleSubscribeUnsubscribe(self.recv("request"))
                    
            
            # route incoming transport stream packets according to PID to the
            # appropriate reconstructor
            while self.dataReady("inbox"):
                ts_packet = self.recv("inbox")
                
                pid = ((ord(ts_packet[1]) << 8) + ord(ts_packet[2])) & 0x01fff
                try:
                    toReconstructorBox = self.activePids[pid][0]
                    self.send(ts_packet, toReconstructorBox)
                except KeyError:
                    # not interested in this PID
                    pass
                
            # receive any reconstructed PSI packets from the reconstructors and
            # route to the subscribed destinations
            for pid in self.activePids:
                inbox = self.activePids[pid][2]
                while self.dataReady(inbox):
                    psi_packet = self.recv(inbox)
                    for outbox in self.destinations[pid]:
                        self.send(psi_packet, outbox)
                        
            self.pause()
            yield 1


if __name__ == "__main__":
    
    from Axon.Component import component
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    class PSIPacketReconstructor(component):
        """Fake packet reconstructor."""
        def main(self):
            print "Reconstructor",self.id,"starts"
            while not self.dataReady("control"):
                while self.dataReady("inbox"):
                    self.send(self.recv("inbox"),"outbox")
                self.pause()
                yield 1
            print "Reconstructor",self.id,"terminates"
    
    import random
    
    class Producer(component):
        """Fake source of packets"""
        def main(self):
            while 1:
                pid = random.randrange(0,6)
                fakepacket = "X" + chr(pid>>8) + chr(pid & 0xff) + "Y"*185
                self.send(fakepacket,"outbox")
                yield 1
                
    
    svc = PSIPacketReconstructorService()
    src = pipeline(Producer(),svc)
    
    class Subscriber(component):
        def __init__(self, spacing, *pids):
            super(Subscriber,self).__init__()
            self.notsubscribed = list(pids)
            self.subscribed = []
            self.spacing = " "*spacing
            
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
            self.link((self,"outbox"),(svc,"request"))
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
                
    Subscriber(28+0,  1,2,3,4,5).activate()
    Subscriber(28+25, 1,2,3,4,5).activate()
    
    from Kamaelia.Util.Introspector import Introspector
    from Kamaelia.Internet.TCPClient import TCPClient
    
    pipeline(Introspector(),TCPClient("r44116",1500)).activate()
    
    print "---PSI Reconstructors------|---1st subscriber:------|---2nd subscriber:------"
    src.run()
    