#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "You need to supply a version number."
    exit 1
fi


cp Kamaelia-$VERSION.tar.gz python-kamaelia_$VERSION.orig.tar.gz || exit 1
tar -xvzf python-kamaelia_$VERSION.orig.tar.gz
mv Kamaelia-$VERSION python-kamaelia-$VERSION

cd python-kamaelia-$VERSION
gzip -dc ../python-kamaelia_*.diff.gz | patch -p1
chmod a+x debian/rules # patch does not mark files as executable
debuild
