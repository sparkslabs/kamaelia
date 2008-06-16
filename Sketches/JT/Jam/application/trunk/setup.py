#! /usr/bin/env python
from distutils.core import setup
setup(name = "Kamaelia Jam Application",
      version = "0.1a1",
      scripts = [\
                 "jam", #STARTSCRIPTS LASTSCRIPTS
                ],
      data_files = [("share/kamaelia",
                     [\
                      "PD/PureJam.pd", #STARTDATA LASTDATA
                     ]
                    )
                   ]
      )
