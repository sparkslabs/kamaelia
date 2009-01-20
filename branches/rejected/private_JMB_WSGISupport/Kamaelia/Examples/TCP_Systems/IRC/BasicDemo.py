#! /usr/bin/env python
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

