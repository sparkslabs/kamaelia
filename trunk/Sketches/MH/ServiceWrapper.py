#!/usr/bin/env python

# service wrapper
# wrapper that turns something into a service


from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT


def Service(component, *services):
    super(Service,self).__init__()

    cat = CAT.getcat()
    for (name, boxname) in services:
        
        try:
            cat.registerService(name, comp, boxname)
        except Axon.AxonExceptions.ServiceAlreadyExists, e:
            print "***************************** ERROR *****************************"
            print "An attempt to reuse service names happened."
            print "This is incorrect usage."
            print 
            traceback.print_exc(3)
            print "***************************** ERROR *****************************"

            raise e

    return component
