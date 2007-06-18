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

# modify the existing Axon.Component.component
# ... bit messy I know, but hey!

__component_old___init__               = Axon.Component.component.__init__
__component_old__closeDownMicroprocess = Axon.Component.component._closeDownMicroprocess

def __component_new___init__(self):
        __component_old___init__(self)
        del self.tracker
        self.tracker = GLOBAL_TRACKER
        self.service_handles = []
        
def __component_new_acquireService(self,name):
    handle, service = self.tracker._acquireService(self, name)
    self.service_handles.append(handle)
    return handle, service

def __component_new_releaseService(self,handle):
    self.service_handles.remove(handle)
    return self.tracker._releaseService(handle)

def __component_new__closeDownMicroprocess(self):
    for handle in self.service_handles:
        self.tracker._releaseService(handle)
    return __component_old__closeDownMicroprocess(self) 

Axon.Component.component.__init__ = __component_new___init__
Axon.Component.component.acquireService = __component_new_acquireService
Axon.Component.component.releaseService = __component_new_releaseService
Axon.Component.component._closeDownMicroprocess = __component_new__closeDownMicroprocess

from Axon.Component import component

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
            

class ServiceUser(component):
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
#        self.releaseService(service_handle)  # not needed, as the component tracks this
        
        
GLOBAL_TRACKER.setupService("TEST",CharGen,"request")

ServiceUser("TEST",0,10).activate()
ServiceUser("TEST",0,5).activate()
ServiceUser("TEST",0,20).activate()
ServiceUser("TEST",50,10).activate()
ServiceUser("TEST",55,10).run()
