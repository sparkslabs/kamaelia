#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
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
## -------------------------------------------------------------------------
"""
=====================
One-buddy AIM Client
=====================

Allows users to instant-message one of their buddies.

Example Usage
--------------
A command-line program with the syntax "./OneBuddyMessenger [-s screeenname password] [-b buddy]"::

This version does not use pygame, nor have default arguments.

How it works
------------
First, we define a function to turn incoming user messages into the tuple-based
commands that AIMHarness understands. Then we define another function to put
tuple output from AIMHarness into a more user-friendly form. Then we run the output
from a sensible user input component (in this case Kamaelia.Util.Console.ConsoleReader)
through the first function and give it to AIMHarness. We put all the output from
AIMHarness through the second function and give it to a user output component
(Kamaelia.Util.Console.ConsoleEchoer). 

"""

from Kamaelia.Protocol.AIM.AIMHarness import AIMHarness
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
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
    Pipeline(ConsoleReader(),
             PureTransformer(lambda X: X[:-1]),
             PureTransformer(lambda text: sendTo(buddyname, text)),
             AIMHarness(screenname, password),
             PureTransformer(lambda tup: outformat(tup, buddyname)),
             ConsoleEchoer(),
             ).run()

if __name__ == '__main__':
    import sys
    def usage():
       print sys.argv[0], "-s [username] [password] -b [buddy]"

    def parseArgs(args):
        if "-b" in args:
            buddy = args[args.index("-b") + 1]
        else:
            usage()
            sys.exit(0)

        if "-s" in args:
            screenname = args[args.index("-s") + 1]
            password = args[args.index("-s") + 2]
        else:
            usage()
            sys.exit(0)
        return screenname, password, buddy

    args = parseArgs(sys.argv[1:])
    
    print sys.argv
    SimpleAIMClient(*args).run()
