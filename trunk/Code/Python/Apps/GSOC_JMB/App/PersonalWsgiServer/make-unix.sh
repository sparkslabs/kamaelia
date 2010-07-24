#!/bin/sh
#make-unix.sh
#usage:  ./make-unix.sh [clean] [include-files]
#This script will first run scripts/publish.prepare.sh to assemble all of the relevant
#files into the assembly directory and strip the .svns from them.  It will then remove
#every pyc from the assembly directory.  Once this is finished, it will zip all the
#source files, byte compiled modules, and optimized modules as well as any other
#files that were named in include-files at the command line.  After this, the script
#will concatenate this zip file with zipheader.unix creating the executable (which
#will be moved to the zip directory).
#
#If clean was specified at the command line, the script will remove the assembly directory
#once it is finished.  It is recommended that you remove the assembly directory prior to
#running this script again.
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

./prepare.sh #assemble everything we need in the assembly directory
#python byte-compile.py urls.py main.py ServerConfig.py

if [ "$1" = "clean" ]
then
    CLEANUP=$1
    shift 1
else
    CLEANUP="empty"
fi



(
cd assembly
echo ">Removing any previously compiled modules"
rm -rfv assembly/*.pyc
echo ">Creating executable"
find . -name "*.py"|zip -@ kwserve.zip
find . -name "*.cfg"|zip -@g9 kwserve.zip
find . -name "*.ini"|zip -@g9 kwserve.zip
find . -name "*.tar" | zip -@g9 kwserve.zip
cat zipheader.unix kwserve.zip > kwserve

if [ ! -d ../dist ]
then
    mkdir ../dist
fi

mv kwserve ../dist
chmod a+x ../dist/kwserve
)

if [ "$CLEANUP" = "clean" ]
then
    echo ">Cleaning up!"
    rm -rf assembly
fi
