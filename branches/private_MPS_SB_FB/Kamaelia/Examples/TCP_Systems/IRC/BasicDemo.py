#! /usr/bin/env python
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

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

from Kamaelia.Support.Protocol.IRC import informat, outformat
from Kamaelia.Protocol.IRC.IRCClient import SimpleIRCClientPrefab
from Kamaelia.Util.PureTransformer import PureTransformer

print "This is one of the simplest possible demos for the IRC Code"
print
print "As a result, you need to type"
print "          /nick yournickname"
print
print "followed by "
print
print "          /user arg1 arg2 arg3 arg4"
print
print "really fast here. You'll then need to join a channel, using something like:"
print "          /join #somechannel"
print
print
print "For example"
print 
print "/nick basicdemokbot"
print "/user aNickName irc.freenode.net thwackety.plus.com michael"
print "/join #kamaeliatest"
print 
print "yes, this isn't expected to be a useful piece of software, it's"
print "more a demo of how to use the pieces together"
print
print "when you're ready, press return to connect :-)"

_ = raw_input() # Yes, we throw it away - we're just using this to pause :-)

Pipeline(
    ConsoleReader(),
    PureTransformer(informat),
    SimpleIRCClientPrefab(),
    PureTransformer(outformat),
    ConsoleEchoer()
).run()

