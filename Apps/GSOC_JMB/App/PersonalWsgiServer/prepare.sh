#!/bin/sh
#This shell script will check to see if an assemly directory already exits and create
#one if not.  It will then copy all of the relevant files over to the assembly directory.
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
echo "Tarring configuration data."
(
    cd data
    mkdir ../assembly/data
    tar -cvvf ../assembly/data/kpuser.tar kpuser kp.ini --exclude=.svn
)

echo "----------------------------------------------------"
echo "Done preparing!"
echo "----------------------------------------------------"
