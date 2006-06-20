from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

import sys ; sys.path.append("/home/ryan/kamaelia/Sketches/RJL/")

from TriggeredFileReader import TriggeredFileReader
from DataSource import DataSource
from HTTPClient import HTTPClient
from btkam import TorrentClient, BasicTorrentExplainer
if __name__ == '__main__':
    
    # download a linux distro
    pipeline(
        DataSource( ["http://www.legaltorrents.com/bit/trusted-computing.torrent",
                     "http://www.legaltorrents.com/bit/freeculture.zip.torrent"] ),
        HTTPClient(),
        TorrentClient(),
        BasicTorrentExplainer(),
        ConsoleEchoer(),    
    ).run()   
