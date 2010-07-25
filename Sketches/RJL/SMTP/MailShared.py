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

def listToDict(a):
    x = {}
    for b in a:
        x[b] = True
    return x
    
"""plainchars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                  "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
                  "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                  "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8",
                  "9", "0", ".", "-", "_"]

plaindict = listToDict(plainchars)
print plaindict"""

def isLocalAddress(address, localdict):
    splitaddress = address.split("@")
    if len(splitaddress) == 2 and localdict.get(splitaddress[-1], False):
        return True
    else:
        return False

def isPlain(text):
    plaindict = {'-': True, '.': True, '1': True, '0': True, '3': True, '2': True, '5': True, '4': True, '7': True, '6': True, '9': True, '8': True, 'A': True, 'C': True, 'B': True, 'E': True, 'D': True, 'G': True, 'F': True, 'I': True, 'H': True, 'K': True, 'J': True, 'M': True, 'L': True, 'O': True, 'N': True, 'Q': True, 'P': True, 'S': True, 'R': True, 'U': True, 'T': True, 'W': True, 'V': True, 'Y': True, 'X': True, 'Z': True, '_': True, 'a': True, 'c': True, 'b': True, 'e': True, 'd': True, 'g': True, 'f': True, 'i': True, 'h': True, 'k': True, 'j': True, 'm': True, 'l': True, 'o': True, 'n': True, 'q': True, 'p': True, 's': True, 'r': True, 'u': True, 't': True, 'w': True, 'v': True, 'y': True, 'x': True, 'z': True}

    for c in text:
        if plaindict.get(c, False) == False:
            return False
    return True
