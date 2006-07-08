"""An example application using the TorrentPatron component to download
several files concurrently, fetching their .torrent files using HTTP."""

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Axon.Scheduler import scheduler

import sys
sys.path.append("../../")
sys.path.append("../../Util")
sys.path.append("../../HTTP")
sys.path.append("../../Torrent")

from DataSource import DataSource
from OnDemandIntrospector import OnDemandIntrospector

from HTTPClient import SimpleHTTPClient
from Kamaelia.Util.Introspector import Introspector
from TorrentClient import BasicTorrentExplainer
from TorrentPatron import TorrentPatron
from Kamaelia.Internet.TCPClient import TCPClient
if __name__ == '__main__':
    
    # download a linux distro
    X = pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent"] ),
        SimpleHTTPClient(),
        #TorrentPatron(),
        #BasicTorrentExplainer(),
        #ConsoleEchoer(),    
    )

    Y = pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent",
                     "http://www.legaltorrents.com/bit/freeculture.zip.torrent"] ),
        SimpleHTTPClient(),
        #TorrentPatron(),
        #BasicTorrentExplainer(),
        #ConsoleEchoer(),    
    )
    Z = pipeline(
        ConsoleReader(),
        OnDemandIntrospector(), # Introspector(),
        ConsoleEchoer()
        #TCPClient("127.0.0.1", 1500),
    )
    X.activate()
    Y.activate()
    Z.activate()
    scheduler.run.runThreads(slowmo=0)
