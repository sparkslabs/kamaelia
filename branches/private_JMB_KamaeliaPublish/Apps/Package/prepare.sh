#!/bin/sh
#This shell script will check to see if an assemly directory already exits and create
#one if not.  It will then copy all of the relevant files over to the assembly directory.

echo "Creating staging area for building"
if [ ! -d assembly ]
then
    mkdir assembly
else
    rm -rf assembly
    mkdir assembly
fi
echo "----------------------------------------------------"
echo "Assembling Axon/Kamaelia files"
echo "Currently building inside private_JMB_DescartesComponentsAdded branch"
echo "----------------------------------------------------"

echo "Copying Axon from branch to assembly directory"
cp -R ../../Axon/Axon/ assembly/Axon
echo "Copying Kamaelia from branch to assembly directory"
cp -R ../../Kamaelia/Kamaelia/ assembly/Kamaelia
echo "Copying zipheader.unix to assembly directory"
cp zipheader.unix assembly/zipheader.unix
echo "Copying scripts into the assembly directory"
cp -R scripts/* assembly
echo "Copying plugins to the assembly directory"
cp -R plugins assembly/plugins
echo "Copying packages to the assembly directory"
cp -R packages assembly/packages

echo "----------------------------------------------------"
echo "Done preparing!"
echo "----------------------------------------------------"
