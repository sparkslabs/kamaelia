# -*- coding: utf-8 -*-
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

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

import sys, time
sys.path.append("../../Util")
sys.path.append("../../HTTP")
sys.path.append("../../Torrent")

from IcecastClient import IcecastClient, IcecastDemux, IcecastStreamRemoveMetadata
from Chunkifier import Chunkifier
from ChunkDistributor import ChunkDistributor
from WholeFileWriter import WholeFileWriter
from TorrentMaker import TorrentMaker
from Kamaelia.Util.Fanout import fanout
from HTTPHelpers import HTTPMakePostRequest
from HTTPClient import SimpleHTTPClient
from TorrentPatron import TorrentPatron

from OnDemandIntrospector import OnDemandIntrospector

#UTIL
from DataSource import TriggeredSource
from LineSplit import LineSplit
from UnseenOnly import UnseenOnly
from TriggeredFileReader import TriggeredFileReader
from PureTransformer import PureTransformer
from TorrentIPC import *
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

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
                    if msg.torrentid == torrents[0][0]:
                        print msg.statsdictionary
                        if msg.statsdictionary.get("fractionDone",0) == 1:
                            self.send(torrents[0][1], "outbox")                        
                            torrents.pop(0)
            self.pause()

if __name__ == '__main__':
    partslist = "filelist.txt"
    resourcefetcher = TriggeredFileReader #SimpleHTTPClient
    
    pipeline(
        ConsoleReader(),
        OnDemandIntrospector(),
        ConsoleEchoer(),
    ).activate()
        
    pipeline(
        CheapAndCheerfulClock(30.0),
        TriggeredSource(partslist),
        resourcefetcher(),
        LineSplit(),
        UnseenOnly(),
        PureTransformer(lambda x: x or None), #eradicate blank lines
        resourcefetcher(),
        TorrentPatron(),
        StreamReconstructor(),
        ConsoleEchoer()
    ).run()
    
