# -*- coding: utf-8 -*-
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

# (Bit)Torrent IPC messages

class TIPC(object):
    "explanation %(foo)s did %(bar)s"
    def __init__(self, **kwds):
        super(TIPC, self).__init__()
        self.__dict__.update(kwds)
    def getText(self):
        return self.__class__.__doc__ % self.__dict__

# ====================== Messages to send to TorrentMaker =======================
class TIPCMakeTorrent(TIPC):
    "Create a .torrent file"
    #Parameters:
    # trackerurl - the URL of the BitTorrent tracker that will be used
    #  log2piecesizebytes - log base 2 of the hash-piece-size, sensible value: 18
    #  title - name of the torrent
    #  comment - a field that can be read by users when they download the torrent
    #  srcfile - the file that the .torrent file will have metainfo about
    
# ========= Messages for TorrentPatron to send to TorrentService ================

# a message for TorrentClient (i.e. to be passed on by TorrentService)
class TIPCServicePassOn(TIPC):
    "Add a client to TorrentService"
    #Parameters: replyService, message

# request to add a TorrentPatron to a TorrentService's list of clients
class TIPCServiceAdd(TIPC):
    "Add a client to TorrentService"
    #Parameters: replyService

# request to remove a TorrentPatron from a TorrentService's list of clients
class TIPCServiceRemove(TIPC):
    "Remove a client from TorrentService"
    #Parameters: replyService

# ==================== Messages for TorrentClient to produce ====================
# a new torrent has been added with id torrentid
class TIPCNewTorrentCreated(TIPC):
    "New torrent %(torrentid)d created in %(savefolder)s"
    #Parameters: torrentid, savefolder
    
# the torrent you requested me to download is already being downloaded as torrentid
class TIPCTorrentAlreadyDownloading(TIPC):
    "That torrent is already downloading!"
    #Parameters: torrentid

# for some reason the torrent could not be started
class TIPCTorrentStartFail(object):
    "Torrent failed to start!"
    #Parameters: (none)

# message containing the current status of a particular torrent
class TIPCTorrentStatusUpdate(TIPC):
    "Current status of a single torrent"
    def __init__(self, torrentid, statsdictionary):
        super(TIPCTorrentStatusUpdate, self).__init__()    
        self.torrentid = torrentid
        self.statsdictionary = statsdictionary
    def getText(self):
        return "Torrent %d status : %s" % (self.torrentid, str(int(self.statsdictionary.get("fractionDone",0) * 100)) + "%")

# ====================== Messages to send to TorrentClient ======================

# create a new torrent (a new download session) from a .torrent file's binary contents
class TIPCCreateNewTorrent(TIPC):
    "Create a new torrent"
    #Parameters: rawmetainfo

# close a running torrent        
class TIPCCloseTorrent(TIPC):
    "Close torrent %(torrentid)d"
    #Parameters: torrentid
