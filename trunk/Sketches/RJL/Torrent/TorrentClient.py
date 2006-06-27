#!/usr/bin/env python

# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Bram Cohen, Uoti Urpala, John Hoffman, and David Harrison

from __future__ import division

from BitTorrent.translation import _

import pdb
import sys
import os
from cStringIO import StringIO
import logging
from logging import ERROR
from time import strftime, sleep
import traceback

import BitTorrent.stackthreading as threading
from BitTorrent.defer import DeferredEvent
from BitTorrent import inject_main_logfile
from BitTorrent.MultiTorrent import Feedback, MultiTorrent
from BitTorrent.defaultargs import get_defaults
from BitTorrent.parseargs import printHelp
from BitTorrent.zurllib import urlopen
from BitTorrent.prefs import Preferences
from BitTorrent import configfile
from BitTorrent import BTFailure
from BitTorrent import version
from BitTorrent import console, stderr_console
from BitTorrent import GetTorrent
from BitTorrent.RawServer_twisted import RawServer, task
from BitTorrent.ConvertedMetainfo import ConvertedMetainfo
from BitTorrent.platform import get_temp_dir
inject_main_logfile()

from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

#TorrentClient Responses
class IPCNewTorrentCreated(object):
    def __init__(self, torrentid, savefolder):
        super(IPCNewTorrentCreated, self).__init__()
        self.torrentid = torrentid
        self.savefolder = savefolder
    def gettext(self):
        return "New torrent %s created in %s" % (self.torrentid, self.savefolder)
        
class IPCTorrentAlreadyDownloading(object):
    def __init__(self, torrentid):
        super(IPCTorrentAlreadyDownloading, self).__init__()
        self.torrentid = torrentid
    def gettext(self):
        return "That torrent is already downloading!"
        
class IPCTorrentStartFail(object):
    def gettext(self):
        return "Torrent failed to start!"

class IPCTorrentStatusUpdate(object):
    def __init__(self, torrentid, statsdictionary):
        super(IPCTorrentStatusUpdate, self).__init__()    
        self.torrentid = torrentid
        self.statsdictionary = statsdictionary
    def gettext(self):
        return "Torrent %d status : %s" % (self.torrentid, str(int(self.statsdictionary.get("fractionDone","0") * 100)) + "%")

#Requests to TorrentClient
class IPCCreateNewTorrent(object):
    def __init__(self, rawmetainfo):
        super(IPCCreateNewTorrent, self).__init__()
        self.rawmetainfo = rawmetainfo
        
class IPCCloseTorrent(object):
    def __init__(self, torrentid):
        super(IPCCloseTorrent, self).__init__()
        self.torrentid = torrentid


class MakeshiftTorrent(object):
    def __init__(self, metainfo):
        super(MakeshiftTorrent, self).__init__()
        self.metainfo = metainfo
        
class TorrentClient(threadedcomponent):
    """Using threadedcomponent so we don't have to worry about blocking IO or making
    mainline yield periodically"""
    
    Inboxes  = { "inbox"   : "Torrent URL",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "State change information, e.g. finished",
                "signal" : "NOT USED",
              }
    def __init__(self, tickInterval = 5):
        super(TorrentClient, self).__init__()
        self.totaltorrents = 0
        self.torrents = {}
        self.torrentinfohashes = {}
        self.tickInterval = tickInterval #seconds
        
    def main(self):
        uiname = "bittorrent-console"
        defaults = get_defaults(uiname)
        config, args = configfile.parse_configuration_and_args(defaults, uiname)
        config = Preferences().initWithDict(config)
        data_dir = config['data_dir']
        self.core_doneflag = DeferredEvent()
        self.rawserver_doneflag = DeferredEvent()
        
        rawserver = RawServer(config) #event and I/O scheduler
        self.multitorrent = MultiTorrent(config, self.core_doneflag, rawserver, data_dir) #class used to add, control and remove torrents

        self.tick() #add periodic function call
    
        rawserver.add_task(0, self.core_doneflag.addCallback, lambda r: rawserver.external_add_task(0, shutdown))
        rawserver.listen_forever(self.rawserver_doneflag)

    def startTorrent(self, metainfo, save_incomplete_as, save_as, torrentid):
        """startTorrent causes MultiTorrent to begin downloading a torrent eventually.
        Use it instead of _start_torrent."""
        
        self._create_torrent(metainfo, save_incomplete_as, save_as)
        self.multitorrent.rawserver.add_task(1, self._start_torrent, metainfo, torrentid)
            
    def _create_torrent(self, metainfo, save_incomplete_as, save_as):
        if not self.multitorrent.torrent_known(metainfo.infohash):
            df = self.multitorrent.create_torrent(metainfo, save_incomplete_as, save_as)                
        #except Exception, e:
        #    print e
        #    return False
                
    def _start_torrent(self, metainfo, torrentid):
        #try:
        t = None
        if self.multitorrent.torrent_known( metainfo.infohash ):
            t = self.multitorrent.get_torrent(metainfo.infohash)
    
        # HACK!! Rewrite when INITIALIZING state is available.
        if t is None or not t.is_initialized():
            #self.logger.debug( "Waiting for torrent to initialize." )
            self.multitorrent.rawserver.add_task(3, self._start_torrent, metainfo, torrentid)
            return

        if not self.multitorrent.torrent_running(metainfo.infohash):
            df = self.multitorrent.start_torrent(metainfo.infohash)
            self.torrents[torrentid] = self.multitorrent.get_torrent(metainfo.infohash)
            
            #yield df
            #df.getResult()  # raises exception if one occurred in yield.
        
        #    print e
        #    print "Failed to start torrent"

    def decodeTorrent(self, data):
        from BitTorrent.bencode import bdecode, bencode
        metainfo = None
        try:
            b = bdecode(data)
            metainfo = ConvertedMetainfo(b)
        except Exception, e:
            pass
        return metainfo
        
    def tick(self):
        "Called periodically"
        self.multitorrent.rawserver.add_task(self.tickInterval, self.tick)
        #print "Tick"
        while self.dataReady("inbox"):
            temp = self.recv("inbox")
            if isinstance(temp, IPCCreateNewTorrent) or isinstance(temp, str):
                if isinstance(temp, str):
                    metainfo = self.decodeTorrent(temp)
                else:
                    metainfo = self.decodeTorrent(temp.rawmetainfo)
                if metainfo != None:
                    savefolder = os.path.join("./",metainfo.name_fs)
                    
                    existingTorrentId = self.torrentinfohashes.get(metainfo.infohash, 0)
                    if existingTorrentId != 0:
                        self.send(IPCTorrentAlreadyDownloading(existingTorrentId), "outbox")
                    else:
                        self.totaltorrents += 1
                        self.torrentinfohashes[metainfo.infohash] = self.totaltorrents
                        self.torrents[self.totaltorrents] = MakeshiftTorrent(metainfo)                    
                        self.startTorrent(metainfo, savefolder, savefolder, self.totaltorrents)
                        self.send(IPCNewTorrentCreated(self.totaltorrents, savefolder), "outbox")
            elif isinstance(temp, IPCCloseTorrent):
                torrent = self.torrents.get(temp.torrentid,None)
                if torrent != None:
                    self.multitorrent.remove_torrent(torrent.metainfo.infohash)
                    self.torrentinfohashes.erase(torrent.metainfo.infohash)
                    self.torrents.erase(temp.torrentid)
                    
        for torrentid, torrent in self.torrents.items():
            if not isinstance(torrent, MakeshiftTorrent):
                self.send(IPCTorrentStatusUpdate(torrentid, torrent.get_status()), "outbox")
        
        #if self.torrent is not None:
        #    status = self.torrent.get_status(self.config['spew'])
        #    self.d.display(status)


class BasicTorrentExplainer(component):
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                temp = self.recv("inbox")
                try:
                    self.send(temp.gettext() + "\n", "outbox")
                except:
                    pass
            self.pause()
           
if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    import sys ; sys.path.append("/home/ryan/kamaelia/Sketches/RJL/")
    from TriggeredFileReader import TriggeredFileReader
    from Axon.Component import component

    # download a linux distro or whatever
    pipeline(
        ConsoleReader(">>> ", ""),
        TriggeredFileReader(),
        TorrentClient(),
        BasicTorrentExplainer(),
        ConsoleEchoer(),    
    ).run()   

            
