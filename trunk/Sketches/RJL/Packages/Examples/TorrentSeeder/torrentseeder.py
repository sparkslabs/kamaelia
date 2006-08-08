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
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

from TorrentClient import TorrentClient, BasicTorrentExplainer
from TorrentMaker import TorrentMaker

if __name__ == '__main__':
    # seed a file
    pipeline(
        ConsoleReader(">>> ", ""),
        TorrentMaker("http://localhost:6969/announce"),
        WholeFileWriter()
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer()
    ).run()
