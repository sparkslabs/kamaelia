#!/bin/sh


cp ../../AUTHORS Axon/
cp ../../COPYING Axon/

rm -rf Axon/Docs
mkdir Axon/Docs
cp -R Kamaelia/Docs/Axon/ Axon/Docs/
cp Kamaelia/Docs/Axon.html Axon/Docs/Axon.html
cp Kamaelia/Docs/cat.gif Axon/Docs/cat.gif

(
   cd Axon
   cvs update -d .
   rm -rf dist
   python setup.py sdist
   cp dist/* ../Releases
)
