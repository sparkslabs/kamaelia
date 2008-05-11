#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from distutils.core import setup

#
# The following is linux specific
#
init_script_dir = "/etc/init.d"
init_script = "App/linux_init/kamaeliagrey"

if 0:
    # Mac OS X options
    #
    init_script_dir = "/System/Library/StartupItems/KamaeliaGrey"
    # Need to ensure the above directory exists!!!
    #
    init_script = "App/mac_init/KamaeliaGrey"


setup(name = "Kamaelia-Grey",
      version = "1.0.0",
      description = "Kamaelia Grey - a greylisting SMTP proxy server",
      author = "Michael Sparks & Kamaelia Contributors",
      author_email = "ms_@users.sourceforge.net",
      url = "http://kamaelia.sourceforge.net/KamaeliaGrey",
      license = "(c)2007 BBC & Kamaelia Contributors, All Rights Reserved. Use allowed under MPL 1.1, GPL 2.0, LGPL 2.1",
      packages = ["Axon",
                  "Kamaelia",
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
                  "Kamaelia.Protocol.HTTP",
                  "Kamaelia.Protocol.HTTP.Handlers",
                  "Kamaelia.Protocol.RTP",
                  "Kamaelia.Protocol.Torrent",
                  "Kamaelia.Support",
                  "Kamaelia.Support.Data",
                  "Kamaelia.Support.DVB",
                  "Kamaelia.Support.Particles",
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
                  "Kamaelia.Visualisation.PhysicsGraph",
                  "Kamaelia.XML",
                  ""],
      scripts = ['App/greylisting.py', 'App/runGreylister.sh'],
      data_files=[ ('/etc', ['Config/greylist.conf.dist']),
                   (init_script_dir, [init_script]) ],
      long_description = """
Kamaelia Grey is a greylisting SMTP proxy written using Kamaelia.
This bundle includes all the Kamaelia dependencies in a single pure python
install bundle. 
""",
      )
