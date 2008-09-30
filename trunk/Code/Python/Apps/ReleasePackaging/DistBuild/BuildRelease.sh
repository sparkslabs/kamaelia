#!/bin/sh -x


echo "Building the Kamaelia release distribution - this builds an integrated Kamaelia & Axon distribution"
echo "---------------------------------------------------------------------------------------------------"
echo
echo "Copying current Axon"
cp -R ../../../Axon/Axon/ ../Axon
echo "Copying current Kamaelia"
cp -R ../../../Kamaelia/Kamaelia/ ../Kamaelia


cp ../../../Axon/README ../Axon.README
cp ../../../Kamaelia/README ../Kamaelia.README

cp ../../../Axon/CHANGELOG ../Axon.CHANGELOG
cp ../../../Kamaelia/CHANGELOG ../Kamaelia.CHANGELOG

echo "Zapping Examples & copying over"
rm -rf ../Examples
cp -R ../../../Kamaelia/Examples ../Examples
cp -R ../../../Axon/Examples ../Examples/Axon

echo "Copying 'Tools' directory over"
cp -R ../../../Kamaelia/Tools ../Tools


echo "Zapping & Copying Documentation"
rm -rf ../Docs
cp -R ../../../Kamaelia/Docs ../Docs

cp ../../../../../AUTHORS ../AUTHORS
cp ../../../../../COPYING ../COPYING

echo "Creating setup.py file"

egrep -B1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" > ../setup.py
egrep -A 1000 START ../../../Axon/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A 1000 START ../../../Kamaelia/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" >> ../setup.py

cp Release.MANIFEST.in ../MANIFEST.in

cd ..
python setup.py sdist
python setup.py bdist_egg
