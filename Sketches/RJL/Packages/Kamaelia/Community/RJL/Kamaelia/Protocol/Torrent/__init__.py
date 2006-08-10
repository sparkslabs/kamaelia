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
# This file is required to import files from its directory
"""
                    Kamaelia.Protocol.Torrent

          Components for downloading and distributing
          files using the BitTorrent peer-to-peer
          protocol.


Note: This software and information is intended to faciliate legal
file distribution. Do not use them for any unlawful activities.
The software project and the author of these components are not
affiliated in any way with the creator(s) of BitTorrent.

Prerequisites
=============
In order to function, Kamaelia's BitTorrent components require the
Mainline (official) BitTorrent client to be installed.

Download source: http://download.bittorrent.com/dl/?M=D

The latest version of the Mainline client that is well-tested with
Kamaelia is 4.20.4. This is the minimum version that you should use.

The source (.tar.gz) version is highly recommended as it ensures
Python installs the BitTorrent library to the right place.

Note: On windows, compilation from source requires:
* ctypes - http://sourceforge.net/project/showfiles.php?group_id=71702
* pywin32 - http://sourceforge.net/project/showfiles.php?group_id=78018

Examples
========
TorrentGUI - a minimal Tkinter GUI for BitTorrent
P2PStreamSeed - streaming over BitTorrent, source/uploader/seed
P2PStreamPeer - streaming over BitTorrent, sink/downloader/peer

Components
==========
* TorrentClient  - an interface to the Mainline BitTorrent client
* TorrentPatron  - an analogue of TorrentClient that supports several
                  concurrent instances
* TorrentMaker   - a .torrent (BitTorrent metadata) file creator
* TorrentService - a component that shares a single
                   TorrentClient between many TorrentPatrons
* TorrentTracker - a BitTorrent tracker component


August 2006 - Ryan Lothian
Created for Google Summer of Code 2006
"""
