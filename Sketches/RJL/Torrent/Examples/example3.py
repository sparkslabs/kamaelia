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

import sys
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

from PureTransformer import PureTransformer

from OnDemandIntrospector import OnDemandIntrospector
from Kamaelia.File.Writing import SimpleFileWriter

if __name__ == '__main__':
    pipeline(
        ConsoleReader(),
        OnDemandIntrospector(),
        ConsoleEchoer(),
    ).activate()
    Graphline(
        streamin = pipeline(
            IcecastClient("http://127.0.0.1:1234/"), # a stream's address
            IcecastDemux(),
            IcecastStreamRemoveMetadata(),
            Chunkifier(500000),
            ChunkDistributor("./"),
            WholeFileWriter(),
            TorrentMaker("http://192.168.1.5:6969/announce"),
        ),
        
        split = fanout(["toMetaUploader", "toSharer"]),
        
        fileupload = pipeline(
            ChunkDistributor("./torrents/", ".torrent"),
            WholeFileWriter(),
            PureTransformer(lambda x : x + "\n"),
            SimpleFileWriter("filelist.txt")
        ),

        #WholeFileWriter()
        #HTTPMakePostRequest("http://192.168.1.15/torrentupload.php"),
        #SimpleHTTPClient()
        
        # uploader still to write
        bt = TorrentPatron(),
        linkages = {
            ("streamin", "outbox") : ("split", "inbox"),
            ("split", "toMetaUploader") : ("fileupload", "inbox"),
            ("split", "toSharer") : ("bt", "inbox"),            
            #("split","toMetaUploader") : ("whatever","inbox"),
        }
    ).run()
    
