#!/usr/bin/python
#
# Builds a basic rooted graph in a simple swarm fashion.
#

class peer(object):
   Peermax = 2
   peers = []
   def __init__(self, parent=None):
      self.childrenIDs = []
      self.parent = None
      self.peermax = self.__class__.Peermax
      self.__class__.peers.append(self)
      self.id = len(self.__class__.peers)-1
   def __repr__(self):
      return "peer (ID=%s, parentID=%s, max=%s, children=%s)" % \
              (str(self.id), str(self.parent), str(self.peermax), str(self.childrenIDs))
   def accept(self, fromWhoID):
      if fromWhoID in self.childrenIDs:
         return True, self.parent, self.childrenIDs
      if len(self.childrenIDs) < self.peermax:
         self.childrenIDs.append(fromWhoID)
         return True, self.parent, self.childrenIDs
      else:
         return False, self.parent, self.childrenIDs
   def join(self, nodeID=0):
      index, searchList, accepted, childrenIDs = -1, [], False, [0]
      while not accepted:
         searchList.extend(childrenIDs)
         index = index + 1
         accepted, parent, childrenIDs = peer.peers[index].accept(self.id)
      self.parent = index

z = peer()
a = peer()
b = peer()
c = peer()
d = peer()
e = peer()
f = peer()
g = peer()
h = peer()

a.join()
b.join()
c.join()
d.join()
e.join()
f.join()
g.join()
h.join()

for i in z,a,b,c,d,e,f,g,h:
   print i

print """

The following should just have been displayed:

peer (ID=0, parentID=None, max=2, children=[1, 2])
peer (ID=1, parentID=0, max=2, children=[3, 4])
peer (ID=2, parentID=0, max=2, children=[5, 6])
peer (ID=3, parentID=1, max=2, children=[7, 8])
peer (ID=4, parentID=1, max=2, children=[])
peer (ID=5, parentID=2, max=2, children=[])
peer (ID=6, parentID=2, max=2, children=[])
peer (ID=7, parentID=3, max=2, children=[])
peer (ID=8, parentID=3, max=2, children=[])"""
