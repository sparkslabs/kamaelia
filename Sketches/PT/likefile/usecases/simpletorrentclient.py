#!/usr/bin/env python

# A demonstration of using likefile to control a torrent downloader.

import likefile, time, sys
from Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
from Kamaelia.Protocol.Torrent.TorrentClient import BasicTorrentExplainer
from Kamaelia.File.TriggeredFileReader import TriggeredFileReader
from Kamaelia.Chassis.Pipeline import Pipeline

likefile.schedulerThread(slowmo=0.01).start()

try: filename = sys.argv[1]
except IndexError:
    print "usage: ./simpletorrentclient.py <filename.torrent>"
    sys.exit(1)


torrenter = likefile.LikeFile(
    Pipeline(TriggeredFileReader(),
        TorrentClient(),
        BasicTorrentExplainer(),
        ))

torrenter.activate()
torrenter.put(filename)
try:
    while True:
        print torrenter.get()
except KeyboardInterrupt:
        torrenter.shutdown()