#!/bin/sh -x



(
   cd Kamaelia-RELEASE/
   rm -f AUTHORS COPYING DEADJOE
   rm -rf dist

   # Ensure version numbers are up-to-date
   cvs update -r RELEASE -d .

   # Now we clobber everything in this branch. 
   # Reason for the update before copy is to ensure we don't get a clash
   find -type f | egrep -v '/build/|/CVS/|/dist/|~$|^./MANIFEST' |while read i; do
      cp ../Kamaelia/$i $i
   done

   cvs status . 2>&1 >/dev/null # Reset all timestamps

   # Extract the version number from setup.py, replace periods with
   # underscores and create a branch point release tag. (Means that
   # if necessary we can instantiate a branch easily, but don't have to)
   RELEASETAG=bp_`egrep "^ *version *=" setup.py |cut -d\" -f2|sed -e "s/\./_/g"`

   cvs tag $RELEASETAG

   cp ../../../AUTHORS .
   cp ../../../COPYING .
   python setup.py sdist
   cp dist/* ../Releases
)
