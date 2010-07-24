#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import Kamaelia.Support.Data.MimeDict, pprint
reload(Kamaelia.Support.Data.MimeDict)
mailfrom = []
for i in range(0,100):
    F = open("POSSIBLEHAMSTORE/"+str(i),"r")
    H = F.read()
    F.close()
    if H[:5] == '+OK\r\n':
         H = H[5:]
    #
    MD = Kamaelia.Support.Data.MimeDict.MimeDict.fromString(H)
    if MD.get("To"):
       Lines_raw = MD["From"]
       Lines_raw = Lines_raw.replace(",", "\r\n")
       Lines = [x.strip() for x in Lines_raw.split("\r\n")]
       mailfrom = mailfrom+Lines

justmails = []
for X in mailfrom:
   if ("<" in X) and (">" in X):
       X = X[X.find("<")+1:X.rfind(">")]
   justmails.append(X)

justmails.sort()
# pprint.pprint( justmails )
seen = {}
for mail in justmails:
    try:
        seen[mail] += 1
    except KeyError:
        seen[mail] = 1

seen_items = [ (count,value) for (value,count) in seen.items() ]
seen_items.sort()
pprint.pprint( seen_items )

print "you /may/ wish to whitelist some of these:"
print "you /may/ wish to blacklist others"
F = open("whitelist_senders.txt")
whitelist_senders = F.read().split("\n")
F.close()

F = open("blacklist_senders.txt")
blacklist_senders = F.read().split("\n")
F.close()

for (count,value) in seen_items:
    if value in blacklist_senders:
        continue
    if value in whitelist_senders:
        continue
    print value
