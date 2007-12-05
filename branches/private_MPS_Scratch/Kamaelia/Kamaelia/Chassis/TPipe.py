#!/usr/bin/python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
============
What it does 
============

XXX TODO: Module level docs

Much like unix "tee", copies data from inboxes to outboxes but also to a
subcomponent. Copying to the subcomponent is conditional on the data, and
also

Example Usage
-------------
What this shows followed by double colon::
    def func():
        print "really really simple minimal code fragment"

Indicate any runtime user input with a python prompt::
    >>> func()
    really really simple minimal code fragment

Optional comment on any particularly important thing to note about the above 
example.

How does it work?
-----------------

Statements, written in the present tense, describing in more detail what the 
component does.

Explicitly refer to "named" inbox an "named" outbox to avoid ambiguity.

Does the component terminate? What are the conditions?

If the 'xxxx' argument is set to yyy during initialization, then something
different happens.

A subheading for a subtopic
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists of important items might be needed, such as commands:
    the item
        A description of the item, what it is and what it does, and maybe 
        consequences of that.

    another item
        A description of the item, what it is and what it does, and maybe 
        consequences of that.

You may also want bullet lists:


- first item
- second item

Optional extra topics
---------------------

May be necessary to describe something separately, eg. a complex data structure
the component expects to receive, or the GUI interface it provides.
"""

import Axon

class TPipe(Axon.Component.component):
    """\
    TPipe([condition=<callback>][,action=<Component>],[,sink=<Bool>],[,source=<Bool>]) -> new TPipe component.

    This component takes a single component as an argument. It runs this argument
    and sets it up to be able to send data to it. (and optionally recieve
    data from it) The subcomponent can obviously be any component, for example
    another pipeline, graphline, threadedcomponent or backplane.

    This component is designed to sit in a Pipeline, where there is interesting
    data flowing through. It always forwards whatever messages it recieves on its
    inboxes "inbox,control" to its outboxs "outbox,signal", *UNLESS* the flag
    "demux" is set.

    Additionally, it runs the condition provided against each piece of
    data. If the condition returns True, then the data is forwarded to the
    subcomponent, otherwise it isn't.

    If the argument "mode" is "route", then any piece of data goes either to
    the subcomponent inboxes or out the component's outboxes. If the argument
    "mode" is "split", it can go to both. The default is "split".

    Finally it takes two boolean arguments "sink" and "source. sink defaults
    to true and means that we should send data to the subcomponent. source
    defaults to false. If source is True however, any data coming out the
    subcomponents outboxes "outbox, signal" is passed through to TPipes
    outboxes "outbox, signal" (respectively).

    Keyword arguments:

    - condition -- Applied to data on inbox, forwards to subcomponent
    - action -- The subcomponent to be activated and recieve a copy of data
    - sink - If True (default) condition will be applied to data if true,
      data forwarded to action
    - source - If True (default=False), any data from action will go out
      our outbox. In a pipeline this results in data injection.
    - mode - "split" (default) or "route". "split" means the each piece of
      data can go to both the component's outboxes and the subcomponent.
      "route" means the data goes to one or the other.
    """
    Inboxes = {
        "inbox" : "Messages we may wish to pass onto the sub component",
        "control" : "Shutdown messages come here.",
        "_inbox" : "Message the subcomponent sends us back",
        "_control" : "The subcomponent may wish to send shutdown to us as well for some reason",
    }
    Outboxes = {
        "outbox" : "We always pass on all messages we recieve",
        "signal" : "We always send on shutdown messages",
        "_outbox" : "Messages we send here go to the sub component",
        "_signal" : "Shutdown messages sent here go to the sub component",
    }
    condition = None
    action = None
    sink = True
    source = False
    mode = "split"
    def main(self):
        if (self.mode != "split") and (self.mode != "route"): return
        if not self.condition: self.condition = lambda x: True
        if not self.action: return
        self.addChildren(*( self.action, ))
        self.link( (self, "_signal"), (self.action, "control") ) # Always want to be able to send a shutdown message
        if self.sink:
            self.link( (self, "_outbox"), (self.action, "inbox") )
        if self.source:
            self.link( (self.action, "outbox"), (self, "_inbox") )
            self.link( (self.action, "signal"), (self, "_control") )

        for child in self.children:
            child.activate()
        while not self.childrenDone():
            while self.dataReady("inbox"):
                d = self.recv("inbox")
                if self.mode == "split":
                    self.send(d, "outbox")

                if self.sink and self.condition(d):
                    self.send(d, "_outbox")
                elif self.mode == "route":
                    self.send(d, "outbox")

                yield 1

            while self.dataReady("_inbox"):
                d = self.recv("_inbox")
                if self.source:
                    self.send(d, "outbox")
                yield 1

            while self.dataReady("control"):
                d = self.recv("control")
                self.send(d, "signal")
                self.send(d, "_signal")
                yield 1
            self.pause()
            yield 1

    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())

