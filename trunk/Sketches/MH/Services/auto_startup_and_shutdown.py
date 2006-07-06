#!/usr/bin/env python

# experiment in ways to do services

import Axon.Component
from Axon.Ipc import shutdownMicroprocess


class ServiceTracker(object):
    
    def __init__(self):
        super(ServiceTracker,self).__init__()
        self.services = {}
        self.serviceUsageHandles = {}
        
    def setupService(self, name, componentFactory, inboxname):
        
        self.services[name] = { "factory"  : componentFactory,
                                "inboxname" : inboxname,
                                "refcount"  : 0,
                              }
                              
    def _acquireService(self, caller, name):
        try:
            service = self.services[name]
        except KeyError:
            raise "NO SUCH SERVICE AVAILABLE"
        
        if service['refcount'] == 0:
            # need to start the service
            service['instance'] = service['factory']()
            service['instance'].activate(caller.scheduler)
        
        instance = service['instance']
        service['refcount'] += 1
        newhandle = object()
        self.serviceUsageHandles[newhandle] = name
        return (newhandle, (instance, service['inboxname']))
        
    def _releaseService(self, handle):
        try:
            name = self.serviceUsageHandles[handle]
        except KeyError:
            raise "NO SUCH HANDLE"
        
        del self.serviceUsageHandles[handle]
        
        service = self.services[name]
        service['refcount'] -= 1
        if service['refcount'] == 0:
            service['instance']._deliver(shutdownMicroprocess(), "control")
            del service['instance']

GLOBAL_TRACKER = ServiceTracker()


class newComponent(Axon.Component.component):
    def __init__(self):
        super(newComponent,self).__init__()
        del self.tracker
        self.tracker = GLOBAL_TRACKER
        self.service_handles = []
            
    def acquireService(self,name):
        handle, service = self.tracker._acquireService(self, name)
        self.service_handles.append(handle)
        return handle, service
    
    def releaseService(self,handle):
        self.service_handles.remove(handle)
        return self.tracker._releaseService(handle)
    
    def _closeDownMicroprocess(self):
        for handle in self.service_handles:
            self.tracker._releaseService(handle)
        return super(newComponent,self)._closeDownMicroprocess() 

## override!!!
#Axon.Component.component = newComponent


# ---------------------
# now some test code

from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

class CharGen(AdaptiveCommsComponent):
    Inboxes = {"inbox":"",
               "control":"",
               "request":"Requests for subscriptions",
              }
              
    def main(self):
        self.destinations = {}
        self.linkages = {}
        
        print "Service started"
        while not self.dataReady("control"):
            while self.dataReady("request"):
                cmd = self.recv("request")
                self.handleCommand(cmd)
                
            for outboxname in self.destinations.values():
                self.send(len(self.destinations),outboxname)
                
            yield 1
        print "Service shutdown"
    
    def handleCommand(self,cmd):
        if cmd[0]=="ADD":
            _, dest = cmd[1:3]
            outboxname = self.addOutbox("outbox")
            self.destinations[dest] = outboxname
            self.linkages[dest] = self.link((self,outboxname),dest)
            
        elif cmd[0]=="REMOVE":
            _, dest = cmd[1:3]
            self.unlink( thelinkage=self.linkages[dest] )
            self.deleteOutbox( self.destinations[dest] )
            del self.linkages[dest]
            del self.destinations[dest]
            

class ServiceUser(newComponent):
    def __init__(self, servicename,startwhen,count):
        super(ServiceUser,self).__init__()
        self.servicename = servicename
        self.startwhen = startwhen
        self.count = count
            
    def main(self):
        n=self.startwhen
        while n>0:
            yield 1
            n-=1
        
        service_handle, service = self.acquireService(self.servicename)
        
        linkage = self.link((self,"outbox"),service)
        self.send(("ADD",None,(self,"inbox")), "outbox")
        print "Registering"
        
        n=self.count
        while n>0:
            while self.dataReady("inbox"):
                msg=self.recv("inbox")
                print msg,
                n=n-1
            self.pause()
            yield 1
            
        self.send(("REMOVE",None,(self,"inbox")), "outbox")
        print "Deregistering"
        
        self.unlink(linkage)
#        self.releaseService(service_handle)  # not needed, as the component tracks this itself now
        
        
GLOBAL_TRACKER.setupService("TEST",CharGen,"request")

ServiceUser("TEST",0,10).activate()
ServiceUser("TEST",0,5).activate()
ServiceUser("TEST",0,20).activate()
ServiceUser("TEST",50,5).run()
