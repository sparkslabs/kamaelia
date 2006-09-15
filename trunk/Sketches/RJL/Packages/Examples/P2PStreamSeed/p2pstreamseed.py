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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
===========================================
Peer-to-Peer Streaming System (server part)
===========================================
This example demonstrates the use of BitTorrent and HTTP to distribute
a data stream in real-time. Specifically, this example redistributes
a SHOUTcast or Icecast audio/video stream of the user's choice.
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

Usage
==============
- Choose an Icecast/SHOUTcast stream that you are legally permitted
  to redistribute and allow others to redistribute.

- Setup a BitTorrent tracker.

- Setup an HTTP server to host the .torrent files.

- Put an upload script on the HTTP server to save .torrent files sent to it.
  (e.g. the PHP script torrentupload.php in this directory)
  
- Run this example.

- Enter the URL of the stream.

- Enter the 'announce' URL of your BitTorrent tracker, which is typically
  "http://yourtrackerhostname:trackerportnumber/announce".
  e.g. "http://www.example.org:6969/announce"
  
- Enter the URL of your upload script.

- Give others the URL of folder on your webserver to which .torrent files
  are saved.
  
- Have them run the example in ../P2PStreamPeer/ on their computer.

- Have them open "myreconstructedstream.mp3" with an MP3 player program.

- They will download and reshare (upload) your stream automatically.

Note: A sensible bitrate for the stream is just under the average upload speed
in the swarm (i.e. of you and all peers downloading your stream).
Typically for broadband this would be 180 kilobits/s = 22.5 kilobytes/s
Your upload speed MUST be larger than this.
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

if __name__ == '__main__':

    # The URL of an Icecast/SHOUTcast stream
    # e.g. "http://a.stream.url.example.com:1234/"
    streamurl = raw_input("Stream URL: ")
    
    # The 'announce' URL of the BitTorrent tracker to use
    # e.g. "http://192.168.1.5:6969/announce"
    trackerannounceurl = raw_input("Tracker Announce URL: ")
    
    # The URL of the .torrent upload script mentioned at the top of this fle
    # e.g. "http://192.168.1.5/torrentupload.php"
    trackerpostuploader = raw_input("Tracker Upload Script: ")
    
    chunksize = 4 * 1024 * 1024 # 4194304 bytes = 4 megabytes - a sensible size
    
    Graphline(
        # Streamin pulls in a stream from an SHOUTcast/Icecast server
        # splits it into chunks of a fixed size, writes these chunks
        # to disk, creates a .torrent (BitTorrent metadata) file for
        # each chunk and then shares the chunks with clients using
        # the BitTorrent protocol (it 'seeds' each chunk)
        streamin = pipeline(
            # Icecast client that connects to a stream and outputs the raw stream data
            IcecastClient(streamurl),
            
            # Split the raw data into audio/visual data and stream metadata
            # example of such metadata would be song title and artist name
            IcecastDemux(),
            
            # Strip the metadata from the stream outputting only the a/v data
            IcecastStreamRemoveMetadata(),
            
            # Split the data stream into discrete chunks of a fixed size
            Chunkifier(chunksize),
            
            # Give each chunk a distinct filename to save it under
            # in the current directory ("./" means this directory)
            # (e.g. the first chunk's filename would be "./chunk1"
            # and the second "./chunk2" etc.)
            ChunkNamer("./"),
            
            # Write each chunk to disc under this name
            WholeFileWriter(),
            
            # Make a .torrent (BitTorrent metadata) file from each chunk file
            TorrentMaker(trackerannounceurl),
        ),
        
        # send the .torrent file to the website that will host them and to
        # a TorrentPatron which will then upload the associated chunks
        # to peers (users that want to download the stream)
        split = fanout(["toHTTP-POSTer", "toTorrentPatron"]),
        
        # fileupload uploads each message it receives to a script on a webserver.
        fileupload = pipeline(
            # convert messages received to HTTP POST requests
            # for the URL trackerpostuploader
            # (with the contents of the message as the payload/request body)
            HTTPMakePostRequest(trackerpostuploader),
            
            # SimpleHTTPClient then makes these requests
            # (connecting to the server given in the URL and sending the
            # POST request in an HTTP request format)
            # the result of which is (assuming a suitable upload script on the
            # webserver) .torrent files sent to this pipeline as messages
            # are uploaded to the webserver
            SimpleHTTPClient()
        ),

        # TorrentPatron is a BitTorrent client which will automatically
        # upload chunks of the stream to users that request them
        bittorrentpatron = TorrentPatron(),
        
        linkages = {
            ("streamin", "outbox")       : ("split", "inbox"),
            ("split", "toHTTP-POSTer")   : ("fileupload", "inbox"),
            ("split", "toTorrentPatron") : ("bittorrentpatron", "inbox"),            
        }
    ).run()
    
    #         BASIC TOPOLOGY
    # -------------------------------
    #
    # streamin --->split----> fileupload
    #                 \
    #                  '----> bittorrentpatron
