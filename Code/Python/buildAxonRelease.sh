#!/bin/sh


cp ../../AUTHORS Axon/
cp ../../COPYING Axon/

(
   cd Axon
   cvs update -d .
   rm -rf dist
   python setup.py sdist
   cp dist/* ../Releases
)