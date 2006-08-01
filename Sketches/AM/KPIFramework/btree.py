#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#

import struct
import random
import array

"""
All KPI keys are stored in a binary tree. The user key are stored in the 
leaf and parent keys are nodes. The binary tree is persisted in a file.

The file structure:
header size-8 bytes for storing 4 bytes in hex format
key_length-8 bytes for storing 4 bytes in hex format
max_user_id-8 bytes for storing 4 bytes in hex format
next_user_id-8 bytes for storing 4 bytes in hex format
All the key bytes are stored with no delimiters (as we know the key len)
[rootkey][child1 key][chid2 key]...[user1 key][user2key]


There are three tree management functions

build_tree, create_user, get_user_config

build tree creates all the user keys and metadata in the file whose 
structure is described above

create_user creates a user config file. This user config must be distributed
to user in a secure manner. The user and its parent keys are stored.
userid=decimal number
keylen=size in bytes
keyid=key hex format
keyid=key hex format
..
..

get_user_config function prints the user configuration

Session key management
get_common_keys(list of userids)
this function is used to determine the common set of keys for a group of active users
"""
def get_key(key_len):
        try:
            frand = open("/dev/random", "r")
            data = frand.read(key_len/2)
            frand.close()
            return data.encode('hex')
        except IOError:
            buf =''
            length = key_len/4
            for i in range(length):
                #read one byte at a time
		buf  = buf + struct.pack("!L", random.getrandbits(32)).encode('hex')
	    return buf[:key_len]
  

def get_depth(count):
    l = count
    depth = 0
    l = l>> 1
    while l != 0:
        depth = depth + 1
        l = l>> 1        
    #more than one 1s in the binary representation
    if( (count & (count -1)) != 0):
        depth = depth + 1
    return depth



HEADER_SIZE = 32 # 32 bytes of header

def createDB(db_file, key_len, num_users):
    header_part = HEADER_SIZE/4
    buf = ""
    next_user_id = 0
    max_user_id = 0
    l = 0

    ftree = open(db_file, "w");

    next_user_id = 1 << get_depth(num_users)
    max_user_id = next_user_id << 1

    buf = struct.pack("!L", HEADER_SIZE).encode('hex')
    ftree.write(buf)

    buf = struct.pack("!L", key_len).encode('hex')
    ftree.write(buf)

    buf = struct.pack("!L", max_user_id).encode('hex')
    ftree.write(buf)

    buf = struct.pack("!L", next_user_id).encode('hex')
    ftree.write(buf)

    #tree starts from the 2nd key
    for l  in range(max_user_id):
	ftree.write(get_key(key_len))
	
    ftree.close()



def createUser(dbfile, user_file):
    header_part = HEADER_SIZE/4

    ftree = open(dbfile, "r+");

    ftree.seek(header_part);

    buf = ftree.read(header_part)
    key_len = struct.unpack("!L", buf.decode('hex'))[0]
    #print "key length", key_len

    buf = ftree.read(header_part)
    max_user_id = struct.unpack("!L", buf.decode('hex'))[0]
    #print "max user id", max_user_id

    buf = ftree.read(header_part)
    next_user_id = struct.unpack("!L", buf.decode('hex'))[0]
    #print "next user id", next_user_id

    if (next_user_id < max_user_id):
        user_id = next_user_id
        next_user_id = next_user_id+1
        buf = struct.pack("!L", next_user_id).encode('hex')
        ftree.seek(header_part * 3)
        ftree.write(buf)
    else:
	print "Cannot create new user. Maximum users limit exceeded"
	ftree.close()
	return

    fuser = open(user_file, "w")
  	
    fuser.write("#user key configuration\n")
    fuser.write("user_id="+ str(user_id)+"\n")
    fuser.write("key_len="+ str(key_len)+"\n")
    #key is written in hex format
    ftree.seek(HEADER_SIZE + user_id * key_len)
    key = ftree.read(key_len)

    fuser.write(str(user_id) + "=" + str(key) + "\n")
    user_id = user_id >> 1
    while( user_id != 0) :
        ftree.seek(HEADER_SIZE + user_id * key_len)
        key = ftree.read(key_len)
	fuser.write(str(user_id) + "=" + key + "\n")
        user_id = user_id >> 1


    fuser.close()
    ftree.close()



createDB("mytree.txt", 16, 4) #builds tree with 16byte keys and 4 users
createUser("mytree.txt", "user1.txt") #create user cfg user 1
createUser("mytree.txt", "user2.txt")
createUser("mytree.txt", "user3.txt")
createUser("mytree.txt", "user4.txt")
createUser("mytree.txt", "user5.txt") # failure test case. user5 cannot be created.
