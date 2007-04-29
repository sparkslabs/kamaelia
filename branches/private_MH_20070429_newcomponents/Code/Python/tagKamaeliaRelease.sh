#!/bin/sh -x



(
   cd Kamaelia-RELEASE/

   # Extract the version number from setup.py, replace periods with
   # underscores and create a branch point release tag. (Means that
   # if necessary we can instantiate a branch easily, but don't have to)
   RELEASETAG=bp_`egrep "^ *version *=" setup.py |cut -d\" -f2|sed -e "s/\./_/g"`

   cvs tag $RELEASETAG

)
