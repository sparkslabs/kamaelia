#!/bin/bash


VERSION=`grep version ../Python/Kamaelia/setup.py |sed -e 's/^[^"]*"//; s/"[^"]*$//;'`
echo "Building $VERSION"

svn export ../Python Kamaelia-$VERSION
cp ../../AUTHORS ../../COPYING Kamaelia-$VERSION
echo "Adding interim/monthly release readme"
sed "s/VERSION/$VERSION/" interim-tarball-readme > Kamaelia-$VERSION/README
tar zcvf Kamaelia-$VERSION.tar.gz Kamaelia-$VERSION/

