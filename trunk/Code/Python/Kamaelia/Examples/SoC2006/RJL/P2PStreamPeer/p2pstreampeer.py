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
===========================================
Peer-to-Peer Streaming System (client part)
===========================================
This example demonstrates the use of BitTorrent and HTTP to download, share
reconstruct a data stream in real-time.
It expects a webserver hosting a folder that contains:

- meta.txt (a file containing the number of chunks/torrents in the stream 
            so far as a decimal, ASCII string)
            
- 1.torrent
- 2.torrent
-    ...
- 123.torrent (if meta.txt contained "123")

Only this metainfo is downloaded using HTTP. The stream itself is downloaded
(and uploaded to other downloaders) using BitTorrent.
Other users must upload the stream's chunks using BitTorrent for this demo
to work.
To listen to/view the stream, just point your favourite media player
(say, XMMS) at the reconstructed file after it's been downloading for a minute
or so.
"""

import time

from Axon.Component import component

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter

from Kamaelia.File.TriggeredFileReader import TriggeredFileReader

from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient

from Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.Protocol.Torrent.TorrentIPC import TIPCNewTorrentCreated, TIPCTorrentStatusUpdate

from Kamaelia.Util.Clock import CheapAndCheerfulClock
from Kamaelia.Util.DataSource import TriggeredSource

class StreamReconstructor(component):
    """\
    StreamReconstructor()
    
    This component receives reports on the status/completion of BitTorrent
    downloads from a TorrentPatron instance. It keeps a record of the
    order in which torrents were started and waits until the first is
    finished. It then outputs the filename of this torrent and removes
    it from its list. Then it waits for the second torrent (now the first
    on the list) to finish downloading, then outputs its filename and so on.
    If later torrents finish before earlier ones, their filenames are not
    output until their all their predecessors have finished.
    
    The purpose of this is output the names of files whose contents should
    be concatenated to a master file to reconstruct the stream.
    """
    
    def main(self):
        torrents = []
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                
                if isinstance(msg, TIPCNewTorrentCreated):
                    torrents.append([msg.torrentid, msg.savefolder]) # add the new torrent to the list of known torrents
                    
                elif isinstance(msg, TIPCTorrentStatusUpdate):
                    # if the status update is about the oldest torrent that
                    # has not been completed prior to now, then...
                    if len(torrents) > 0 and msg.torrentid == torrents[0][0]:
                        # if this oldest torrent is now complete
                        if msg.statsdictionary.get("fractionDone",0) == 1:
                            # forward on the name of the file downloaded in this torrent
                            self.send(torrents[0][1], "outbox") 
                            torrents.pop(0) # and remove it from our list of torrents that we care about
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdown) or isinstance(msg, producerFinished):
                    # if we are being told to shutdown then do so
                    self.send(producerFinished(self), "signal")
                    return
            
            self.pause()

class PartsFilenameGenerator(component):
    """\
    PartsFilenameGenerator()
    Arguments:
    - prefix - string to prepend to the id of a torrent to make its URL
    - [suffix] - string to append to the id of the torrent to make the URL
                 defaults to ".torrent"

    Generate the URLs of the .torrents that make up the stream
    from reports  of the total number of chunks/torrents in the stream
    that are received on "inbox".
    
    e.g. Assuming it was created as
    PartsFilenameGenerator("http://www.example.com/", ".torrent"),
    
    Send it "3" and it will output (one message listed per line):
    - "http://www.example.com/1.torrent"
    - "http://www.example.com/2.torrent"
    - "http://www.example.com/3.torrent"
    Then send it "3" again and it will output nothing.
    Now send it "5" and it will output:
    - "http://www.example.com/4.torrent"
    - "http://www.example.com/5.torrent"
    """
    def __init__(self, prefix, suffix = ".torrent"):
        self.prefix = prefix
        self.suffix = suffix
        super(self, PartsFilenameGenerator).__init__()
        
    def main(self):
        highestseensofar = 0 # we have not outputted any torrent URLs so far
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = int(self.recv("inbox"))
                
                # output the URLs of all the torrents whose numbers are > the
                # number of last torrent output and <= the value of message received
                while highestsofar < msg: 
                    highestsofar += 1
                    self.send(self.prefix + str(highestsofar) + self.suffix, "outbox")
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdown) or isinstance(msg, producerFinished):
                    self.send(producerFinished(self), "signal")
                    return
            
            self.pause()

def P2PStreamer(torrentsfolder):
    """\
    Arguments:
    - torrentsfolder, e.g. "http://my.server.example.org/radioFoo/"
    """
    
    # Create a pipeline of components whose net result is to output the contents of a certain URL
    # (torrentsfolder  + metafilename) every 60 seconds (the contents at the time of output, i.e.
    # it fetches the page every 60 seconds).
    
    poller = Pipeline(
        # This generates a message every 60 seconds to wake TriggeredSource
         # allowing us to poll the meta file without busy-waiting.
        CheapAndCheerfulClock(60.0),
        
         # This sends the string (torrentsfolder  + "meta.txt") every time it receives a message
         # This string will be the URL of the meta file on the torrent hosting website
         # e.g. "http://my.server.example.org/radioFoo/meta.txt"
        TriggeredSource(torrentsfolder + "meta.txt"),
        
        # SimpleHTTPClient retrieves the resource specified by the message it receives,
        # which will be URL string. 
        # i.e. It fetches the page whose URL is (torrentsfolder + "meta.txt) (the string
        # produced by TriggeredSource) and forwards on the contents of that page.
        
        # The contents of that particular page will always be a number
        # (in the form of a decimal ASCII string) which represents the number of
        # 'chunks' of the stream that exist
        SimpleHTTPClient()
    )
    
    # As a whole, streamer acts like a normal streaming client, outputting the contents of
    # a stream to its outbox, although in much larger chunks with longer in between chunks
    # than for a typical stream.
    streamer = Pipeline(
        # fetch the P2P-stream meta file every 60 seconds and send its contents on
        poller,
        
        # PartsFilenameGenerator uses the number retrived by poller
        # i.e. the number of chunks/torrents in the stream
        # to generate the URLs of all the .torrent files
        # (torrent metadata files) that make up the stream.
        # (They will have been named 1.torrent,
        # 2.torrent, 3.torrent ... etc. on the server).
        
        PartsFilenameGenerator(torrentsfolder, ".torrent"),        
        
        # Download these .torrent files (each message received by resourcefetcher
        # will be the URL of one .torrent file it should download). The
        # contents of the page downloaded it forwarded on to the next component.
        # NOTE: this downloads the .torrent file (metadata about part of the
        # stream) not the stream itself
        SimpleHTTPClient(),
        
        # now use BitTorrent to download the stream itself using the
        # metadata retrieved from .torrent files (each has information about a
        # section of the stream - a section itself is typically a few MB of data)
        # (TorrentPatron is a BitTorrent client component)
        TorrentPatron(),
        
        # output the names of the chunks of the stream as soon as they and
        # all previous chunks have been downloaded 
        StreamReconstructor(),
        
        # read the contents of these chunks (files)
        TriggeredFileReader(),
    )
    return streamer
    
if __name__ == '__main__':
    # ask the user from which website we should get the stream's metadata
    # e.g. "http://my.server.example.org/radioFoo/"
    torrentsfolder = raw_input("P2P-stream meta folder (URL): ")
    
    Pipeline(
        # fetch the stream using BitTorrent and HTTP - see above for details
        P2PStreamer(torrentsfolder),
        
        # write the stream to a file on disk
        SimpleFileWriter("myreconstructedstream.mp3")
    ).run()
    
