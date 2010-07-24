#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#

from KPI.DB import btree
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage:", sys.argv[0], "dbfile keylength numusers"
        sys.exit(1)
    dbfile = sys.argv[1]
    keylen = long(sys.argv[2])
    numusers = long(sys.argv[3])
    if numusers < 1 :
        print "numusers", sys.argv[3], "is invalid\n"
        sys.exit(1)
    btree.createDB(dbfile, keylen, numusers)
