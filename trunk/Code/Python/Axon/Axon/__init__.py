"""Axon -


"""
import Component, Ipc, Linkage, Microprocess, Postman, Scheduler, debug, util, AdaptiveCommsComponent, AxonExceptions, CoordinatingAssistantTracker
from Axon import AxonObject, AxonType

Microprocess.microprocess.setSchedulerClass(Scheduler.scheduler)
#Microprocess.microprocess.setTrackerClass(CoordinatingAssistantTracker.coordinatingassistanttracker)
Microprocess.microprocess.setTrackerClass(None)
CoordinatingAssistantTracker.coordinatingassistanttracker()
Scheduler.scheduler() # Initialise the class.


