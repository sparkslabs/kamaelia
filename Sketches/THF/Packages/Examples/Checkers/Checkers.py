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
Checkers game component
=====================
"""


import Axon

from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent

from CheckersBoard import CheckersBoard
from CheckersPiece import CheckersPiece
from CheckersInteractor import CheckersInteractor

class Checkers(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {
       "inbox": "not used",
       "control": "ignored",
    }
    
    Outboxes = {
        "outbox": "not used",
    }

    def initialiseComponent(self):
        # initialise display
        display = OpenGLDisplay(viewerposition=(0,-10,0), lookat=(0,0,-15), limit_fps=100).activate()
        OpenGLDisplay.setDisplayService(display)
    
        # create board
        self.boardvis = CheckersBoard(position=(0,0,-15)).activate()
        
        self.interactor_comms = {}

        self.board = {}                
        for i in range(8):
            self.board[i] = {}
            for j in range(8):
                self.board[i][j] = None
        
        # create black pieces
        self.blackPieces = []
        self.blackInteractors = []
        for i in range(8):
            for j in range(3):
                if (i+j) %2 == 0:
                    x = float(i)-3.5
                    y = float(j)-3.5
                    piece = CheckersPiece(position=(x, y, -15), colour=(0.6,0,0)).activate()
                    self.blackPieces.append(piece)

                    interactor = CheckersInteractor(target=piece, colour='B').activate()
                    self.blackInteractors.append(interactor)

                    intcomms = self.addOutbox("interactor_comms")
                    self.interactor_comms[id(interactor)] = intcomms
                    self.link( (self, intcomms), (interactor, "inbox"))
                    self.link( (interactor, "outbox"), (self, "inbox"))
                    
                    self.board[i][j] = 'B'

                    
        # create white pieces
        self.whitePieces = []
        self.whiteInteractors = []
        for i in range(8):
            for j in range(5,8):
                if (i+j) %2 == 0:
                    x = float(i)-3.5
                    y = float(j)-3.5
                    piece = CheckersPiece(position=(x, y, -15), colour=(0,0,0.6)).activate()
                    self.whitePieces.append(piece)

                    interactor = CheckersInteractor(target=piece, colour='B').activate()
                    self.whiteInteractors.append(interactor)

                    intcomms = self.addOutbox("interactor_comms")
                    self.interactor_comms[id(interactor)] = intcomms
                    self.link( (self, intcomms), (interactor, "inbox"))
                    self.link( (interactor, "outbox"), (self, "inbox"))

                    self.board[i][j] = 'W'

        return 1
        
        
    def mainBody(self):
        while self.dataReady("inbox"):
            msg = self.recv("inbox")
            
            if msg.get("PLACEMENT", None):
                objectid = msg.get("objectid")
                fr = msg.get("from")
                to = msg.get("to")
                colour = msg.get("colour")
                
                if (to[0]<0 or to[0]>7 or to[1]<0 or to[1]>7 or to[0] + to[1]) % 2 != 0 or self.board[to[0]][to[1]] is not None:
                    self.send("INVALID", self.interactor_comms[objectid])
                else:
                    self.board[fr[0]][fr[1]] = None
                    self.board[to[0]][to[1]] = colour
                    self.send("ACK", self.interactor_comms[objectid])
                    
        return 1
        
if __name__=='__main__': 
    Checkers().activate()
    Axon.Scheduler.scheduler.run.runThreads()
