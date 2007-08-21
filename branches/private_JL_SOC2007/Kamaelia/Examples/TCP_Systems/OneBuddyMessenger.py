#!/usr/bin/env python
##
## (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
## You may only modify and redistribute this under the terms of any of the
## following licenses(2): Mozilla Public License, V1.1, GNU General
## Public License, V2.0, GNU Lesser General Public License, V2.1
##
## (1) Kamaelia Contributors are listed in the AUTHORS file and at
##     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
##     not this notice.
## (2) Reproduced in the COPYING file, and at:
##     http://kamaelia.sourceforge.net/COPYING
## Under section 3.5 of the MPL, we are using this text since we deem the MPL
## notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
## notice is prohibited.
##
## Please contact us via: kamaelia-list-owner@lists.sourceforge.net
## to discuss alternative licensing.
## -------------------------------------------------------------------------
"""
=====================
One-buddy AIM Client
=====================

Allows users to instant-message one of their buddies.

Example Usage
--------------
A command-line program with the syntax "./OneBuddyMessenger [-s screeenname password] [-b buddy]"::

    def parseArgs(args):
        if "-b" in args:
            buddy = args[args.index("-b") + 1]
        else:
            buddy = "Spleak"
        if "-s" in args:
            screenname = args[args.index("-s") + 1]
            password = args[args.index("-s") + 2]
        else:
            screenname, password = "kamaelia1", "abc123"
        return screenname, password, buddy

    args = parseArgs(sys.argv[1:])
    print sys.argv
    SimpleAIMClient(*args).run()


How it works
------------
First, we define a function to turn incoming user messages into the tuple-based
commands that AIMHarness understands. Then we define another function to put
tuple output from AIMHarness into a more user-friendly form. Then we run the output
from a sensible user input component (in this case Kamaelia.UI.Pygame.Text.Textbox)
through the first function and give it to AIMHarness. We put all the output from
AIMHarness through the second function and give it to a user output component
(Kamaelia.UI.Pygame.Text.TextDisplayer). 

"""

from Kamaelia.Protocol.AIM.AIMHarness import AIMHarness
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

def sendTo(recipient, text):
    return ("message", recipient, text)

def outformat(data, buddyname):
    buddyname = buddyname.lower()
    if data[0] == "buddy online" and data[1]["name"].lower() ==  buddyname:
        return "%s is online" % data[1]["name"]
    elif data[0] == "message" and data[1].lower() == buddyname:
        return "%s: %s" % (data[1], data[2])
    elif data[0] == "error":
        return ": ".join(data)

def SimpleAIMClient(screenname, password, buddyname):
    Pipeline(Textbox(position=(0, 400)),
             PureTransformer(lambda text: sendTo(buddyname, text)),
             AIMHarness(screenname, password),
             PureTransformer(lambda tup: outformat(tup, buddyname)),
             TextDisplayer()
             ).run()

if __name__ == '__main__':
    import sys

    def parseArgs(args):
        if "-b" in args:
            buddy = args[args.index("-b") + 1]
        else:
            buddy = "Spleak"
        if "-s" in args:
            screenname = args[args.index("-s") + 1]
            password = args[args.index("-s") + 2]
        else:
            screenname, password = "kamaelia1", "abc123"
        return screenname, password, buddy

    args = parseArgs(sys.argv[1:])
    print sys.argv
    SimpleAIMClient(*args).run()
