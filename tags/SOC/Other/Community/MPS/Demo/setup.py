#!/usr/bin/env python
"""
Use of this file is governed by the COPYING file in this distribution
"""
from distutils.core import setup

setup(name = "KamaeliaContributionPackage",
      version = "0.1",
      description = "Sample Kamaelia Community Contribution package",
      author = "Michael",
      author_email = "ms_@users.sourceforge.net",
      url = "http://kamaelia.sourceforge.net/",
      packages = ["Kamaelia",
                  "Kamaelia.Community",
                  "Kamaelia.Community.MPS",
                  ""],
      scripts = [],
      long_description = """
"""
      )
