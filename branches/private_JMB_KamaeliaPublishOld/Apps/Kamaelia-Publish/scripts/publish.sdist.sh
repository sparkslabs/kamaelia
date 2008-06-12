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

echo "Copying Axon from branch"
cp -R ../../Axon/Axon/ assembly/Axon
echo "Copying Kamaelia from branch"
cp -R ../../Kamaelia/Kamaelia/ assembly/Kamaelia
echo "Copying WsgiApps into staging area"
cp -R WsgiApps assembly/WsgiApps
echo "Copying wsgiref into staging area"
cp -R wsgiref assembly/wsgiref
echo "Copying main.py into staging area"
cp main.py assembly/kpublish.py
echo "Copying ServerConfig.py into staging area"
cp ServerConfig.py assembly/ServerConfig.py
echo "Copying urls.py into staging area"
cp urls.py assembly/urls.py

echo "----------------------------------------------------"
echo "Done preparing!"
echo "----------------------------------------------------"
