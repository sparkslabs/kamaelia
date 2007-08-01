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

from Axon.AdaptiveCommsComponent import _AdaptiveCommsable

# Mixin to make it easy to make something into a subscribable service
def SubscribableService(inboxname="request"):
    class Mixin(_AdaptiveCommsable):
        def __init__(self):
            super(Mixin,self).__init__()
            self.addInbox(inboxname)
            self.__inboxname = inboxname
            self.__key2outboxes = {}
            self.__linkages    = {}
            self.__boxes       = {}
            self.__boxRefCount = {}
            
        def handleSubscriptions(self):
            #call me in your main loop
            while self.dataReady(self.__inboxname):
                cmd = self.recv(self.__inboxname)
                self.__handleCommand(cmd)
                
        def sendToSubscribers(self, data, key):
            # call me to send to subscribers
            for outboxname in self.__key2outbox[key]:
                self.send(data, outboxname)
                
        def sendToAllSubscribers(self, data):
            # call me to send to all subscribers
            for outboxname in self.__boxes.values():
                self.send(data, outboxname)
                
        def numberOfSubscribers(self):
            return len(self.__boxes)
                
        def __handleCommand(self, cmd):
            if cmd[0] == "ADD":
                keylist, dest = cmd[1], cmd[2]          # dest = (component,inboxname)
                
                # get, or set up the outbox
                try:
                    outboxname = self.__boxes[dest]
                except KeyError:
                    outboxname = self.addOutbox("outbox")
                    self.__boxes[dest] = outboxname
                    self.__linkages[dest] = self.link((self,outboxname),dest)
                    self.__boxRefCount[outboxname] = 0
                    
                # for each key
                for key in keylist:
                    # get, or set up, the list of destinations for that key
                    try:
                        outboxes = self.__key2outboxes[key]
                    except KeyError:
                        outboxes = []
                        self.__key2outboxes[key] = outboxes
                        
                    if outboxname not in outboxes:
                        outboxes.append(outboxname)
                        self.__boxRefCount[outboxname] += 1
                
            elif cmd[0] == "REMOVE":
                keylist, dest = cmd[1], cmd[2]
                
                # skip if we dont' actually know about this destination
                try:
                    outboxname = self.__boxes[dest]
                except KeyError:
                    return
                    
                for key in keylist:
                    try:
                        outboxes = self.__key2outboxes[key]
                    
                        if outboxname in outboxes:
                            outboxes.remove(outboxname)
                            self.__boxRefCount[outboxname] -=1
                            
                        if outboxes == []:
                            del self.__key2outboxes[key]
                            
                    except KeyError:
                        pass
                        
                # if nothing else going to this outbox, unlink it, delete it
                # and delete appropriate dtaa structures
                if self.__boxRefCount[outboxname] == 0:
                    self.unlink(thelinkage=self.__linkages[dest])
                    self.deleteOutbox(outboxname)
                    
                    del self.__linkages[dest]
                    del self.__boxes[dest]
                    del self.__boxRefCount[outboxname]
                    
    return Mixin
                
                
def Subscribing(servicename, inboxname="inbox"):
    class Mixin(_AdaptiveCommsable):
        def __init__(self):
            super(Mixin,self).__init__()
            self.__suboutboxname = self.addOutbox("subcription requests")
    
        def subscribeTo(self, *keys):
            self.__service_handle, self.__service = self.acquireService(self.servicename)
            
            self.__linkage = self.link((self,self.__suboutboxname),self.__service)
            self.send(("ADD",keys,(self,inboxname)), self.__suboutboxname)
            print "Registering"
            
        def unsubscribeFrom(self, *keys):
            self.send(("REMOVE",keys,(self,inboxname)), self.__suboutboxname)
            print "Deregistering"
            
    return Mixin
# ---------------------
# now some test code

from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

class CharGen( SubscribableService(inboxname="request"),
               component
             ):
                    
    def main(self):
        while not self.dataReady("control"):
            self.handleSubscriptions()
                
            self.sendToAllSubscribers(self.numberOfSubscribers())
                
            yield 1
    
            

class ServiceUser(Subscribing(servicename="TEST"),
                  component):
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
        
        self.subscribeTo(1)
        
        n=self.count
        while n>0:
            while self.dataReady("inbox"):
                msg=self.recv("inbox")
                print msg,
                n=n-1
            self.pause()
            yield 1
            
        self.unsubscribeFrom(1)
#        self.releaseService(service_handle)  # not needed, as the component tracks this
        
        
GLOBAL_TRACKER.setupService("TEST",CharGen,"request")

ServiceUser("TEST",0,10).activate()
ServiceUser("TEST",0,5).activate()
ServiceUser("TEST",0,20).activate()
ServiceUser("TEST",50,10).activate()
ServiceUser("TEST",55,10).run()
