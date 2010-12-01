#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
===============================================
Axon - the core concurrency system for Kamaelia
===============================================

Axon is a component concurrency framework. With it you can create software
"components" that can run concurrently with each other. Components have
"inboxes" and "outboxes" through with they communicate with other components.

A component may send a message to one of its outboxes. If a linkage has been
created from that outbox to another component's inbox; then that message will
arrive in the inbox of the other component. In this way, components can send
and receive data - allowing you to create systems by linking many components
together.

Each component is a microprocess - rather like a thread of execution. A
scheduler takes care of making sure all microprocesses (and therefore all
components) get regularly executed. It also looks after putting microprocesses
to sleep (when they ask to be) and waking them up (for example, when something
arrives in one of their inboxes).



Base classes for building your own components
---------------------------------------------

* **Axon.Component**

  - defines the basic component. Subclass it to write your own components.

* **Axon.AdaptiveCommsComponent**

  - like a basic component but with facilties to let you add and remove inboxes
    and outboxes during runtime.

* **Axon.ThreadedComponent**

  - like ordinary components, but which truly run in a separate thread - meaning
    they can perform blocking tasks (since they don't have to yield control to
    the scheduler for other components to continue executing)
     


Underlying concurrency system
-----------------------------

* **Axon.Microprocess**

  - Turns a python generator into a schedulable microprocess - something that
    can be started, paused, reawoken and stopped. Subclass it to make your own.

* **Axon.Scheduler**

  - Runs the microprocesses. Manages the starting, stopping, pausing
    and waking of them. Is also a microprocess itself!



Services, statistics, Instrospection
------------------------------------
    
* **Axon.CoordinatingAssistantTracker**

  - provides mechanisms for components to advertising and discover services they
    can provide for each other.

  - acts as a repository for collecting statistics from components in the system

* **Axon.Introspector**

  - outputs live topology data describing what components there are in a
    running axon system and how they are linked together.


        
Exceptions, Messages and Misc
-----------------------------

* **Axon.Axon**

  - base metaclass for key Axon classes

* **Axon.AxonExceptions**

  - classes defining various exceptions in Axon.
  
* **Axon.Ipc**

  - classes defining various IPC messages in Axon used for signalling shutdown,
    errors, notifications, etc...

* **Axon.idGen**

  - unique id value generation

* **Axon.util**

  - various miscellaneous support utility methods



Integration with other systems
------------------------------

* **Axon.background**

  - use Axon components within other python programs by wrapping them in
    a scheduler running in a separate thread
  
* **Axon.Handle**

  - a Handle for getting data into and out of the standard inboxes and outboxes
    of a component from a non Axon based piece of code. Useful in combination
    with Axon.background



Internals for implementing inboxes, outboxes and linkages
---------------------------------------------------------

* **Axon.Box**

  - The base implementation of inboxes and outboxes.

* **Axon.Postoffice**

  - All components have one of these for creating, destroying and tracking
    linkages.

* **Axon.Linkage**

  - handles used to describe linkages from one postbox to another

What, no Postman? Optimisations made to Axon have dropped the Postman.
Inboxes and outboxes handle the delivery of messages themselves now.



Debugging support
-----------------

* **Axon.debug**

  - defines a debugging output object.
  
* **Axon.debugConfigFile**

  - defines a method for loading a debugging configuration file that determines
    what debugging output gets displayed and what gets filtered out.
    
* **Axon.debugConfigDefaults**

  - defines a method that supplies a default debugging configuration.
"""
import Component
import Ipc
import Linkage
import Microprocess
import Postoffice
import Scheduler
import debug
import util
import AdaptiveCommsComponent
import AxonExceptions
import CoordinatingAssistantTracker
import debugConfigFile
import Box
import ThreadedComponent
import Introspector

from Axon import AxonObject, AxonType

Microprocess.microprocess.setSchedulerClass(Scheduler.scheduler)
#Microprocess.microprocess.setTrackerClass(CoordinatingAssistantTracker.coordinatingassistanttracker)
Microprocess.microprocess.setTrackerClass(None)
CoordinatingAssistantTracker.coordinatingassistanttracker()
Scheduler.scheduler() # Initialise the class.
