#!/bin/sh
#

echo "Assembling Axon/Kamaelia files"
echo "Currently building inside private_JMB_DescartesComponentsAdded branch"

echo
echo "----------------------------------------------------"
echo "Removing old Axon"
rm -rf Axon
echo "Removing old Kamaelia"
rm -rf Kamaelia
echo "----------------------------------------------------"
echo "Copying Axon from branch"
cp -Rv ../../Axon/Axon/ Axon > axon.log
echo "Copying Kamaelia from branch"
cp -Rv ../../Kamaelia/Kamaelia/ Kamaelia > kamaelia.log
echo "----------------------------------------------------"

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
