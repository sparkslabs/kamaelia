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
Peer-to-Peer Streaming System (server part)
===========================================
This example demonstrates the use of BitTorrent and HTTP to distribute
a data stream in real-time.
It expects a webserver hosting a script which saves data POST'd to it
as N.torrent where N is the number of POST requests it has seen before
this one + 1. This script should also write this value N as a decimal,
ASCII string to a file meta.txt in the same directory also available
from the webserver using HTTP.

i.e. the script should produce:
- meta.txt (a file containing the number of torrents in the stream 
            so far as a decimal, ASCII string)
            
- 1.torrent
- 2.torrent
-    ...
- 100.torrent (if meta.txt contained "100")

Only this metainfo is downloaded using HTTP. The stream itself is transmitted
using the BitTorrent protocol.
"""

from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Fanout import fanout

from Kamaelia.Community.RJL.Kamaelia.Util.Chunkifier import Chunkifier
from Kamaelia.Community.RJL.Kamaelia.Util.ChunkNamer import ChunkNamer
from Kamaelia.Community.RJL.Kamaelia.File.WholeFileWriter import WholeFileWriter

from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentMaker import TorrentMaker
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron

from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.IcecastClient import IcecastClient, IcecastDemux, IcecastStreamRemoveMetadata
from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPHelpers import HTTPMakePostRequest
from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient

from Kamaelia.Community.RJL.Kamaelia.Util.PureTransformer import PureTransformer

if __name__ == '__main__':
    streamurl = raw_input("Stream URL: ") # e.g. "http://a.stream.url.example.com:1234/"
    trackerannounceurl = raw_input("Tracker Announce URL: ") # e.g. "http://192.168.1.5:6969/announce"
    trackerpostuploader = raw_input("Tracker Upload Script: ") # e.g. "http://192.168.1.5/torrentupload.php"
    
    chunksize = 2**22 # 4 megabytes
    
    Graphline(
        streamin = pipeline(
            IcecastClient(streamurl), # a stream's address
            IcecastDemux(),
            IcecastStreamRemoveMetadata(),
            Chunkifier(chunksize),
            ChunkNamer("./"),
            WholeFileWriter(),
            TorrentMaker(trackerannounceurl),
        ),
        
        split = fanout(["toMetaUploader", "toSharer"]),
        
        fileupload = pipeline(
            HTTPMakePostRequest(trackerpostuploader),
            SimpleHTTPClient()
        ),

        bt = TorrentPatron(),
        linkages = {
            ("streamin", "outbox") : ("split", "inbox"),
            ("split", "toMetaUploader") : ("fileupload", "inbox"),
            ("split", "toSharer") : ("bt", "inbox"),            
        }
    ).run()
    
