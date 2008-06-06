#!/bin/sh
#
echo "Creating staging area for building"
mkdir assembly
echo "----------------------------------------------------"
echo "Assembling Axon/Kamaelia files"
echo "Currently building inside private_JMB_DescartesComponentsAdded branch"

echo
echo "----------------------------------------------------"

echo "Copying Axon from branch"
cp -R ../../Axon/Axon/ assembly/Axon
echo "Copying Kamaelia from branch"
cp -R ../../Kamaelia/Kamaelia/ assembly/Kamaelia
echo "Copying WsgiApps into staging area"
cp -R WsgiApps assembly/WsgiApps
echo "Copying zipheader.unix into staging area"
cp zipheader.unix assembly/WsgiApps
echo "Copying main.py into staging area"
cp main.py assembly/main.py
echo "Copying ServerConfig.py into staging area"
cp ServerConfig.py assembly/ServerConfig.py
echo "----------------------------------------------------"
echo "stripping .svn directories from Axon"
(
cd assembly/Axon
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
    rm -rf $dirname
done
)

echo "stripping .svn directories from Kamaelia"
(
cd assembly/Kamaelia
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
    rm -rf $dirname
done
)

echo "stripping .svn directories from WsgiApps"
(
cd assembly/WsgiApps
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
    rm -rf $dirname
done
)
echo "----------------------------------------------------"
echo "Done preparing!"
echo "----------------------------------------------------"
# cp ../../../../../trunk/Sketches/MPS/greylisting.py ../App
# cp ../../../../../trunk/Sketches/MPS/greylist.conf.dist ../Config

#( cd ../..; tar zcvf Kamaelia-Publish.tar.gz Kamaelia-Publish )
