#!/bin/sh

echo "Building the Kamaelia Grey distribution"
echo "Currently building inside private_MPS_Scratch branch"

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -R ../../../Axon/Axon/ ../Axon
echo "Copying current Kamaelia"
cp -R ../../../Kamaelia/Kamaelia/ ../Kamaelia

echo "stripping .svn directories"
(
cd ..
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
done
)

# cp ../../../../../trunk/Sketches/MPS/greylisting.py ../App
# cp ../../../../../trunk/Sketches/MPS/greylist.conf.dist ../Config

( cd ../..; tar zcvf Kamaelia-Grey.tar.gz Kamaelia-Grey )
