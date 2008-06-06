#!/bin/sh

scripts/publish.prepare.sh #assemble everything we need in the assembly directory
#python byte-compile.py urls.py main.py ServerConfig.py

(
cd assembly
echo "Removing any previously compiled modules"
rm -rf assembly/*.pyc
echo "Creating executable"
zip kpublish.zip urls.py main.py ServerConfig.py Kamaelia Axon WsgiApps $@
cat zipheader.unix kpublish.zip > kpublish
mkdir ../dist
mv kpublish ../dist
)
