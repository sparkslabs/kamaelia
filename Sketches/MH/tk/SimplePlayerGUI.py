#!/usr/bin/python
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
# Simple control window for a looping audio player

from Axon.Ipc import producerFinished, shutdownMicroprocess

import Tkinter
from TkInterComponents import TkWindow

import sys ; sys.path.append("../filereading")
from ReadMultiFileAdapter import FixedRateReadMultiFileAdapter



class ControlWindow(TkWindow):
    """
    """

    Inboxes = { "inbox":"",
                "control":""
              }
              
    Outboxes = { "outbox":"filenames to read",
                 "signal":""
               }

    def __init__(self):
        super(ControlWindow, self).__init__()

    def setupWindow(self):
        self.frame = Tkinter.Frame(self.window)

        self.window.title("Kamaelia Ogg Player")
        
        self.frame.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)

        self.label = Tkinter.Label(self.frame, text="Simple player.Click to play")
        self.label.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        
        self.playbutton = Tkinter.Button(self.frame, text="PLAY!", command=lambda: self.playAudio() )
        self.playbutton.grid(row=1, column=0, padx=4, pady=4)


    def playAudio(self):
        self.send( "/opt/kde3/share/apps/khangman/sounds/new_game.ogg", "outbox")

    def destroyHandler(self,event):
        if str(event.widget) == str(self.window):
            self.send( shutdownMicroprocess(self), "signal")

            

if __name__ == "__main__":
    from Axon.Scheduler import scheduler

    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
    
    pipeline( ControlWindow(),
              FixedRateReadMultiFileAdapter( readmode="bytes", rate=128000/8, chunksize=1024 ),
              VorbisDecode(),
              AOAudioPlaybackAdaptor()
            ).activate()
    
    
    scheduler.run.runThreads(slowmo=0)
