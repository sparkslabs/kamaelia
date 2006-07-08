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

# Written by Bram Cohen

#if __name__ == '__main__':
#    from BitTorrent.translation import _

import sys
import locale
#from BitTorrent.defaultargs import get_defaults
#from BitTorrent import configfile
from BitTorrent.makemetafile import make_meta_files
from BitTorrent.parseargs import parseargs, printHelp
from BitTorrent import BTFailure

from Axon.ThreadedComponent import threadedcomponent
from TorrentIPC import *
import time
import os
import tempfile

#defaults = get_defaults('maketorrent-console')
#defaults.extend([
#    ('target', '',
#     _("optional target file for the torrent")),
#    ])
#
#defconfig = dict([(name, value) for (name, value, doc) in defaults])
#del name, value, doc

# Send me TIPCMakeTorrent messages!
class TorrentMaker(threadedcomponent):    
    """Limitations: Only one file per torrent file"""
    def __init__(self, defaulttracker=""):
        super(TorrentMaker, self).__init__()
        self.defaulttracker = defaulttracker
        
    def maketorrent(self, request):
        le = locale.getpreferredencoding()
    
        try:
            tmp = tempfile.mkstemp("", "kamTorrentMaker")
            
            make_meta_files(
                url=request.trackerurl,
                files=[request.srcfile],
                piece_len_pow2=request.log2piecesizebytes,
                title=request.title,
                comment=request.comment,
                target=tmp[1],
                progressfunc=lambda x: None,
                filefunc=lambda x: None,
            )
            tmp = os.fdopen(tmp[0])
            metadata = tmp.read()
            tmp.close()
            
            self.send(metadata, "outbox")
        except BTFailure, e:
            print str(e)
            
    def main(self):
        unfinished = True
        
        while unfinished or self.dataReady("inbox"):
        
            if self.dataReady("inbox"):
                request = self.recv("inbox")
                
                # for easy interaction we allow strings as well as TIPCMakeTorrent messages
                if isinstance(request, str):
                    request = TIPCMakeTorrent(
                        trackerurl=self.defaulttracker,
                        srcfile=request,
                        title=os.path.split(request)[1],
                        comment="Created by Kamaelia",
                        log2piecesizebytes=18 # 256kB
                    )
                
                if isinstance(request, TIPCMakeTorrent):
                    self.maketorrent(request)
                else:
                    print "TorrentMaker - what on earth is a " + str(type(request)) + "!?"
                    
            elif self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    unfinished = False
                elif isinstance(msg, shutdown):
                    return
            else:
                time.sleep(2.0)
                
if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter
    
    # type in a file path and have a .torrent file made for it
    pipeline(
        ConsoleReader(">>> ", ""),
        TorrentMaker("http://example.com:12345/"),
        SimpleFileWriter("downloadedfile.txt")
    ).run()
