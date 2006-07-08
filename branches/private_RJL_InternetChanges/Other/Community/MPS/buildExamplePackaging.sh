#!/bin/sh

echo "This script builds the example package. When we're happy with it,
echo "this may be integrated into the main distribution to assist people"
echo with sharing their own components and systems"

VERSION=`grep version Demo/setup.py |cut -d\" -f2`

mkdir -p dist
ln -s Demo example-package-$VERSION
tar --exclude=CVS -zcf dist/kamaelia-example-packaging-${VERSION}.tar.gz example-package-${VERSION}/.
rm example-package-$VERSION
echo
echo "Done"
echo
echo "Contents of dist/ : "
ls dist
