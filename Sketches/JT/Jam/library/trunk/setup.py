#! /usr/bin/env python
from distutils.core import setup
setup(name="Kamaelia Jam",
      version = "0.1a1",
      packages = ["Kamaelia.Apps.Jam.Internet",
                  "Kamaelia.Apps.Jam.Protocol",
                  "Kamaelia.Apps.Jam.UI",
                  "Kamaelia.Apps.Jam.Util"],
      py_modules = ["Kamaelia.Apps.__init__",
                    "Kamaelia.Apps.Jam.__init__"]
      )

