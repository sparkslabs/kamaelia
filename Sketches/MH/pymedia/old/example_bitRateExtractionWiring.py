#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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