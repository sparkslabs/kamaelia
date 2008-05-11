#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

from Axon.Component import component
from Axon.Scheduler import scheduler

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug

from Kamaelia.Util.RateFilter import VariableByteRate_RequestControl as VariableRateControl
from Kamaelia.File.Reading import PromptedFileReader as ReadFileAdapter

from AudioDecoder import AudioDecoder
from SoundOutput import SoundOutput
from BitRateExtractor import BitRateExtractor


filepath = "/opt/kde3/share/apps/khangman/sounds/new_game.ogg"
extn = filepath[-3:].lower()

rateController   = VariableRateControl(rate=4096, chunksize=1024)
fileReader       = ReadFileAdapter(filename=filepath, readmode="bytes")
bitrateExtractor = BitRateExtractor()
decoder          = AudioDecoder(extn)
output           = SoundOutput()

wiringoption = 2

if wiringoption == 1:  #--------------------------------------------------------

    audiosplitter = Splitter()

    decodedAudioSource = pipeline( rateController,
                                   fileReader,
                                   decoder,
                                   audiosplitter
                                 )

    # here we break the encapsulation provided by pipeline
    # - by directly referencing 'audiosplitter'
    bitrateSource = Plug(audiosplitter, bitrateExtractor)

    mainpipe = pipeline( bitrateSource,
                         decodedAudioSource,
                         output ).activate()


elif wiringoption == 2:  #------------------------------------------------------

    decodedAudioSource = Splitter( pipeline( rateController,
                                             fileReader,
                                             decoder )
                                 )

    bitrateSource = Plug(decodedAudioSource, bitrateExtractor)

    mainpipe = pipeline( bitrateSource,
                         decodedAudioSource,
                         output ).activate()


elif wiringoption == 3:  #------------------------------------------------------
    decodedAudioSource = Splitter( pipeline(rateController,
                                            fileReader,
                                            decoder )
                                 )

    bitrateSource = Plug(decodedAudioSource, bitrateExtractor)

    soundout = Plug(decodedAudioSource, output).activate()

    feedbackpipe = pipeline(bitrateSource, decodedAudioSource).activate()


if 0:
    from Kamaelia.Util.Introspector import Introspector
    from Kamaelia.Internet.TCPClient import TCPClient

    pipeline(Introspector(), TCPClient("127.0.0.1", 1500)).activate()

    
scheduler.run.runThreads()