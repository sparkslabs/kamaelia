#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
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
                print msg
                if isinstance(msg, TIPCNewTorrentCreated):
                    torrents.append([msg.torrentid, msg.savefolder])
                    
                elif isinstance(msg, TIPCTorrentStatusUpdate):
                    print msg.torrentid
                    if len(torrents) > 0 and msg.torrentid == torrents[0][0]:
                        print msg.statsdictionary
                        if msg.statsdictionary.get("fractionDone",0) == 1:
                            self.send(torrents[0][1], "outbox")                        
                            torrents.pop(0)
            self.pause()
			
if __name__ == '__main__':
    partslist = "http://ronline.no-ip.info/torrentlist.txt"
    torrenturlsuffix = "http://ronline.no-ip.info/"
    resourcefetcher = SimpleHTTPClient #SimpleHTTPClient
    
    pipeline(
        CheapAndCheerfulClock(30.0),
        TriggeredSource(partslist),
        resourcefetcher(),
        LineSplit(),
        UnseenOnly(),
        PureTransformer(lambda x: x or None), #eradicate blank lines
        PureTransformer(lambda x: torrenturlsuffix + x),
        #ConsoleEchoer(forwarder=True),
        resourcefetcher(),
        TorrentPatron(),
        StreamReconstructor(),
        TriggeredFileReader(),
        SimpleFileWriter("myreconstructedstream.mp3")
    ).run()
    
