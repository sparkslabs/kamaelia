#!/usr/bin/env python

from distutils.core import setup

setup(name = "Axon",
      version = "1.0",
      description = "Axon - Aynschonous Isolated Generator Component System",
      author = "Michael",
      author_email = "ms_@users.sourceforge.net",
      url = "http://kamaelia.sourceforge.net/",
      packages = ["Axon",
                  ""],
      long_description = """
Axon is a software component system. In Axon, components are active and
reactive, independent processing nodes responding to a CSP-like environment.
Systems are composed by creating communications channels (linkages) between
components.
"""
      )
      


