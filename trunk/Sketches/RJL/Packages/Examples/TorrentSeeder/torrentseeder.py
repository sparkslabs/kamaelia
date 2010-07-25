#!/usr/bin/env python
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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
==============================================
Torrent Seeder
==============================================

The user specifies a file to which they own the copyright that they wish
to share using BitTorrent. This example creates a .torrent
(BitTorrent metadata) file for that file and seeds it.

Enter a filename to the console, e.g.
>>> mycreativecommonssong.ogg

NOTE: The file whose name you give MUST be in the local directory
otherwise it will not be found for seeding.

How does it work?
-----------------
TorrentMaker reads the contents of the file whose path is entered by the user.
It creates a .torrent file which contains cryptographic hashes of the source
file and enough information to distribute it using BitTorrent (provided a
central 'tracker' server is available to tell peers who has the file).

TorrentPatron then seeds the source file.
i.e. it uploads it to any clients that request it.
Send others your .torrent file so they can download from you and later upload
your file to others.

Usage
-----
First enter the announce URL of your BitTorrent tracker,
e.g. http://myserver.example.org:6969/announce
Then enter the names of files you wish to seed (they must be
in the local directory). For each of these, a .torrent file
will be created. With a copy of this file, other users
can download from you. 
"""

from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Fanout import fanout

from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentClient import BasicTorrentExplainer
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.Community.RJL.Kamaelia.File.WholeFileWriter import WholeFileWriter
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentMaker import TorrentMaker
from Kamaelia.Community.RJL.Kamaelia.Util.PureTransformer import PureTransformer

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class TwoSourceListifier(component):
    """Wait until inboxes "a" and "b" have messages, then
    take the first from each and combine them into a new list
    of the form [a,b]. Repeat."""
    
    Inboxes = ["a", "b", "control"]
    def main(self):
        while 1:
            yield 1
            
            while self.dataReady("a") and self.dataReady("b"):
                self.send([self.recv("a"), self.recv("b")], "outbox")
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return
            
            self.pause()

if __name__ == '__main__':
    # The 'announce' URL of the BitTorrent tracker to use
    # e.g. "http://192.168.1.5:6969/announce"
    trackerannounceurl = raw_input("Tracker Announce URL: ")
    
    Graphline(
        filenamereader = ConsoleReader(">>> ", ""),
        
        # send the filename entered by the user to both the .torrent
        # maker and to the file writer to use as part of the filename
        # (so that it knows what to save the metadata as)
        filenamesplitter = fanout(["toNamer", "toTorrentMaker"]),
        
        # makes the .torrent file (BitTorrent metadata)
        torrentmaker = TorrentMaker(trackerannounceurl), 
        
        # saves the .torrent file
        filewriter = WholeFileWriter(),
        
        # does the seeding (uploading) of the file
        torrentpatron = TorrentPatron(),
        
        # puts a name to the .torrent file
        torrentnamer = TwoSourceListifier(),
        
        # send the .torrent file data to both the seeder and the saver
        torrentmetasplitter = fanout(["toTorrentPatron", "toNamer"]),

        # appends ".torrent" to the filename to give the .torrent filename
        suffixtorrent = PureTransformer(lambda x : x + ".torrent"),
        
        # output debugging messages, e.g. download progress
        explainer = pipeline(
            BasicTorrentExplainer(),
            ConsoleEchoer()
        ),
        
        linkages = {
            ("filenamereader", "outbox") : ("filenamesplitter", "inbox"),
            ("filenamesplitter", "toNamer") : ("suffixtorrent", "inbox"),
            ("suffixtorrent", "outbox")  :("torrentnamer", "a"),
            ("filenamesplitter", "toTorrentMaker") : ("torrentmaker", "inbox"),
            ("torrentmaker", "outbox") : ("torrentmetasplitter", "inbox"),
            ("torrentmetasplitter", "toTorrentPatron") : ("torrentpatron", "inbox"),
            ("torrentmetasplitter", "toNamer") : ("torrentnamer", "b"),            
            ("torrentnamer", "outbox") : ("filewriter", "inbox"),
            ("torrentpatron", "outbox") : ("explainer", "inbox"),
        }
    ).run()
