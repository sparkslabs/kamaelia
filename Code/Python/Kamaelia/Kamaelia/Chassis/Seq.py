#!/usr/bin/env python
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
"""\
================================================
Run components one after the other (in sequence)
================================================

A Seq component runs components one after the other in sequence, waiting until
one terminates before starting the next.

Strings can also be put in the sequence. They'll be printed to the console



Example Usage
-------------

Run several OneShot components running one after the other::

    Pipeline( Seq( "BEGIN SEQUENCE",
                   OneShot("Hello\\n"),
                   OneShot("Doctor\\n"),
                   OneShot("Name\\n"),
                   OneShot("Continue\\n"),
                   OneShot("Yesterday\\n"),
                   OneShot("Tomorrow\\n"),
                   "END SEQUENCE",
                 ),
              ConsoleEchoer(),
            ).run()

Running this generates the following output::

    BEGIN SEQUENCE
    Hello
    Doctor
    Name
    Continue
    Yesterday
    Tomorrow
    END SEQUENCE



Behaviour
---------

Each component in the sequence is activated as a child component and is wired up
so that the "inbox" inbox and "outbox" outbox are forwarded to the "inbox"
inbox and "outbox" outbox of the Seq component itself.

When the child component terminates it is replaced with the next in the
sequence.

If a string is listed instead of a component then it is printed on the console
and Seq immediately moves onto the next in the sequence.

Any messages sent out of the child component's "signal" outbox are dropped - 
this is so that if you Pipeline a Seq component to another, it does not cause it
to terminate when the Seq component switches to a new child.

This component ignores any messages sent to its "control" inbox.

When the end of the sequence is reached, a producerFinished() message is sent
out of the "signal" outbox and the component terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess



class Seq(component):
    """\
    Seq(\*sequence) -> new Seq component.
    
    Runs a set of components in sequence, one after the other. Their "inbox"
    inbox and "outbox" outbox are forwarded to the "inbox" inbox and "outbox"
    outbox of the Seq component.
    
    Keyword arguments:
    
    - \*sequence  -- Components that will be run, in sequence. Can also include strings that will be output to the console.
    """

    def __init__(self, *sequence):
        super(Seq,self).__init__()
        self.sequence = sequence

    def main(self):
        for item in self.sequence:
            
            if isinstance(item,str):
                print item
                continue
            
            comp = item

            self.addChildren(comp)
            comp.activate()

            linkages = [
                self.link((comp,"outbox"),(self,"outbox"),passthrough=2),
                self.link((self,"inbox"),(comp,"inbox"),passthrough=1),
                # not linking signal-control, since we don't want downstream
                # component to terminate prematurely
            ]

            while not self.childrenDone():
                self.pause()
                yield 1

            for linkage in linkages:
                self.unlink(thelinkage=linkage)

        self.send(producerFinished(self),"signal")


    def childrenDone(self):
        """\
        Unplugs any children that have terminated, and returns true if there are no
        running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())


__kamaelia_components__ = ( Seq, )


if __name__=="__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.OneShot import OneShot
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline( Seq( "BEGIN SEQUENCE",
                   OneShot("Hello\n"),
                   OneShot("Doctor\n"),
                   OneShot("Name\n"),
                   OneShot("Continue\n"),
                   OneShot("Yesterday\n"),
                   OneShot("Tomorrow\n"),
                   "END SEQUENCE",
                 ),
              ConsoleEchoer(),
            ).run()

