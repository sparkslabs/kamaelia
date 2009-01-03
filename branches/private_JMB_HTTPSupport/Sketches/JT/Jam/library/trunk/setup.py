#! /usr/bin/env python
from distutils.core import setup
setup(name="Kamaelia Jam Library",
      version = "0.1a1",
      platforms = ["any"],
      packages = [
                  "Axon",
                  "Kamaelia",
                  "Kamaelia.Apps",
                  "Kamaelia.Apps.Jam",
                  "Kamaelia.Apps.Jam.Audio", #STARTPACKAGES
                  "Kamaelia.Apps.Jam.Internet",
                  "Kamaelia.Apps.Jam.Protocol",
                  "Kamaelia.Apps.Jam.Support",
                  "Kamaelia.Apps.Jam.Support.Data",
                  "Kamaelia.Apps.Jam.UI",
                  "Kamaelia.Apps.Jam.Util", #LASTPACKAGES
                 ],
      )
