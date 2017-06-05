class TstNode(object):
    key = None
    value = None
    mid = None
    left = None
    right = None

    def __init__(self, key=None, value=None, left=None, right=None, mid=None):
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value
        if mid is not None:
            self.mid = mid
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right


def char_at(s, index):
    if len(s) <= index:
        return -1
    return ord(s[index])


class TernarySearchTrie(object):
    root = None
    N = 0

    def put(self, key, value):
        self.root = self._put(self.root, key, value, 0)

    def _put(self, x, key, value, d):
        c = char_at(key, d)
        if x is None:
            x = TstNode(key=c, value=None)
        compared = c - x.key
        if compared < 0:
            x.left = self._put(x.left, key, value, d)
        elif compared > 0:
            x.right = self._put(x.right, key, value, d)
        else:
            if len(key) - 1 > d:
                x.mid = self._put(x.mid, key, value, d + 1)
            else:
                if x.value is None:
                    self.N += 1
                x.value = value
        return x

    def get(self, key):
        x = self._get(self.root, key, 0)
        if x is None:
            return None
        return x.value

    def _get(self, x, key, d):
        c = char_at(key, d)
        if x is None:
            return None
        compared = c - x.key
        if compared < 0:
            return self._get(x.left, key, d)
        elif compared > 0:
            return self._get(x.right, key, d)
        else:
            if len(key) - 1 > d:
                return self._get(x.mid, key, d + 1)
            else:
                return x

    def delete(self, key):
        self.root = self._delete(self.root, key, 0)

    def _delete(self, x, key, d):
        if x is None:
            return None
        c = char_at(key, d)
        compared = c - x.key
        if compared < 0:
            x.left = self._delete(x.left, key, d)
        elif compared > 0:
            x.right = self._delete(x.right, key, d)
        else:
            if len(key) - 1 > d:
                x.mid = self._delete(x.mid, key, d + 1)
            else:
                self.N -= 1
                x = None
        return x

    def contains_key(self, key):
        x = self._get(self.root, key, 0)
        if x is None:
            return False
        return True

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0

    def keys(self):
        queue = []
        self.collect(self.root, '', queue)
        return queue

    def values(self):
        queue = []
        self.collect_values(self.root, queue)
        return queue

    def collect(self, x, prefix, queue):
        if x is None:
            return
        if x.value is not None:
            queue.append(prefix + chr(x.key))
        self.collect(x.left, prefix, queue)
        self.collect(x.mid, prefix + chr(x.key), queue)
        self.collect(x.right, prefix, queue)

    def collect_values(self, x, queue):
        if x is None:
            return
        if x.value is not None:
            queue.append(x.value)

        self.collect_values(x.left, queue)
        self.collect_values(x.mid, queue)
        self.collect_values(x.right, queue)


class TernarySearchSet(TernarySearchTrie):
    def add(self, key):
        self.put(key, 0)

    def contains(self, key):
        return self.contains_key(key)

    def to_array(self):
        return self.keys()
