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

# Written by Bram Cohen, Uoti Urpala and John Hoffman

# Converted to a kamaelia threadedcomponent by Ryan Lothian

from __future__ import division

from BitTorrent.platform import install_translation
install_translation()

import sys
import os
import threading

from time import time, strftime, sleep
from cStringIO import StringIO

from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

from BitTorrent.download import Feedback, Multitorrent
from BitTorrent.defaultargs import get_defaults
from BitTorrent.parseargs import printHelp
from BitTorrent.zurllib import urlopen
from BitTorrent.bencode import bdecode
from BitTorrent.ConvertedMetainfo import ConvertedMetainfo
from BitTorrent.prefs import Preferences
from BitTorrent import configfile
from BitTorrent import BTFailure
from BitTorrent import version
from BitTorrent import GetTorrent

class Lagger(component):
	def main(self):
		while 1:
			yield 1
			sleep(0.05)


class TorrentClient(threadedcomponent):
    """Using threadedcomponent so we don't have to worry about blocking IO or making
    mainline yield periodically"""
    
    Inboxes  = { "inbox"   : "Commands, e.g. shutdown",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "State change information, e.g. finished",
                "signal" : "NOT USED",
              }

    def __init__(self, torrentfilename):
        super(TorrentClient, self).__init__()
        self.torrentfilename = torrentfilename
        self.done = False
        
    def main(self):
        print "TorrentClient.run"
        """Main loop"""
        uiname = 'bittorrent-console'
        defaults = get_defaults(uiname)
        defaults["twisted"] = 0
        metainfo = None
        config, args = configfile.parse_configuration_and_args(defaults, uiname)
        try:
            metainfo, errors = GetTorrent.get( self.torrentfilename )
            if errors:
                raise BTFailure(_("Error reading .torrent file: ") + '\n'.join(errors))
            else:
                self.dl = DLKamaelia(metainfo, config, self)
                self.dl.run()
        except BTFailure, e:
            print str(e)
            sys.exit(1)
        self.outqueues["outbox"].put("exited")
        
    def checkInboxes(self):
        while not self.inqueues["inbox"].empty():
            command = self.inqueues["inbox"].get()
            if command == "shutdown":
                self.dl.multitorrent.rawserver.doneflag.set()

    def finished(self):
        """Called by DL class when the download has completed successfully"""
        self.done = True
        self.send("complete", "outbox")
        print "BitTorrent debug: finished"

    def error(self, errormsg):
        """Called by DL if an error occurs"""
        print strftime('[%H:%M:%S] ') + errormsg
        self.send("failed", "outbox")

    def display(self, statistics):
        """Called by DL to display status updates"""
        # Forward on to next component
        self.send(statistics, "outbox")
        
    def set_torrent_values(self, name, path, size, numpieces):
        self.file = name
        self.downloadTo = path
        self.fileSize = size
        self.numpieces = numpieces

class DLKamaelia(Feedback):
    """This class accepts feedback from the multitorrent downloader class
    which it can then pass back to the inboxes of TorrentClient"""
    def __init__(self, metainfo, config, interface):
        self.doneflag = threading.Event()
        self.metainfo = metainfo
        self.config = Preferences().initWithDict(config)
        self.d = interface
        
    def run(self):
        try:
            self.multitorrent = Multitorrent(self.config, self.doneflag,
                                             self.global_error)
            # raises BTFailure if bad
            metainfo = ConvertedMetainfo(bdecode(self.metainfo))
            torrent_name = metainfo.name_fs
            if self.config['save_as']:
                if self.config['save_in']:
                    raise BTFailure(_("You cannot specify both --save_as and "
                                      "--save_in"))
                saveas = self.config['save_as']
            elif self.config['save_in']:
                saveas = os.path.join(self.config['save_in'], torrent_name)
            else:
                saveas = torrent_name

            self.d.set_torrent_values(metainfo.name, os.path.abspath(saveas),
                                metainfo.total_bytes, len(metainfo.hashes))
            self.torrent = self.multitorrent.start_torrent(metainfo,
                                Preferences(self.config), self, saveas)
        except BTFailure, e:
            print str(e)
            return
        self.get_status()
        #self.multitorrent.rawserver.install_sigint_handler()
        self.multitorrent.rawserver.listen_forever( self.d )
        self.d.display({'activity':_("shutting down"), 'fractionDone':0})
        self.torrent.shutdown()
        print "BitTorrent Debug: shutting down"

    def reread_config(self):
        try:
            newvalues = configfile.get_config(self.config, 'bittorrent-console')
        except Exception, e:
            self.d.error(_("Error reading config: ") + str(e))
            return
        self.config.update(newvalues)
        # The set_option call can potentially trigger something that kills
        # the torrent (when writing this the only possibility is a change in
        # max_files_open causing an IOError while closing files), and so
        # the self.failed() callback can run during this loop.
        for option, value in newvalues.iteritems():
            self.multitorrent.set_option(option, value)
        for option, value in newvalues.iteritems():
            self.torrent.set_option(option, value)

    def get_status(self):
        self.multitorrent.rawserver.add_task(self.get_status,
                                             self.config['display_interval'])
        status = self.torrent.get_status(self.config['spew'])
        self.d.display(status)

    def global_error(self, level, text):
        self.d.error(text)

    def error(self, torrent, level, text):
        self.d.error(text)

    def failed(self, torrent, is_external):
        self.doneflag.set()

    def finished(self, torrent):
        self.d.finished()

if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    
    # download a linux distro
    pipeline(
        ConsoleReader(">>> ", ""),
        TorrentClient("http://www.tlm-project.org/public/distributions/damnsmall/current/dsl-2.4.iso.torrent"),
        ConsoleEchoer(),
    ).run()
