import btree

#create a tree with 16 bytes key and 4 users
btree.createDB("mytree", 16, 4)
btree.createUser("mytree", "user1")
btree.createUser("mytree", "user2")
btree.createUser("mytree", "user3")
btree.createUser("mytree", "user4")

#testing
"""
createUser("mytree.txt", "user5.txt")
ids =[4,5,6,7]
print getCommonKeys("mytree.txt",ids)
ids =[4,5,6]
print getCommonKeys("mytree.txt",ids)
ids =[5,6]
print ids
print getCommonKeys("mytree.txt",ids)
getUserConfig("mytree.txt", 7)
getUserConfig("mytree.txt", 8)
info = getInfo("mytree.txt")
print "key len:", info.key_len
print "max user id:", info.max_user_id
print "current userid:", info.current_user_id
print getUserKey("mytree.txt", 7)
#this shud throw invalid user
print getUserKey("mytree.txt", 8)
"""
