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
"""\
=====================
General Interactor
=====================
Methods to be overridden:
    handleEvents()
    setup()
    frame()
"""


import pygame
from pygame.locals import *
from OpenGLDisplay import *

import Axon

class Interactor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {
        "inbox"      : "not used",
        "control"    : "ignored",
        "events"     : "Input events",
        "callback"   : "for the response after a displayrequest",
    }
    
    Outboxes = {
        "outbox"        : "used for sending relative tranlational movement",
        "display_signal": "Outbox used for communicating to the display surface",
    }
    
    def __init__(self, **argd):
        super(Interactor, self).__init__()

        # get display service
        displayservice = OpenGLDisplay.getDisplayService()
        # link display_signal to displayservice
        self.link((self,"display_signal"), displayservice)
       
        self.victim = argd.get("victim")
        
        self.nolink = argd.get("nolink", False)
                    
            
    def main(self):
        # create eventspy request
        self.eventspyrequest = { "EVENTSPYREQUEST" : True,
                                                   "objectid" : id(self),
                                                   "victim": id(self.victim),
                                                   "callback" : (self,"callback"),
                                                   "events" : (self, "events")  }
    
        # send display request
        self.send(self.eventspyrequest, "display_signal")

        # setup function from derived objects
        self.setup()        

        # wait for response on displayrequest
        while not self.dataReady("callback"): yield 1
        self.identifier = self.recv("callback")

        while 1:
            yield 1
            self.handleEvents()
            # frame function from derived objects
            self.frame()

    ##
    # Methods to be used by derived objects
    ##

    def addListenEvents(self, events):
        for event in events:
            self.send({"ADDLISTENEVENT":event, "objectid":id(self)}, "display_signal")

    
    def removeListenEvents(self, events):
        for event in events:
            self.send({"REMOVELISTENEVENT":event, "objectid":id(self)}, "display_signal")


    ##
    # Method stubs to be overridden by derived objects
    ##
    def makeInteractorLinkages(self):
        """ Method stub """
        pass


    def handleEvents(self):
        """ Method stub """
        pass        
    
    def setup(self):
        """ Method stub """
        pass

    def frame(self):
        """ Method stub """
        pass

