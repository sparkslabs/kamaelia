#!/bin/sh
#

echo "Building the Kamaelia Publish distribution"
echo "Currently building inside private_JMB_DescartesComponentsAdded branch"

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -Rv --remove-destination ../../Axon/Axon/ Axon > axon.log
echo "Copying current Kamaelia"
cp -Rv --remove-destination ../../Kamaelia/Kamaelia/ Kamaelia > kamaelia.log

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
