#!/bin/sh

echo "Building the Kamaelia Whiteboard distribution"
echo "Currently building inside private_MPS_Scratch branch"


echo
echo "----------------------------------------------------"
echo "Copying current Whiteboard"
cp ../../../Kamaelia/Tools/Whiteboard/Whiteboard.py ../App/

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -R ../../../Axon/Axon/ ../Axon
echo "Copying current Kamaelia"
cp -R ../../../Kamaelia/Kamaelia/ ../Kamaelia


( cd ../..; tar zcvf Kamaelia-Whiteboard.tar.gz Kamaelia-Whiteboard --exclude=.svn )
