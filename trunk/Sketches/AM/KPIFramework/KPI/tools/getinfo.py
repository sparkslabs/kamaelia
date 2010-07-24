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
    if len(sys.argv) < 2:
        print "usage:", sys.argv[0], "dbfile"
        sys.exit(1)
    dbfile = sys.argv[1]
    info = btree.getInfo(dbfile)
    print "--DB Information--"
    print "Key length", info.key_len
    print "User id range [", info.min_user_id, "-", str(info.max_user_id -1) ,"]"
    if info.current_user_id == 0:
        print "Currently there are no users created"
    else:
        print "Current userid", info.current_user_id
    
