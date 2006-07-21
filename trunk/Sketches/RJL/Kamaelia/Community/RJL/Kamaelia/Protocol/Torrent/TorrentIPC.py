# (Bit)Torrent IPC messages

class TIPC(object):
    "explanation %(foo)s did %(bar)s"
    Parameters = [] # ["foo", "bar"]
    def __init__(self, **kwds):
        super(TIPC, self).__init__()
        for param in self.Parameters:
            optional = False
            if param[:1] == "?":
                param = param[1:]
                optional = True
                
            if not kwds.has_key(param):
                if not optional:
                    raise ValueError(param + " not given as a parameter to " + str(self.__class__.__name__))
                else:
                    self.__dict__[param] = None
            else:
                self.__dict__[param] = kwds[param]
                del kwds[param]

        for additional in kwds.keys():
            raise ValueError("Unknown parameter " + additional + " to " + str(self.__class__.__name__))
            
        self.__dict__.update(kwds)

    def __str__(self):
        return self.__class__.__doc__ % self.__dict__

# ====================== Messages to send to TorrentMaker =======================
class TIPCMakeTorrent(TIPC):
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
class TIPCServicePassOn(TIPC):
    "Add a client to TorrentService"
    Parameters = [ "replyService", "message" ]
    #Parameters: replyService, message

# request to add a TorrentPatron to a TorrentService's list of clients
class TIPCServiceAdd(TIPC):
    "Add a client to TorrentService"
    Parameters = [ "replyService" ]
    #Parameters: replyService

# request to remove a TorrentPatron from a TorrentService's list of clients
class TIPCServiceRemove(TIPC):
    "Remove a client from TorrentService"
    Parameters = [ "replyService" ]
    #Parameters: replyService

# ==================== Messages for TorrentClient to produce ====================
# a new torrent has been added with id torrentid
class TIPCNewTorrentCreated(TIPC):
    "New torrent %(torrentid)d created in %(savefolder)s"
    Parameters = [ "torrentid", "savefolder" ]    
    #Parameters: torrentid, savefolder
    
# the torrent you requested me to download is already being downloaded as torrentid
class TIPCTorrentAlreadyDownloading(TIPC):
    "That torrent is already downloading!"
    Parameters = [ "torrentid" ]
    #Parameters: torrentid

# for some reason the torrent could not be started
class TIPCTorrentStartFail(object):
    "Torrent failed to start!"
    Parameters = []
    #Parameters: (none)

# message containing the current status of a particular torrent
class TIPCTorrentStatusUpdate(TIPC):
    "Current status of a single torrent"
    def __init__(self, torrentid, statsdictionary):
        super(TIPCTorrentStatusUpdate, self).__init__()    
        self.torrentid = torrentid
        self.statsdictionary = statsdictionary
    
    def __str__(self):
        return "Torrent %d status : %s" % (self.torrentid, str(int(self.statsdictionary.get("fractionDone",0) * 100)) + "%")

# ====================== Messages to send to TorrentClient ======================

# create a new torrent (a new download session) from a .torrent file's binary contents
class TIPCCreateNewTorrent(TIPC):
    "Create a new torrent"
    Parameters = [ "rawmetainfo" ]
    #Parameters: rawmetainfo - the contents of a .torrent file

# close a running torrent        
class TIPCCloseTorrent(TIPC):
    "Close torrent %(torrentid)d"
    Parameters = [ "torrentid" ]
    #Parameters: torrentid
