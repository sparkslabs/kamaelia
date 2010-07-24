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

"""(Bit)Torrent IPC messages"""
from Kamaelia.BaseIPC import IPC

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
