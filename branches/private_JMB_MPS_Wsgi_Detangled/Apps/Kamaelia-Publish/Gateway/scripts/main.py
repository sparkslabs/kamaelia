#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: JMB

from Kamaelia.Apps.Web_common.ConfigFile import DictFormatter, ParseConfigFile
from Kamaelia.Apps.Web_common.Structs import ConfigObject
from Kamaelia.Apps.Web_common.ServerSetup import initializeLogger

from jabber import constructXMPPClient
from http import constructHTTPServer
from Kamaelia.Apps.Publish.Gateway.JIDLookup import connectToDB
import optparse

def main():
    ConfigDict = ParseConfigFile('~/kpgate.ini', DictFormatter())
    options = parseCmdOpts()
    #print options
    
    Config = ConfigObject(ConfigDict, options)
    initializeLogger()
    
    server = constructHTTPServer(Config)    
    xmpp = constructXMPPClient(Config)
    connectToDB(Config)
    
    xmpp.activate()
    server.run()
    
def parseCmdOpts():
    parser = optparse.OptionParser()
    parser.add_option('-x', '--xmpp-verbose', dest='xmpp_verbose', action='store_true',
                      help='Use this option to view each incoming and outgoing XMPP message')
    (options, args) = parser.parse_args()
    return options
