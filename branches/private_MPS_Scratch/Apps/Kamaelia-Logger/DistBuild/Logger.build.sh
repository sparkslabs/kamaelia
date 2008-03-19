#!/bin/sh

echo "Building the Kamaelia Logger distribution"
echo "Currently building inside private_MPS_Scratch branch"

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -R ../../../Axon/Axon/ ../Axon
echo "Copying current Kamaelia"
cp -R ../../../Kamaelia/Kamaelia/ ../Kamaelia

echo "Creating setup.py file"

egrep -B1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" > ../setup.py
egrep -A 1000 START ../../../Axon/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A 1000 START ../../../Kamaelia/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" >> ../setup.py

echo "stripping .svn directories"
(
cd ..
find . -type d|grep .svn$ |while read dirname; do
    echo "rm -rf $dirname"
done
)

( cd ../..; tar zcvf Kamaelia-Logger.tar.gz Kamaelia-Logger )

