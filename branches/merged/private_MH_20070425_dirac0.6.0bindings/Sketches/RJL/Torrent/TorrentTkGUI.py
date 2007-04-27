
"""\
=================
TorrentWindow - a basic GUI for BitTorrent
=================

This component supports downloading from multiple torrents simultaneously
but no deletion or statistics other than percentage completuion so far.

How does it work?
-----------------
TorrentWindow uses Tkinter to produce a very simple GUI.
It then produces messages for and accepts messages produced by a
TorrentPatron component (also would work with TorrentClient but 
TorrentPatron is preferred, see their respective files).

Example Usage
-------------
The following setup allows torrents to be entered as HTTP URLs into the
GUI and then downloaded with progress information for each torrent.

    Graphline(
        gui=TorrentWindow(),
        httpclient=SimpleHTTPClient(),
        backend=TorrentPatron(),
        linkages = {
            ("gui", "outbox") : ("backend", "inbox"),
            ("gui", "fetchersignal") : ("httpclient", "control"),
            ("gui", "signal") : ("backend", "control"),
            ("gui", "fetcher") : ("httpclient", "inbox"),
            ("httpclient", "outbox") : ("backend", "inbox"),
            ("backend", "outbox"): ("gui", "inbox")
        }
    ).run()
"""

from Kamaelia.UI.Tk.TkWindow import TkWindow
from Axon.Ipc import producerFinished, shutdown
import Tkinter, time
from TorrentPatron import TorrentPatron
from TorrentIPC import *


class TorrentWindow(TkWindow):
    Inboxes = { 
        "inbox"   : "From TorrentPatron backend",
        "control" : "Tell me to shutdown",
    }
    Outboxes = {
        "outbox"  : "To TorrentPatron backend",
        "fetcher" : "To TorrentPatron backend via a resource fetcher, e.g. file reader or HTTP client",
        "fetchersignal" : "Shutdown resource fetcher",
        "signal" : "When I've shutdown"
    }
        
    def __init__(self):
        self.pendingtorrents = []
        self.torrents = {}
        super(TorrentWindow, self).__init__()
        
    def setupWindow(self):
        "Create the GUI controls and window for this application"
        self.entry = Tkinter.Entry(self.window)
        self.addtorrentbutton = Tkinter.Button(self.window, text="Add Torrent", command=self.addTorrent)
        self.window.title("Kamaelia BitTorrent Client")
        
        self.entry.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.addtorrentbutton.grid(row=0, column=1, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)        
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=3)
        self.window.columnconfigure(1, weight=1)

    def addTorrent(self):
        "Request the addition of a new torrent"
        torrenturl = self.entry.get()
        self.pendingtorrents.append(torrenturl.rsplit("/", 1)[-1])
        self.send(torrenturl, "fetcher") # forward on the torrent URL/path to the fetcher
        self.entry.delete(0, Tkinter.END)

    def main(self):
        while not self.isDestroyed():
            time.sleep(0.05) # reduces CPU usage but a timer component would be better
            yield 1
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(msg, "signal")
                    self.window.destroy()
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                if isinstance(msg, TIPCNewTorrentCreated):
                    torrentname = self.pendingtorrents.pop(0)
                    labeltext = Tkinter.StringVar() # allow us to change the label's text on the fly
                    newlabel = Tkinter.Label(self.window, textvariable=labeltext)                    
                    self.torrents[msg.torrentid] = (torrentname, newlabel, labeltext)
                    labeltext.set(torrentname + " - 0%")
                    
                    newlabel.grid(row=len(self.torrents), column=0, columnspan=2, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
                    self.window.rowconfigure(len(self.torrents), weight=1)
                    
                elif isinstance(msg, TIPCTorrentStartFail) or isinstance(msg, TIPCTorrentAlreadyDownloading):
                    self.pendingtorrents.pop(0) # the oldest torrent not yet started failed so remove it from the list of pending torrents
                
                elif isinstance(msg, TIPCTorrentStatusUpdate):
                    # print msg.statsdictionary.get("fractionDone","-1")
                    self.torrents[msg.torrentid][2].set(self.torrents[msg.torrentid][0] + " - " + str(int(msg.statsdictionary.get("fractionDone","0") * 100)) + "%")
            
            self.tkupdate()
        self.send(shutdown(), "signal") 
        self.send(shutdown(), "fetchersignal")
                
if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    import sys
    sys.path.append("../HTTP")

    from HTTPClient import SimpleHTTPClient
    
    Graphline(
        gui=TorrentWindow(),
        httpclient=SimpleHTTPClient(),
        backend=TorrentPatron(),
        linkages = {
            ("gui", "outbox") : ("backend", "inbox"),
            ("gui", "fetchersignal") : ("httpclient", "control"),
            ("gui", "signal") : ("backend", "control"),
            ("gui", "fetcher") : ("httpclient", "inbox"),
            ("httpclient", "outbox") : ("backend", "inbox"),
            ("backend", "outbox"): ("gui", "inbox")
        }
    ).run()

