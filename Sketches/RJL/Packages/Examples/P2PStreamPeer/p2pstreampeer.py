#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Peer-to-Peer Streaming System (client part)
===========================================
This example demonstrates the use of BitTorrent and HTTP to download, share
reconstruct a data stream in real-time.
It expects a webserver hosting a folder that contains:

- meta.txt (a file containing the number of torrents in the stream 
            so far as a decimal, ASCII string)
            
- 1.torrent
- 2.torrent
-    ...
- 100.torrent (if meta.txt contained "100")

Only this metainfo is downloaded using HTTP. The stream itself is downloaded
(and uploaded to other downloaders) using BitTorrent.
Other users must upload the stream's chunks using BitTorrent for this demo
to work.
To listen to/view the stream, just point your favourite media player
(say, XMMS) at the reconstructed file after it's been downloading for a minute
or so.
"""

import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Fanout import fanout
from Kamaelia.File.Writing import SimpleFileWriter

from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.IcecastClient import IcecastClient, IcecastDemux, IcecastStreamRemoveMetadata
from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPHelpers import HTTPMakePostRequest

from Kamaelia.Community.RJL.Kamaelia.File.WholeFileWriter import WholeFileWriter
from Kamaelia.Community.RJL.Kamaelia.File.TriggeredFileReader import TriggeredFileReader

from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentMaker import TorrentMaker
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentIPC import *

from Kamaelia.Community.RJL.Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Community.RJL.Kamaelia.Util.DataSource import TriggeredSource
from Kamaelia.Community.RJL.Kamaelia.Util.UnseenOnly import UnseenOnly
from Kamaelia.Community.RJL.Kamaelia.Util.LineSplit import LineSplit


class CheapAndCheerfulClock(threadedcomponent):
    def __init__(self, interval):
        super(CheapAndCheerfulClock, self).__init__()
        self.interval = interval

    def main(self):
        while 1:
            self.send(True, "outbox")
            time.sleep(self.interval)


class StreamReconstructor(component):
    def main(self):
        torrents = []
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                #print msg
                if isinstance(msg, TIPCNewTorrentCreated):
                    torrents.append([msg.torrentid, msg.savefolder])
                    
                elif isinstance(msg, TIPCTorrentStatusUpdate):
                    print msg.torrentid
                    if len(torrents) > 0 and msg.torrentid == torrents[0][0]:
                        print msg.statsdictionary
                        if msg.statsdictionary.get("fractionDone",0) == 1:
                            self.send(torrents[0][1], "outbox")                        
                            torrents.pop(0)
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdown) or isinstance(msg, producerFinished):
                    return
            
            self.pause()

class PartsFilenameGenerator(component):
    def __init__(self, prefix, suffix)
        self.prefix = prefix
        self.suffix = suffix
        super(self, PartsFilenameGenerator).__init__()
        
    def main(self):
        highestseensofar = 0
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = int(self.recv("inbox"))
                
                while highestsofar < msg:
                    highestsofar += 1
                    self.send(self.prefix + str(highestsofar) + self.suffix, "outbox")
            
            while self.dataReady("control"):
                msg = self.recv("control"):
                if isinstance(msg, shutdown) or isinstance(msg, producerFinished):
                    return
            
            self.pause()

def P2PStreamer(torrentsfolder, metafilename = "meta.txt", resourcefetcher = SimpleHTTPClient):
    """\
    Arguments:
    - torrentsfolder, e.g. "http://my.server.example.org/radioFoo/"
    - metafilename - the name of the file in torrentsfolder that gives P2P stream metainfo, e.g. "meta.php"
    - resourcefetcher - component class used to resolve URLs and fetch their associated file data
    """
    
    streamer = pipeline(
        CheapAndCheerfulClock(60.0),
        TriggeredSource(torrentsfolder  + metafilename),
        resourcefetcher(),
        PartsFilenameGenerator(torrentsfolder, ".torrent"),
        ConsoleEchoer(forwarder=True),
        resourcefetcher(),
        TorrentPatron(),
        StreamReconstructor(),
        TriggeredFileReader(),
    )
    return streamer
    
if __name__ == '__main__':
    torrentsfolder = raw_input("P2P-stream meta folder (URL): ") # e.g. "http://my.server.example.org/radioFoo/"
    saveas = raw_input("Save stream as: ") # e.g. "myreconstructedstream.mp3"
    pipeline(
        streamer = P2PStreamer(torrentsfolder),
        SimpleFileWriter(saveas)
    ).run()
    
