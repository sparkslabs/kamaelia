#!/bin/sh

echo "Building the Distribution"

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -R ../../../Axon/Axon/ ../Axon
echo "Copying current Kamaelia"
cp -R ../../../Kamaelia/Kamaelia/ ../Kamaelia

echo "Copying Authors & License files"
cp ../../../../../AUTHORS ..
cp ../../../../../COPYING ..

echo "Creating setup.py file"
egrep -B1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" > ../setup.py
egrep -A 1000 START ../../../Axon/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A 1000 START ../../../Kamaelia/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" >> ../setup.py

cd ..
python setup.py sdist




