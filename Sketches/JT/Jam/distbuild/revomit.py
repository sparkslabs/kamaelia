#! /usr/bin/env python
###VOMIT: Joe can't use sed
"""
revomit.py - Replaces comments in the setup.py file with arguments piped in 
from a shell script.  I think this may be the single most horrible bit of code
I've ever written.
"""
import sys

f = open(sys.argv[4], "r+")
setupFile = f.read()
setupFile = setupFile.split("#PACKAGES")
setupFile.insert(1, sys.argv[1])
setupFile = ''.join([x for x in setupFile])
setupFile = setupFile.split("#SCRIPTS")
setupFile.insert(1, sys.argv[2])
setupFile = ''.join([x for x in setupFile])
setupFile = setupFile.split("#DATA")
setupFile.insert(1, sys.argv[3])
setupFile = ''.join([x for x in setupFile])
setupFile = setupFile.replace("\\n", "\n")
f.seek(0)
f.write(setupFile)
f.close()

