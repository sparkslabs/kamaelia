# (Bit)Torrent IPC messages

class TIPC(object):
    "explanation %(foo)s did %(bar)s"
    def __init__(self, **kwds):
        super(TIPC, self).__init__()
        self.__dict__.update(kwds)
    def getText(self):
        return self.__class__.__doc__ % self.__dict__

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
class TIPCTorrentStatusUpdate(object):
    "Current status of a single torrent"
    def __init__(self, torrentid, statsdictionary):
        super(IPCTorrentStatusUpdate, self).__init__()    
        self.torrentid = torrentid
        self.statsdictonary = statsdictionary
    def gettext(self):
        return "Torrent %d status : %s" % (self.torrentid, str(int(self.statsdictionary.get("fractionDone","0") * 100)) + "%")

# ====================== Messages to send to TorrentClient ======================

# create a new torrent (a new download session) from a .torrent file's binary contents
class TIPCCreateNewTorrent(TIPC):
    "Create a new torrent"
    #Parameters: rawmetainfo

# close a running torrent        
class TIPCCloseTorrent(object):
    "Close torrent %(torrentid)d"
    #Parameters: torrentid
    def __init__(self, torrentid):
        super(IPCCloseTorrent, self).__init__()
        self.torrentid = torrentid
