#!/bin/sh -x

(
   cd Axon-RELEASE/
   rm -f AUTHORS COPYING DEADJOE
   rm -rf dist
   rm -rf Docs
   mkdir Docs

   # Ensure version numbers are up-to-date
   cvs update -r RELEASE -d .

   # Now we clobber everything in this branch. 
   # Reason for the update before copy is to ensure we don't get a clash
   find . -type f | egrep -v '/build/|/CVS/|/dist/|~$|^./MANIFEST' |while read i; do
      cp ../Axon/$i $i
   done

   cvs status . 2>&1 >/dev/null # Reset all timestamps

   # NOTE: We do not tag the release here any more - this allows us to do
   # test builds _without_ clobbering older releases.

   cp ../../../AUTHORS .
   cp ../../../COPYING .

   cp -R ../Kamaelia/Docs/Axon/ Docs/
   cp ../Kamaelia/Docs/Axon.html Docs/Axon.html
   cp ../Kamaelia/Docs/cat.gif Docs/cat.gif

   python setup.py sdist
   cp dist/* ../Releases

   echo "If the release tar ball is fine, please use tagAxonRelease.sh"
   echo "to tag the release"
)
