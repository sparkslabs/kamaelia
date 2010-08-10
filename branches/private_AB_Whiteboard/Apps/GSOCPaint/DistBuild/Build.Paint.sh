#!/bin/sh

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

echo "Building the Kamaelia GSOC Paint distribution"

echo
echo "----------------------------------------------------"
echo "Copying current Axon"
cp -R ../../../Axon/Axon/ ../Axon
echo "Copying current Kamaelia"
cp -R ../../../Kamaelia/Kamaelia/ ../Kamaelia

cp ../../../../../trunk/AUTHORS ../AUTHORS
cp ../../../../../trunk/COPYING ../COPYING

echo "Creating setup.py file"

egrep -B1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" > ../setup.py
egrep -A 1000 START ../../../Axon/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A 1000 START ../../../Kamaelia/setup.py|egrep -B1000 LAST >> ../setup.py
egrep -A1000 "# REPLACE" setup.py.src |grep -v "# REPLACE" >> ../setup.py

cd ..
python setup.py sdist




