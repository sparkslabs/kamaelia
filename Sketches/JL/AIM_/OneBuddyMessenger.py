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

#the locations of AIMHarness and IRC.Text may change.

from AIMHarness import AIMHarness
from IRC.Text import TextDisplayer, Textbox
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

def sendTo(recipient, text):
    return ("message", recipient, text)

def outformat(data, buddyname):
    if data[0] == "buddy online" and data[1]["name"] ==  buddyname:
        return "%s is online" % buddyname
    elif data[0] == "message" and data[1] == buddyname:
        return "%s: %s" % (buddyname, data[2])
    elif data[0] == "error":
        ": ".join(data)

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
