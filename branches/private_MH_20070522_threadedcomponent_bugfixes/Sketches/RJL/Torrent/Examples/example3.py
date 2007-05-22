from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

import sys
sys.path.append("../../Util")
sys.path.append("../../HTTP")
sys.path.append("../../Torrent")

from IcecastClient import IcecastClient, IcecastDemux, IcecastStreamRemoveMetadata
from Chunkifier import Chunkifier
from ChunkDistributor import ChunkDistributor
from WholeFileWriter import WholeFileWriter
from TorrentMaker import TorrentMaker
from Kamaelia.Util.Fanout import fanout
from HTTPHelpers import HTTPMakePostRequest
from HTTPClient import SimpleHTTPClient
from TorrentPatron import TorrentPatron

from PureTransformer import PureTransformer

from OnDemandIntrospector import OnDemandIntrospector
from Kamaelia.File.Writing import SimpleFileWriter

if __name__ == '__main__':
    pipeline(
        ConsoleReader(),
        OnDemandIntrospector(),
        ConsoleEchoer(),
    ).activate()
    Graphline(
        streamin = pipeline(
            IcecastClient("http://127.0.0.1:1234/"), # a stream's address
            IcecastDemux(),
            IcecastStreamRemoveMetadata(),
            Chunkifier(500000),
            ChunkDistributor("./"),
            WholeFileWriter(),
            TorrentMaker("http://192.168.1.5:6969/announce"),
        ),
        
        split = fanout(["toMetaUploader", "toSharer"]),
        
        fileupload = pipeline(
            ChunkDistributor("./torrents/", ".torrent"),
            WholeFileWriter(),
            PureTransformer(lambda x : x + "\n"),
            SimpleFileWriter("filelist.txt")
        ),

        #WholeFileWriter()
        #HTTPMakePostRequest("http://192.168.1.15/torrentupload.php"),
        #SimpleHTTPClient()
        
        # uploader still to write
        bt = TorrentPatron(),
        linkages = {
            ("streamin", "outbox") : ("split", "inbox"),
            ("split", "toMetaUploader") : ("fileupload", "inbox"),
            ("split", "toSharer") : ("bt", "inbox"),            
            #("split","toMetaUploader") : ("whatever","inbox"),
        }
    ).run()
    
