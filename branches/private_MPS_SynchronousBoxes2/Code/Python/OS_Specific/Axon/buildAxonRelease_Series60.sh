#!/bin/sh

rm -rf dist
mkdir dist
cp ../../../../AUTHORS dist/
cp ../../../../COPYING dist/

(
   cd dist
   cvs co Series60
   mv AUTHORS COPYING Series60

   VERSION=`grep '^Version:' Series60/README|awk '{print $2}'`
   echo "Building Version " $VERSION

   mkdir Series60/Docs
   cp -R ../../../Kamaelia/Docs/Axon Series60/Docs
   cp    ../../../Kamaelia/Docs/Axon.html Series60/Docs
   cp    ../../../Kamaelia/Docs/cat.gif Series60/Docs

   find -type d|egrep "/CVS$"| while read dir; do
      rm -rf $dir
   done
   mv Series60 Axon-$VERSION
   tar zcvf Axon-$VERSION.tar.gz Axon-$VERSION/
   cp Axon-$VERSION.tar.gz ../Releases
)

#rm -rf Axon/Docs
#mkdir Axon/Docs
#cp -R Kamaelia/Docs/Axon/ Axon/Docs/
#cp Kamaelia/Docs/Axon.html Axon/Docs/Axon.html
#cp Kamaelia/Docs/cat.gif Axon/Docs/cat.gif
#
#(
#   cd Axon
#   cvs update -d .
#   rm -rf dist
#   python setup.py sdist
#   cp dist/* ../Releases
#)

#rm -rf dist
