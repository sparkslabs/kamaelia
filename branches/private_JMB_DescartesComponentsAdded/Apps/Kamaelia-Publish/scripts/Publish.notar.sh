#!/bin/sh
#

echo "Building the Kamaelia Publish distribution"
echo "Currently building inside private_JMB_DescartesComponentsAdded branch"

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -R ../../Axon/Axon/ ./Axon
echo "Copying current Kamaelia"
cp -R ../../Kamaelia/Kamaelia/ ./Kamaelia

echo "stripping .svn directories"
(
cd Axon
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
done
)

(
cd Kamaelia
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
done
)

# cp ../../../../../trunk/Sketches/MPS/greylisting.py ../App
# cp ../../../../../trunk/Sketches/MPS/greylist.conf.dist ../Config

#( cd ../..; tar zcvf Kamaelia-Publish.tar.gz Kamaelia-Publish )
