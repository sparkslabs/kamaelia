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

"""
===============================
Logical Key Hierarchy Module
================================
A set of functions that implement Logical Key Hierarchy(LKH) scheme for
multicast transmission.
The Logical Key Hierarchy (LKH) scheme is a balanced binary tree based
scheme. The binary tree is persisted in one file.
In an LKH tree, there is a leaf node corresponding to each group member.
The internal nodes are "logical" entities which do not correspond to any
real-life entities in the multicast group, and are only used for key
distribution purposes. There is a key associated with each node in
the tree, and each member holds a copy of every key on the path from
its corresponding leaf node to the root of the tree. Hence, the key
corresponding to the root node is shared by all members, and serves
as the group key.

How it works?
----------------
There are three tree management functions

createDB, createUser, getUserConfig, getInfo

createDB writes all the metadata and user keys in a file .
The file structure:
header size-8 bytes for storing 4 bytes in hex format
key_length-8 bytes for storing 4 bytes in hex format
max_user_id-8 bytes for storing 4 bytes in hex format
next_user_id-8 bytes for storing 4 bytes in hex format
All the key bytes are stored with no delimiters (as we know the key len)
[rootkey][child1 key][chid2 key]...[user1 key][user2key]

createUser creates a user config file. This user config must be distributed
to user in a secure manner. The user and its parent keys are stored.
userid=number
keylen=number
keyid=key
keyid=key
..
..

getUserConfig function prints the user configuration

Session key management
getCommonKeys(list of userids)
this function is used to determine the common set of keys for a group of
active users
"""

import struct, random, array
def create_key(key_len):
    """ Generates key using random device if present
    - key_len    -- length of key
    """
    try:
        #generates truly random numbers
        frand = open("/dev/random", "r")
        data = frand.read(key_len/2)
        frand.close()
        return data.encode('hex')
    except IOError:
        buf =''
        length = key_len/4
        #generates truly pusedo random numbers
        for i in range(length):
            #read one byte at a time
            buf  = buf + struct.pack("!L", random.getrandbits(32)).encode('hex')
        return buf[:key_len]
  

def get_depth(count):
    """ returns the depth of the tree
    - count    -- 32 bit value
    eg: If any number between 9 and 16 is passed the function returns 4
    """
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
    """ creates DB file with all keys and meta data
    - db_file    -- db file name
    - key_len    -- length of the key
    - num_users  -- number of users
    eg: createDB("mytree", 16, 4)
    """
    header_part = HEADER_SIZE/4
    buf = ""
    next_user_id = 0
    max_user_id = 0
    l = 0

    ftree = open(db_file, "w");
    
    #calculate max user id and next user id
    next_user_id = 1 << get_depth(num_users)
    max_user_id = next_user_id << 1

    #4 bytes to store the header size 
    buf = struct.pack("!L", HEADER_SIZE).encode('hex')
    ftree.write(buf)

    #4 bytes to store the key length
    buf = struct.pack("!L", key_len).encode('hex')
    ftree.write(buf)

    #4 bytes to store the max user id
    buf = struct.pack("!L", max_user_id).encode('hex')
    ftree.write(buf)

    #4 bytes to store the next user id
    buf = struct.pack("!L", next_user_id).encode('hex')
    ftree.write(buf)

    #generates keys and write into DB file
    for l  in range(max_user_id):
        ftree.write(create_key(key_len))

    ftree.close()



def createUser(dbfile, user_file):
    """ creates a User and creates config file with user keys
    - db_file    -- db file name
    - user_file  -- User configuration file
    eg: createUser("mytree", "user1")
    """    
    header_part = HEADER_SIZE/4

    ftree = open(dbfile, "r+");

    ftree.seek(header_part);

    #read key len by unpacking 4 bytes 
    buf = ftree.read(header_part)
    key_len = struct.unpack("!L", buf.decode('hex'))[0]

    #read max user id by unpacking 4 bytes 
    buf = ftree.read(header_part)
    max_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    #read next user id by unpacking 4 bytes
    buf = ftree.read(header_part)
    next_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    #create a new user and update the next_user_id 
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

    #create user config file
    fuser = open(user_file, "w")

    fuser.write("#user key configuration\n")
    fuser.write("user_id="+ str(user_id)+"\n")
    fuser.write("key_len="+ str(key_len)+"\n")
    #key is written in hex format
    ftree.seek(HEADER_SIZE + user_id * key_len)
    key = ftree.read(key_len)

    fuser.write(str(user_id) + "=" + str(key) + "\n")
    user_id = user_id >> 1
    #get all the user's parent keys and write to config file
    while( user_id != 0) :
        ftree.seek(HEADER_SIZE + user_id * key_len)
        key = ftree.read(key_len)
        fuser.write(str(user_id) + "=" + key + "\n")
        user_id = user_id >> 1

    fuser.close()
    ftree.close()


def getCommonKeys(db_file, ids):
    """ returns a table of common ids and keys given a list of ids
    - db_file  -- tree db file
    - ids    -- list of userids
    eg: getCommonKeys("mytree", [4,6,7])
    """    
   
    header_part = HEADER_SIZE/4
    ftree = open(db_file, "r")

    ftree.seek(header_part)
    buf = ftree.read(header_part)

    #read key len by unpacking 4 bytes 
    key_len = struct.unpack("!L", buf.decode('hex'))[0]

    idkeymap = {} #holds common id:keys pairs
    #get common set ids
    common_ids = getCommonIds(ids)

    #get common keys
    for ID in common_ids:
        ftree.seek(HEADER_SIZE + ID * key_len)
        idkeymap[ID] = ftree.read(key_len)

    ftree.close()
    return idkeymap


def getCommonIds(ids):
    """ returns a list of common ids/parent ids and given a list of user ids
    - ids    -- list of userids
    eg: getCommonIds([4,6,7])
    """ 
    common_ids = []
    count = len(ids)
    depth  = get_depth(count)

    #make a copy of IDs
    for ID in ids:
        common_ids.append(ID)

    for i in range( 1, depth+1):
        temp = []
        for ID in ids:
            temp.append(ID >> i)

        #count number of common keys
        k = 0
        while ( k < count):
            num = 1
            for j in range(k+1, count):
                if(temp[k] == temp[j]):
                    num = num + 1

            if(num == 1<<i):
                for u in range(k, k + (1<<i)):
                    if((ids[u]>>i) == (ids[k]>>i)):
                        common_ids[u] = ids[k]>>i
            #since numbers are sorted, we can skip the comparision
            k += num


    #remove duplicate ids
    id_list = []
    for ID in common_ids:
        if(id_list.count(ID) == 0) :
            id_list.append(ID)


    return id_list
    

def getUserConfig(dbfile, user_id):
    """ prints user config given user id
    used for troubleshooting
    - dbfile    -- tree database file
    - userid    -- user id
    eg: getUserConfig("mytree", 7)
    """            
    header_part = HEADER_SIZE/4
    ftree = open(dbfile, "r")
    ftree.seek(header_part)
    buf = ftree.read(header_part)
    key_len = struct.unpack("!L", buf.decode('hex'))[0]

    buf = ftree.read(header_part)
    max_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    if( (user_id < max_user_id/2) or (user_id > max_user_id -1)):
        print "user id ", user_id, " not found"
        return

    print "#user key configuration"
    print "user_id=", user_id
    print "key_len=", key_len
    while(user_id != 0):
        ftree.seek(HEADER_SIZE + (user_id * key_len))
        key = ftree.read(key_len)
        print user_id, "=", key
        user_id = user_id >> 1


    ftree.close()


def getUserKey(dbfile, user_id):
    """ return user key given user id
    - dbfile    -- tree database file
    - userid    -- user id
    eg: getUserKey("mytree", 7)
    """    
    header_part = HEADER_SIZE/4
    ftree = open(dbfile, "r")
    ftree.seek(header_part)
    buf = ftree.read(header_part)
    key_len = struct.unpack("!L", buf.decode('hex'))[0]

    buf = ftree.read(header_part)
    max_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    if( (user_id < max_user_id/2) or (user_id > max_user_id -1)):
        raise LookupError("user id " + str(user_id) + " not found")

    ftree.seek(HEADER_SIZE + (user_id * key_len))
    key = ftree.read(key_len)
    ftree.close()
    return key

def getKey(dbfile, ID):
    """ return user key given user id
    - dbfile    -- tree database file
    - userid    -- user id
    eg: getUserKey("mytree", 7)
    """    
    header_part = HEADER_SIZE/4
    ftree = open(dbfile, "r")
    ftree.seek(header_part)
    buf = ftree.read(header_part)
    key_len = struct.unpack("!L", buf.decode('hex'))[0]

    buf = ftree.read(header_part)
    max_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    if( (ID < 1) or (ID > max_user_id-1)):
        raise LookupError("id " + str(ID) + " not found")

    ftree.seek(HEADER_SIZE + (ID * key_len))
    key = ftree.read(key_len)
    ftree.close()
    return key


class DBInfo:
    """ meta data class that contains header"""
    key_len = 0
    current_user_id = 0
    max_user_id = 0



def getInfo(dbfile):
    """ return DBInfo instance given dbfile
    - dbfile    -- tree database file
    used for diagnostic purpose
    eg: getInfo("mytree")
    """    
    header_part = HEADER_SIZE/4
    ftree = open(dbfile, "r")

    ftree.seek(header_part)
    buf = ftree.read(header_part)

    key_len = struct.unpack("!L", buf.decode('hex'))[0]

    buf = ftree.read(header_part)
    max_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    buf = ftree.read(header_part)
    next_user_id = struct.unpack("!L", buf.decode('hex'))[0]

    info = DBInfo()

    info.key_len = key_len
    info.max_user_id = max_user_id
    info.min_user_id = max_user_id>>1
    if(next_user_id == info.min_user_id):
        info.current_user_id = 0 # no new user exists
    else:
        info.current_user_id = next_user_id-1

    ftree.close()
    return info


   

