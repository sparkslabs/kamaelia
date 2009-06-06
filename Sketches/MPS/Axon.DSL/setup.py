#!/usr/bin/python

import sys

if "uninstall" in sys.argv:
    print "uninstall is not supported by distutils, trying anyway"
    print
    print "Rummaging to find me to uninstall me"
    print "I will not uninstall dependencies"
    print
    import Axon.DSL
    print "need to delete this: Axon.DSL"
    print
    import os
    d, f = os.path.split(Axon.DSL.__file__)
    failures = []
    for f in os.listdir(d):
        print "  Removing", os.path.join(d,f),
        try:
            os.unlink(os.path.join(d,f))
            print "Succeeded"
        except Exception, e:
            print "Failed", e
            failures.append((f,e))

    print
    if len(failures)>0:
        print "Did not uninstall all files, are you running as root?"
        print "Please check", d, "for left over files"
        print "Failures:"
        for f,e in failures:
            print " File", f
            print " Error", e

    else:
        print "uninstalled"

else:
    from distutils.core import setup

    setup(name = "Axon.DSL",
          version = "1.0.0",
          description = "Axon: DSL for managing collections of components",
          author = "Michael Sparks",
          author_email = "sparks.m@gmail.com",
          url = "http://www.kamaelia.org/Home",
          license = "Copyright (c)2009 Kamaelia Contributors, All Rights Reserved. Use allowed under MPL 1.1, GPL 2.0, LGPL 2.1",
          packages = ["Axon.DSL", 
                       ],
          long_description=""
    )
