#!/usr/bin/env python
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

from distutils.core import setup

setup(name = "Kamaelia",
      version = "1.0.11.0", # Year.Year.Month.ReleaseCountThisMonth
      description = "Kamaelia - Multimedia & Server Development Kit",

      author = "Kamaelia Contributors.",
      author_email = "sparks.m@gmail.com",
      url = "http://www.kamaelia.org/",
      license ="Apache Software License",
      packages = [\
                  "Kamaelia", # START
                  "Kamaelia.Apps",
                  "Kamaelia.Apps.Compose",
                  "Kamaelia.Apps.Compose.GUI",
                  "Kamaelia.Apps.CL",
                  "Kamaelia.Apps.CL.FOAFViewer",
                  "Kamaelia.Apps.CL.CollabViewer",
                  "Kamaelia.Apps.Europython09",
                  "Kamaelia.Apps.Europython09.BB",
                  "Kamaelia.Apps.Games4Kids",
                  "Kamaelia.Apps.Grey",
                  "Kamaelia.Apps.GSOCPaint",
                  "Kamaelia.Apps.IRCLogger",
                  "Kamaelia.Apps.JsonRPC",
                  "Kamaelia.Apps.JMB",
                  "Kamaelia.Apps.JMB.Common",
                  "Kamaelia.Apps.JMB.WSGI",
                  "Kamaelia.Apps.JMB.WSGI.Apps",
                  "Kamaelia.Apps.JPB",
                  "Kamaelia.Apps.MH",
                  "Kamaelia.Apps.MPS",
                  "Kamaelia.Apps.SA",
                  "Kamaelia.Apps.Show",
                  "Kamaelia.Apps.SocialBookmarks",
                  "Kamaelia.Apps.SpeakNWrite",
                  "Kamaelia.Apps.SpeakNWrite.Gestures",
                  "Kamaelia.Apps.Whiteboard",
                  "Kamaelia.Automata",
                  "Kamaelia.Audio",
                  "Kamaelia.Audio.PyMedia",
                  "Kamaelia.Audio.Codec",
                  "Kamaelia.Audio.Codec.PyMedia",
                  "Kamaelia.Chassis",
                  "Kamaelia.Codec",
                  "Kamaelia.Device",
                  "Kamaelia.Device.DVB",
                  "Kamaelia.Device.DVB.Parse",
                  "Kamaelia.Experimental",
                  "Kamaelia.File",
                  "Kamaelia.Internet",
                  "Kamaelia.Internet.Simulate",
                  "Kamaelia.Protocol",
                  "Kamaelia.Protocol.AIM",
                  "Kamaelia.Protocol.HTTP",
                  "Kamaelia.Protocol.HTTP.Handlers",
                  "Kamaelia.Protocol.IRC",
                  "Kamaelia.Protocol.RTP",
                  "Kamaelia.Protocol.Torrent",
                  "Kamaelia.Support",
                  "Kamaelia.Support.Data",
                  "Kamaelia.Support.DVB",
                  "Kamaelia.Support.Particles",
                  "Kamaelia.Support.Protocol",
                  "Kamaelia.Support.PyMedia",
                  "Kamaelia.Support.Tk",
                  "Kamaelia.UI",
                  "Kamaelia.UI.Tk",
                  "Kamaelia.UI.MH",
                  "Kamaelia.UI.Pygame",  
                  "Kamaelia.UI.OpenGL",
                  "Kamaelia.Util",
                  "Kamaelia.Util.Tokenisation",
                  "Kamaelia.Video",
                  "Kamaelia.Visualisation",
                  "Kamaelia.Visualisation.Axon",
                  "Kamaelia.Visualisation.ER",
                  "Kamaelia.Visualisation.PhysicsGraph",
                  "Kamaelia.Visualisation.PhysicsGraph3D",
                  "Kamaelia.XML", # LAST
                  ""],
#      scripts = ['Tools/KamaeliaPresent.py'],
      long_description = """
"""
      )
