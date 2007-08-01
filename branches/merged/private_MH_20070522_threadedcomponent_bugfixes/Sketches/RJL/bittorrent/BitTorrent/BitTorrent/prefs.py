# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.


class Preferences(object):
    def __init__(self, parent=None):
        self._parent = None
        self._options = {}
        if parent:
            self._parent = parent

    def initWithDict(self, dict):
        self._options = dict
        return self

    def getDict(self):
        return dict(self._options)

    def getDifference(self):
        if self._parent:
            return dict([(x, y) for x, y in self._options.items() if y != self._parent.get(x, None)])
        else:
            return dict(self._options)
            
    def __getitem__(self, option):
        if self._options.has_key(option):
            return self._options[option]
        elif self._parent:
            return self._parent[option]
        return None

    def __setitem__(self, option, value):
        self._options.__setitem__(option, value)

    def __len__(self):
        l = len(self._options)
        if self._parent:
            return l + len(self._parent)
        else:
            return l

    def __delitem__(self, option):
        del(self._options[option])

    def clear(self): self._options.clear()

    def has_key(self, option):
        if self._options.has_key(option):
            return True
        elif self._parent:
            return self._parent.has_key(option)
        return False

    def keys(self):
        l = self._options.keys()
        if self._parent:
            l += [key for key in self._parent.keys() if key not in l]
        return l

    def values(self):
        l = self._options.values()
        if self._parent:
            l += [value for value in self._parent.values() if value not in l]
        return l
    
    def items(self):
        l = self._options.items()
        if self._parent:
            l += [item for item in self._parent.items() if item not in l]
        return l

    def __iter__(self): return self.iterkeys()
    def __str__(self): return 'Preferences({%s})' % str(self.items())
    def iteritems(self): return self.items().__iter__()
    def iterkeys(self): return self.keys().__iter__()
    def itervalues(self): return self.values().__iter__()
    def update(self, dict): return self._options.update(dict)

    def get(self, key, failobj=None):
        if not self.has_key(key):
            return failobj
        return self[key]
