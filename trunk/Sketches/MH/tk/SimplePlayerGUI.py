#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#
# Simple control window for a looping audio player

from Axon.Ipc import producerFinished, shutdownMicroprocess

import Tkinter
from Kamaelia.UI.Tk.TkWindow import TkWindow

class ControlWindow(TkWindow):
    """A simple audio player control window.

       Clicking "PLAY" emits a filename on the outbox
       Closing the window doesn't immediately close it, but sends a shutdownMicroprocess()
       message out of the outbox.
       The window will actually close when this component receives a shutdownMicroproces()
       message itself.
    """

    Inboxes = { "inbox":"",
                "control":""
              }
              
    Outboxes = { "outbox":"filenames to read",
                 "signal":""
               }

    def __init__(self):
        super(ControlWindow, self).__init__()

    # default main() waits for shutdownMicroprocess() and then destroys this component
        
    def setupWindow(self):
        self.frame = Tkinter.Frame(self.window)

        self.window.title("Kamaelia Ogg Player")
        
        self.frame.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)

        self.label = Tkinter.Label(self.frame, text="Simple player.Click to play")
        self.label.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        
        self.playbutton = Tkinter.Button(self.frame, text="PLAY!", command=lambda: self.playAudio() )
        self.playbutton.grid(row=1, column=0, padx=4, pady=4)

        self.window.protocol("WM_DELETE_WINDOW", self.handleCloseWindowRequest )

    def playAudio(self):
        self.send( "/opt/kde3/share/sounds/KDE_Startup_2.ogg", "outbox")

    def destroyHandler(self,event):
        if str(event.widget) == str(self.window):
            self.send( shutdownMicroprocess(self), "signal")

    def handleCloseWindowRequest(self):
        # we won't close the window, we'll send on a shutdown message to children
        self.send( shutdownMicroprocess(self), "signal")
        # we'll destroy outselves when we receive a shutdown message ourselves
        self.label["text"] = "Shutting down..."
        self.playbutton.destroy()

        
if __name__ == "__main__":
    from Axon.Scheduler import scheduler

    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
    from Kamaelia.File.Reading import FixedRateControlledReusableFileReader
    
    # make pipeline, but make the signal->control path loop round, so a shutdownMicroprocess()
    # message sent by ControlWindow will eventually get back to ControlWindow()
    p=pipeline( ControlWindow(),
                FixedRateControlledReusableFileReader( readmode="bytes",
                                                       rate=128000/8,
                                                       chunksize=1024 ),
                VorbisDecode(),
                AOAudioPlaybackAdaptor()
              ).activate()
    p.link( (p,"signal"), (p,"control") )
    
    if 0:
        from Kamaelia.Internet.TCPClient import TCPClient
        from Kamaelia.Util.Introspector import Introspector
        pipeline(Introspector(), TCPClient("127.0.0.1",1500)).activate()
    
    scheduler.run.runThreads(slowmo=0)
