"""An example application using the TorrentPatron component to download
several files concurrently, fetching their .torrent files using HTTP."""

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Axon.Scheduler import scheduler

import sys
sys.path.append("../../")

from Util.DataSource import DataSource

from HTTP.HTTPClient import SimpleHTTPClient

from Torrent.TorrentClient import BasicTorrentExplainer
from Torrent.TorrentPatron import TorrentPatron

if __name__ == '__main__':
    
    # download a linux distro
    X = pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent"] ),
        SimpleHTTPClient(),
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer(),    
    )

    Y = pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent",
                     "http://www.legaltorrents.com/bit/freeculture.zip.torrent"] ),
        SimpleHTTPClient(),
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer(),    
    )
    X.activate()
    Y.activate()
    scheduler.run.runThreads(slowmo=0)
