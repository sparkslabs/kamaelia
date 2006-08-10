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

"""

from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Fanout import fanout

from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentClient import BasicTorrentExplainer
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.Community.RJL.Kamaelia.File.WholeFileWriter import WholeFileWriter
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentMaker import TorrentMaker

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class TwoSourceListifier(component):
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
    # seed a file
    Graphline(
        filenamereader = ConsoleReader(">>> ", ""),
        filenamesplitter = fanout(["toNamer", "toTorrentMaker"]),
        torrentmaker = TorrentMaker("http://localhost:6969/announce"),
        filewriter = WholeFileWriter(),
        torrentpatron = TorrentPatron(),
        torrentnamer = TwoSourceListifier(),
        torrentmetasplitter = fanout(["toTorrentPatron", "toNamer"]),
        explainer = pipeline(
            BasicTorrentExplainer(),
            ConsoleEchoer()
        ),
        linkages = {
            ("filenamereader", "outbox") : ("filenamesplitter", "inbox"),
            ("filenamesplitter", "toNamer") : ("torrentnamer", "a"),
            ("filenamesplitter", "toTorrentMaker") : ("torrentmaker", "inbox"),
            ("torrentmaker", "outbox") : ("torrentmetasplitter", "inbox"),
            ("torrentmetasplitter", "toTorrentPatron") : ("torrentpatron", "inbox"),
            ("torrentmetasplitter", "toNamer") : ("torrentnamer", "b"),            
            ("torrentnamer", "outbox") : ("filewriter", "inbox"),
            ("torrentpatron", "outbox") : ("explainer", "inbox"),
        }
    ).run()
