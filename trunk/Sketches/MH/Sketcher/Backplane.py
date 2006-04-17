#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# MPS's experimental backplane code
import Axon
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT


class Backplane(Axon.Component.component):
    def __init__(self, name):
        super(Backplane,self).__init__()
        assert name == str(name)
        self.name = name
        self.splitter = Splitter().activate()

        splitter = self.splitter
        cat = CAT.getcat()
        try:
            cat.registerService("Backplane_I_"+self.name, splitter, "inbox")
            cat.registerService("Backplane_O_"+self.name, splitter, "configuration")
        except Axon.AxonExceptions.ServiceAlreadyExists, e:
            print "***************************** ERROR *****************************"
            print "An attempt to make a second backplane with the same name happened."
            print "This is incorrect usage."
            print 
            traceback.print_exc(3)
            print "***************************** ERROR *****************************"


            raise e
    def main(self):
        while 1:
            self.pause()
            yield 1


class publishTo(Axon.Component.component):
    def __init__(self, destination):
        super(publishTo, self).__init__()
        self.destination = destination
    def main(self):
        cat = CAT.getcat()
        service = cat.retrieveService("Backplane_I_"+self.destination)
        self.link((self,"inbox"), service, passthrough=1)
        while 1:
            self.pause()
            yield 1            
            
            
class subscribeTo(Axon.Component.component):
    def __init__(self, source):
        super(subscribeTo, self).__init__()
        self.source = source
    def main(self):
        cat = CAT.getcat()
        splitter,configbox = cat.retrieveService("Backplane_O_"+self.source)
        Plug(splitter, self).activate()
        while 1:
            while self.dataReady("inbox"):
                d = self.recv("inbox")
                self.send(d, "outbox")
            yield 1            
