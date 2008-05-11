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

"""(Bit)Torrent IPC messages"""
from Kamaelia.Community.RJL.Kamaelia.IPC.BaseIPC import IPC

# ====================== Messages to send to TorrentMaker =======================
class TIPCMakeTorrent(IPC):
    "Create a .torrent file"
    Parameters = [ "trackerurl", "log2piecesizebytes", "title", "comment", "srcfile" ]
    
    #Parameters:
    # trackerurl - the URL of the BitTorrent tracker that will be used
    #  log2piecesizebytes - log base 2 of the hash-piece-size, sensible value: 18
    #  title - name of the torrent
    #  comment - a field that can be read by users when they download the torrent
    #  srcfile - the file that the .torrent file will have metainfo about
    
# ========= Messages for TorrentPatron to send to TorrentService ================

# a message for TorrentClient (i.e. to be passed on by TorrentService)
class TIPCServicePassOn(IPC):
    "Add a client to TorrentService"
    Parameters = [ "replyService", "message" ]
    #Parameters: replyService, message

# request to add a TorrentPatron to a TorrentService's list of clients
class TIPCServiceAdd(IPC):
    "Add a client to TorrentService"
    Parameters = [ "replyService" ]
    #Parameters: replyService

# request to remove a TorrentPatron from a TorrentService's list of clients
class TIPCServiceRemove(IPC):
    "Remove a client from TorrentService"
    Parameters = [ "replyService" ]
    #Parameters: replyService

# ==================== Messages for TorrentClient to produce ====================
# a new torrent has been added with id torrentid
class TIPCNewTorrentCreated(IPC):
    "New torrent %(torrentid)d created in %(savefolder)s"
    Parameters = [ "torrentid", "savefolder" ]    
    #Parameters: torrentid, savefolder
    
# the torrent you requested me to download is already being downloaded as torrentid
class TIPCTorrentAlreadyDownloading(IPC):
    "That torrent is already downloading!"
    Parameters = [ "torrentid" ]
    #Parameters: torrentid

# for some reason the torrent could not be started
class TIPCTorrentStartFail(object):
    "Torrent failed to start!"
    Parameters = []
    #Parameters: (none)

# message containing the current status of a particular torrent
class TIPCTorrentStatusUpdate(IPC):
    "Current status of a single torrent"
    def __init__(self, torrentid, statsdictionary):
        super(TIPCTorrentStatusUpdate, self).__init__()    
        self.torrentid = torrentid
        self.statsdictionary = statsdictionary
    
    def __str__(self):
        return "Torrent %d status : %s" % (self.torrentid, str(int(self.statsdictionary.get("fractionDone",0) * 100)) + "%")

# ====================== Messages to send to TorrentClient ======================

# create a new torrent (a new download session) from a .torrent file's binary contents
class TIPCCreateNewTorrent(IPC):
    "Create a new torrent"
    Parameters = [ "rawmetainfo" ]
    #Parameters: rawmetainfo - the contents of a .torrent file

# close a running torrent        
class TIPCCloseTorrent(IPC):
    "Close torrent %(torrentid)d"
    Parameters = [ "torrentid" ]
    #Parameters: torrentid
