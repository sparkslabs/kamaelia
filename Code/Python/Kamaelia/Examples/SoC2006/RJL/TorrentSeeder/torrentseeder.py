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

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Fanout import Fanout

from Kamaelia.Protocol.Torrent.TorrentClient import BasicTorrentExplainer
from Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.File.WholeFileWriter import WholeFileWriter
from Kamaelia.Protocol.Torrent.TorrentMaker import TorrentMaker
from Kamaelia.Util.PureTransformer import PureTransformer

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
        filenamesplitter = Fanout(["toNamer", "toTorrentMaker"]),
        
        # makes the .torrent file (BitTorrent metadata)
        torrentmaker = TorrentMaker(trackerannounceurl), 
        
        # saves the .torrent file
        filewriter = WholeFileWriter(),
        
        # does the seeding (uploading) of the file
        torrentpatron = TorrentPatron(),
        
        # puts a name to the .torrent file
        torrentnamer = TwoSourceListifier(),
        
        # send the .torrent file data to both the seeder and the saver
        torrentmetasplitter = Fanout(["toTorrentPatron", "toNamer"]),

        # appends ".torrent" to the filename to give the .torrent filename
        suffixtorrent = PureTransformer(lambda x : x + ".torrent"),
        
        # output debugging messages, e.g. download progress
        explainer = Pipeline(
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
