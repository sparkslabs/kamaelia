from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

import sys
sys.path.append("../../")
sys.path.append("../../Util")
sys.path.append("../../HTTP")
sys.path.append("../../Torrent")

from DataSource import DataSource
from OnDemandIntrospector import OnDemandIntrospector

from TorrentClient import TorrentClient, BasicTorrentExplainer
from TorrentMaker import TorrentMaker

if __name__ == '__main__':
    
    # seed a file
    pipeline(
        ConsoleReader(">>> ",""),
        TorrentMaker("http://localhost:6969/announce"),
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer()
        #TorrentPatron(),
        #BasicTorrentExplainer(),
        #ConsoleEchoer(),    
    ).run()
