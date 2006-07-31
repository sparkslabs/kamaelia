from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Fanout import fanout

from Kamaelia.Community.RJL.Kamaelia.Util.Chunkifier import Chunkifier
from Kamaelia.Community.RJL.Kamaelia.Util.ChunkNamer import ChunkNamer
from Kamaelia.Community.RJL.Kamaelia.File.WholeFileWriter import WholeFileWriter

from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentMaker import TorrentMaker
from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron

from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.IcecastClient import IcecastClient, IcecastDemux, IcecastStreamRemoveMetadata
from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPHelpers import HTTPMakePostRequest
from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient

from Kamaelia.Community.RJL.Kamaelia.Util.PureTransformer import PureTransformer

if __name__ == '__main__':
    streamurl = raw_input("Stream URL: ") # e.g. "http://a.stream.url.example.com:1234/"
    trackerannounceurl = raw_input("Tracker Announce URL: ") # e.g. "http://192.168.1.5:6969/announce"
    trackerpostuploader = raw_input("Tracker Upload Script: ") # e.g. "http://192.168.1.5/torrentupload.php"
    
    chunksize = 2**20 # one megabyte
    
    Graphline(
        streamin = pipeline(
            IcecastClient(streamurl), # a stream's address
            IcecastDemux(),
            IcecastStreamRemoveMetadata(),
            Chunkifier(chunksize),
            ChunkNamer("./"),
            WholeFileWriter(),
            TorrentMaker(trackerannounceurl),
        ),
        
        split = fanout(["toMetaUploader", "toSharer"]),
        
        fileupload = pipeline(
            HTTPMakePostRequest(trackerpostuploader),
            SimpleHTTPClient()
        ),

        bt = TorrentPatron(),
        linkages = {
            ("streamin", "outbox") : ("split", "inbox"),
            ("split", "toMetaUploader") : ("fileupload", "inbox"),
            ("split", "toSharer") : ("bt", "inbox"),            
        }
    ).run()
    
