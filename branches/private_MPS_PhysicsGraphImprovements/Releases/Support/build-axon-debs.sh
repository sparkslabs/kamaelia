#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "You need to supply a version number."
    exit 1
fi


cp Axon-$VERSION.tar.gz python-axon_$VERSION.orig.tar.gz || exit 1
tar -xvzf python-axon_$VERSION.orig.tar.gz
mv Axon-$VERSION python-axon-$VERSION

cd python-axon-$VERSION
gzip -dc ../python-axon_*.diff.gz | patch -p1
chmod a+x debian/rules # patch does not mark files as executable
debuild
