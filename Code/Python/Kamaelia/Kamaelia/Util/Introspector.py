#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
===================================================
Detecting the topology of a running Kamaelia system
===================================================

The Introspector component introspects the current local topology of a Kamaelia
system - that is what components there are and how they are wired up.

It continually outputs any changes that occur to the topology.



Example Usage
-------------
Introspect and display whats going on inside the system::

    MyComplexSystem().activate()
    
    Pipeline( Introspector(),
              text_to_token_lists()
              AxonVisualiser(),
            )



How does it work?
-----------------

Once activated, this component introspects the current local topology of a
Kamaelia system.

Local? This component examines its scheduler to find components and postmen.
It then examines them to determine their inboxes and outboxes and the linkages
between them. In effect, it determines the current topology of the system.
    
If this component is not active, then it will see no scheduler and will report
nothing.

What is output is how the topology changes. Immediately after activation, the
topology is assumed to be empty, so the first set of changes describes adding
nodes and linkages to the topology to build up the current state of it.

Subsequent output just describes the changes - adding or deleting linkages and
nodes as appropriate.

Nodes in the topology represent components and postboxes. A linkage between
a component node and a postbox node expresses the fact that that postbox belongs
to that component. A linkage between two postboxes represents a linkage in the
Axon system, from one component to another.

This topology change data is output as string containing one or more lines. It
is output through the "outbox" outbox. Each line may be one of the following:

* "DEL ALL"
  
  - the first thing sent immediately after activation - to ensure that
    the receiver of this data understand that we are starting from nothing

* "ADD NODE <id> <name> randompos component"
* "ADD NODE <id> <name> randompos inbox"
* "ADD NODE <id> <name> randompos outbox"

  - an instruction to add a node to the topology, representing a component,
    inbox or outbox. <id> is a unique identifier. <name> is a 'friendly'
    textual label for the node.

* "DEL NODE <id>"

  - an instruction to delete a node, specified by its unique id
    
* "ADD LINK <id1> <id2>"

  - an instruction to add a link between the two identified nodes. The link is
    deemed to be directional, from <id1> to <id2>

* "DEL LINK <id1> <id2>"

  - an instruction to delete any link between the two identified nodes. Again,
    the directionality is from <id1> to <id2>.

the <id> and <name> fields may be encapsulated in double quote marks ("). This
will definitely be so if they contain space characters.

If there are no topology changes then nothing is output.

This component ignores anything arriving at its "inbox" inbox.

If a shutdownMicroprocess message is received on the "control" inbox, it is sent
on to the "signal" outbox and the component will terminate.
"""

from Axon.Introspector import Introspector as _AxonIntrospector

class Introspector(_AxonIntrospector):
    pass

__kamaelia_components__  = ( Introspector, )


if __name__ == '__main__':
   import Axon
   
   i = Introspector()
   i.activate()
   from Kamaelia.Util.Console import ConsoleEchoer
   e = ConsoleEchoer()
   e.activate()
   i.link((i,"outbox"), (e, "inbox"))
   
   print ("You should see the Introspector find that it and a ConsoleEchoer component exist.")
   print ("We both have inbox, control, signal and outbox postboxes")
   print ("The Introspector's outbox is linked to the ConsoleEchoer's inbox")
   print ("")
   Axon.Scheduler.scheduler.run.runThreads(slowmo=0)
