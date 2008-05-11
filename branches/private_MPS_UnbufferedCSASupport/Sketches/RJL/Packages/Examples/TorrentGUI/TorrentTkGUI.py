#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
==============================================
Torrent Tk Window - a basic GUI for BitTorrent
==============================================

This component supports downloading from multiple torrents simultaneously
but no deletion or statistics other than percentage completion so far.

How does it work?
-----------------
TorrentTkWindow uses Tkinter to produce a very simple GUI.
It then produces messages for and accepts messages produced by a
TorrentPatron component (also would work with TorrentClient but 
TorrentPatron is preferred, see their respective files).

Example Usage
-------------
The following setup allows torrents to be entered as HTTP URLs into the
GUI and then downloaded with progress information for each torrent.

    Graphline(
        gui=TorrentTkWindow(),
        httpclient=SimpleHTTPClient(),
        backend=TorrentPatron(),
        linkages = {
            ("gui", "outbox") : ("backend", "inbox"),
            ("gui", "fetchersignal") : ("httpclient", "control"),
            ("gui", "signal") : ("backend", "control"),
            ("gui", "fetcher") : ("httpclient", "inbox"),
            ("httpclient", "outbox") : ("backend", "inbox"),
            ("backend", "outbox") : ("gui", "inbox")
        }
    ).run()
    
Detailed Explanation
--------------------
The TorrentTkGUI component accepts the following Torrent IPC messages on "inbox":

- TIPCNewTorrentCreated
- TIPCTorrentStartFail
- TIPCTorrentAlreadyDownloading
- TIPCTorrentStatusUpdate

It uses these messages to build and update a list of torrents and their
percentage completion.
See TorrentPatron, TorrentClient and TorrentIPC in
Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent
for more details on how the BitTorrent components function and the
messages they send/accept.

This component requests the addition of new torrents by sending the URL of
a .torrent file to its "fetcher" outbox, which generally will connect to
a SimpleHTTPClient or alternatively, a TriggeredFileReader.
This 'fetcher' component will then forward on the contents of the .torrent file
to a TorrentPatron (it should be connected up to do so).
"""

import Tkinter, time

from Kamaelia.UI.Tk.TkWindow import TkWindow
from Axon.Ipc import producerFinished, shutdown

from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentIPC import TIPCNewTorrentCreated, TIPCTorrentStartFail, TIPCTorrentAlreadyDownloading, TIPCTorrentStatusUpdate

class TorrentTkWindow(TkWindow):
    """Tkinter BitTorrent client GUI"""

    Inboxes = { 
        "inbox"   : "From TorrentPatron backend",
        "control" : "Tell me to shutdown",
    }
    Outboxes = {
        "outbox"  : "To TorrentPatron backend",
        "fetcher" : "To TorrentPatron backend via a resource fetcher, e.g. file reader or HTTP client",
        "fetchersignal" : "Shutdown resource fetcher",
        "signal"  : "When I've shutdown"
    }
        
    def __init__(self):
        super(TorrentTkWindow, self).__init__()
            
        # torrents that the user has requested be downloaded,
        # but which TorrentPatron has not yet confirmed
        self.pendingtorrents = []
        
        # torrents that have been started by TorrentPatron
        # (an associative array of torrentid -> (torrentname, label, labeltext) )
        self.torrents = {}

        
    def setupWindow(self):
        "Create the GUI controls and window for this application"
        # THIS FUNCTION IS CALLED BY THE PARENT CLASS - TorrentTkWindow during __init__
        
        # Create the URL entry text box
        self.entry = Tkinter.Entry(self.window)
        
        # Create a button labelled "Add Torrent" which causes self.requestNewTorrent
        # to be called when clicked (a callback function)
        self.addtorrentbutton = Tkinter.Button(self.window, text="Add Torrent", command=self.requestNewTorrent)
        
        # Set the caption of our window
        self.window.title("Kamaelia BitTorrent Client")
        
        # Layout the window like a table so it resizes
        # the widgets automatically when it resizes
        # it will look something like: (without the grid lines)
        # +---------------------------------------+--------------+
        # | ENTRY (75% width)                     | BUTTON (25%) |
        # +---------------------------------------+--------------+
        
        # set the position of the text box in the 'table'
        self.entry.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        
        # set the button of the text box in the 'table'
        self.addtorrentbutton.grid(row=0, column=1, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)        
        
        # setup the row they are both in
        self.window.rowconfigure(0, weight=1)
        
        # make the left-most column three times the width of the right-most one
        self.window.columnconfigure(0, weight=3) 
        self.window.columnconfigure(1, weight=1)

    def requestNewTorrent(self):
        "Request the addition of a new torrent"
        
        # get the contents of the text box (which should be a URL of a .torrent)
        torrenturl = self.entry.get()
        
        # add it to our list of torrents pending confirmation from Torrent Patron
        self.pendingtorrents.append(torrenturl.rsplit("/", 1)[-1])
        
        # send this the URL of this .torrent to the fetcher
        self.send(torrenturl, "fetcher")
        
        # clear the text box - make its contents ""
        self.entry.delete(0, Tkinter.END)

    def addTorrentToList(self, msg):
        "Add a new torrent to the list onscreen"
        # this torrent is the oldest one we requested that has not yet been added
        torrentname = self.pendingtorrents.pop(0)
                    
        # using a StringVar allows us to change the label's text on the fly
        labeltext = Tkinter.StringVar()

        # create a new label for this torrent
        newlabel = Tkinter.Label(self.window, textvariable=labeltext)                    
        self.torrents[msg.torrentid] = (torrentname, newlabel, labeltext)
        labeltext.set(torrentname + " - 0%")

        # setup the layout 'table' so that the label spans
        # the entire width of the window
        newlabel.grid(row=len(self.torrents), column=0, columnspan=2, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.window.rowconfigure(len(self.torrents), weight=1)
                    
    def main(self):
        while not self.isDestroyed():
            time.sleep(0.05) # reduces CPU usage but a separate timer component would be better
            yield 1
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):                    
                    # close this window, causing us to exit the main loop
                    # (it makes self.isDestroyed() == True)
                    self.window.destroy()
            
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                if isinstance(msg, TIPCNewTorrentCreated):
                    self.addTorrentToList(msg)
                    
                elif isinstance(msg, TIPCTorrentStartFail) or isinstance(msg, TIPCTorrentAlreadyDownloading):
                    # the oldest torrent not yet started failed to start so
                    # remove it from the list of pending torrents
                    print "Oops - torrent start failed!\n"
                    self.pendingtorrents.pop(0)
                
                elif isinstance(msg, TIPCTorrentStatusUpdate):
                    # change the label for that torrent to show the new percentage completion
                    # newlabelcaption = "{the torrent name} - {the percentage completion of the download}%"
                    newlabelcaption = self.torrents[msg.torrentid][0] + " - " + str(int(msg.statsdictionary.get("fractionDone","0") * 100)) + "%"
                    self.torrents[msg.torrentid][2].set(newlabelcaption)
            
            # update the screen
            self.tkupdate()
        
        # shutdown the TorrentPatron
        self.send(shutdown(), "signal")
        
        # and tell the HTTP client that we've finished which should cause
        # it to terminate gracefully, of its own accord 
        self.send(producerFinished(self), "fetchersignal")

__kamaelia_components__  = ( TorrentTkWindow, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    
    Graphline(
        gui = TorrentTkWindow(), # our GUI
        httpclient = SimpleHTTPClient(), # used to download .torrent files
        backend = TorrentPatron(), # our BitTorrent client backend
        linkages = {
            ("backend", "outbox") : ("gui", "inbox"),
            ("gui", "outbox") : ("backend", "inbox"),
            ("gui", "signal") : ("backend", "control"),
            
            ("gui", "fetchersignal") : ("httpclient", "control"),
            ("gui", "fetcher") : ("httpclient", "inbox"),
            ("httpclient", "outbox") : ("backend", "inbox"),
        }
    ).run()

    #         BASIC TOPOLOGY
    # -------------------------------
    #
    # httpclient <-- gui <--> backend
    #      \                    /
    #       '--->---->---->--->'
