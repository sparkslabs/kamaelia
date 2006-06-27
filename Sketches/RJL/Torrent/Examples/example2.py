from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Axon.Scheduler import scheduler

import sys ; sys.path.append("../")

from TriggeredFileReader import TriggeredFileReader
from DataSource import DataSource
from HTTPClient import HTTPClient
from btkam import BasicTorrentExplainer
from btkamservice import TorrentPatron

if __name__ == '__main__':
    
    # download a linux distro
    X = pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent"] ),
        HTTPClient(),
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer(),    
    )

    Y = pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent",
                     "http://www.legaltorrents.com/bit/freeculture.zip.torrent"] ),
        HTTPClient(),
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer(),    
    )
    X.activate()
    Y.activate()
    scheduler.run.runThreads(slowmo=0)
