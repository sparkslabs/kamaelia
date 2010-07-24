#!/usr/bin/python
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
#

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
import os

graph = ["\n","""DEL ALL
ADD NODE This This auto -
ADD NODE is is auto -
ADD NODE a a auto -
ADD NODE Pipeline Pipeline auto -
ADD LINK This is
ADD LINK is a
ADD LINK a Pipeline
""","""DEL NODE Pipeline
ADD NODE graphline graphline auto -
ADD NODE because because auto -
ADD NODE it it auto -
ADD NODE isn't isn't auto -
ADD NODE pipelike pipelike auto -
ADD LINK a graphline
ADD LINK This because
ADD LINK it isn't
ADD LINK it pipelike
ADD LINK it is
""", 
"""DEL ALL
""", """ADD NODE FIND FIND auto -
ADD NODE EGREP EGREP auto -
ADD NODE READ* READ* auto -
ADD NODE CP CP auto -
ADD LINK FIND EGREP
ADD LINK EGREP READ*
ADD LINK READ* CP
""",
"""ADD NODE ENV ENV auto -
ADD LINK ENV FIND
ADD LINK ENV EGREP
ADD LINK ENV READ*
ADD LINK ENV CP
""","""DEL ALL
""", """ADD NODE ComponentOne ComponentOne auto -
ADD NODE ComponentTwo ComponentTwo auto -
ADD NODE ComponentThree ComponentThree auto -
ADD NODE ComponentFour ComponentFour auto -
ADD NODE ComponentFive ComponentFive auto -
""","""ADD LINK ComponentOne ComponentTwo
ADD LINK ComponentTwo ComponentFive
ADD LINK ComponentThree ComponentFour
ADD LINK ComponentThree ComponentFive
ADD LINK ComponentTwo ComponentFour
""",
"""ADD NODE CAT CAT auto -
ADD LINK CAT ComponentOne
ADD LINK CAT ComponentTwo
ADD LINK CAT ComponentThree
ADD LINK CAT ComponentFour
ADD LINK CAT ComponentFive
""","""DEL ALL
""","""ADD NODE TCPClient TCPClient auto -
ADD NODE VorbisDecode VorbisDecode auto -
ADD NODE AOPlayer AOPlayer auto -
ADD LINK TCPClient VorbisDecode
ADD LINK VorbisDecode AOPlayer
""", """ADD NODE ReadFileAdaptor ReadFileAdaptor auto -
ADD NODE SimpleServer SimpleServer auto -
ADD LINK ReadFileAdaptor SimpleServer
""","""DEL NODE SimpleServer
DEL NODE ReadFileAdaptor
ADD NODE Multicast_Transceiver Multicast_Transceiver auto -
ADD NODE detuple detuple auto -
ADD LINK Multicast_Transceiver detuple
""","""DEL NODE TCPClient
ADD LINK detuple VorbisDecode
""","""DEL ALL
""",
"""ADD NODE reciever reciever auto -
ADD NODE demodulation demodulation auto -
ADD NODE error_correction error_correction auto -
ADD NODE demultiplexing demultiplexing auto -
ADD NODE decode decode auto -
ADD NODE display display auto -
ADD LINK reciever demodulation
ADD LINK demodulation error_correction
ADD LINK error_correction demultiplexing
ADD LINK demultiplexing decode
ADD LINK decode display
""","""DEL ALL
""",
"""ADD NODE ProtocolHandler ProtocolHandler auto -
ADD NODE SimpleServer SimpleServer auto -
ADD NODE FileChooser FileChooser auto -
ADD NODE ImageGrabber ImageGrabber auto -
ADD NODE MyFileReader MyFileReader auto -
ADD LINK ProtocolHandler SimpleServer
ADD LINK FileChooser ImageGrabber
ADD LINK ImageGrabber MyFileReader
ADD LINK ImageGrabber ProtocolHandler
ADD LINK MyFileReader ProtocolHandler
""","""ADD NODE ClientProtocolHandler ClientProtocolHandler auto -
ADD NODE PacketCombiner PacketCombiner auto -
ADD NODE FileWriter FileWriter auto -
ADD NODE PCDisplay PCDisplay auto -
ADD LINK ClientProtocolHandler PacketCombiner
ADD LINK PacketCombiner FileWriter
ADD LINK FileWriter PCDisplay
""","""DEL NODE PCDisplay
ADD NODE NokiaDisplay NokiaDisplay auto -
ADD LINK FileWriter NokiaDisplay
""","""DEL ALL
"""
]

path = "Slides"
extn = ".gif"
#files = os.listdir(path)
#files = [ os.path.join(path,fname) for fname in files if fname[-len(extn):]==extn ]
#files.sort()

allfiles = os.listdir(path)
files = list()
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))

files.sort()

Graphline(
     CHOOSER = Chooser(items = files),
     IMAGE = Image(size=(800,600), position=(0,0)),
     NEXT = Button(caption="Next", msg="NEXT", position=(64,0), transparent=True),
     PREVIOUS = Button(caption="Previous", msg="PREV",position=(0,0), transparent=True),
     FIRST = Button(caption="First", msg="FIRST",position=(256,0), transparent=True),
     LAST = Button(caption="Last", msg="LAST",position=(320,0), transparent=True),
     linkages = {
        ("NEXT","outbox") : ("CHOOSER","inbox"),
        ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
        ("FIRST","outbox") : ("CHOOSER","inbox"),
        ("LAST","outbox") : ("CHOOSER","inbox"),
        ("CHOOSER","outbox") : ("IMAGE","inbox"),
     }
).activate()

Pipeline(
     Button(caption="dink", msg="NEXT", position=(136,0), transparent=True),
     Chooser(items = graph),
     chunks_to_lines(),
     lines_to_tokenlists(),
     TopologyViewer(transparency = (255,255,255), showGrid = False, position=(0,0)),
).run()

